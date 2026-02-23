"""Tests for chat message action button handlers.

Covers: copy_message, handle_message_feedback (like/dislike), regenerate_response.
The bookmark handler is intentionally kept in state but UI button has been removed.

Run with: pytest tests/test_button_handlers.py -v
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from educhat.state.app_state import AppState


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def consume(gen):
    """Consume an async generator and return all yielded values."""
    results = []
    async for item in gen:
        results.append(item)
    return results


class _MockParentState:
    """Minimal parent-state stub.

    Reflex's state machinery calls _mark_dirty() and accesses dirty_substates
    on the parent when any state var is mutated.  Without a real Reflex runtime
    the parent_state is None.  This stub satisfies those calls so that tests
    can set inherited vars (like 'is_loading' which lives in AuthState) without
    crashing.

    Also exposes AuthState vars that AppState event handlers READ (e.g.,
    self.language) so they don't raise AttributeError inside the handler try/
    except blocks.
    """

    def __init__(self):
        # Reflex dirty-tracking
        self.dirty_substates: set = set()
        # AuthState-owned vars
        self.is_loading: bool = False
        self.is_authenticated: bool = False
        self.is_guest: bool = False
        self.user_id: object = None
        self.auth_loading: bool = False
        self.language: str = "nl"
        self.user_name: object = None

    def _mark_dirty(self):
        """No-op: we don't need real dirty propagation in tests."""

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        """Return None for any unregistered attribute so nothing raises."""
        return None


def make_state(messages=None):
    """Create an AppState instance pre-loaded with messages.

    is_authenticated defaults to False, so no DB calls are triggered.
    """
    state = AppState()

    # Attach the stub parent so Reflex's inherited-var assignments and
    # _mark_dirty() don't fail due to parent_state being None.
    object.__setattr__(state, "parent_state", _MockParentState())

    state.messages = messages if messages is not None else [
        {
            "content": "Wat is de stelling van Pythagoras?",
            "is_user": True,
            "timestamp": "14:00",
        },
        {
            "content": "De stelling van Pythagoras zegt: a² + b² = c².",
            "is_user": False,
            "timestamp": "14:01",
        },
    ]
    return state


# ---------------------------------------------------------------------------
# copy_message
# ---------------------------------------------------------------------------

class TestCopyMessage:
    """copy_message should emit a JS clipboard call and not mutate messages."""

    @pytest.mark.asyncio
    async def test_copy_yields_event_for_valid_index(self):
        """copy_message on a valid index yields at least one event (the JS call)."""
        state = make_state()
        results = await consume(state.copy_message(1))
        # Should yield the rx.call_script event spec + a trailing yield
        assert len(results) >= 1

    @pytest.mark.asyncio
    async def test_copy_sets_copied_message_index(self):
        """copy_message must set copied_message_index to the target message index."""
        state = make_state()
        # Don't fully consume - just check it sets the index before the sleep
        gen = state.copy_message(1)
        # Advance until copied_message_index is set (first yield after the set)
        try:
            await gen.__anext__()  # rx.call_script yield
            await gen.__anext__()  # yield after setting copied_message_index
        except StopAsyncIteration:
            pass
        assert state.copied_message_index == 1

    @pytest.mark.asyncio
    async def test_copy_invalid_index_yields_nothing(self):
        """copy_message on an out-of-range index yields nothing and does not raise."""
        state = make_state()
        results = await consume(state.copy_message(99))
        assert results == []

    @pytest.mark.asyncio
    async def test_copy_does_not_change_message_content(self):
        """copy_message must never modify message text."""
        state = make_state()
        original = state.messages[1]["content"]
        await consume(state.copy_message(1))
        assert state.messages[1]["content"] == original

    @pytest.mark.asyncio
    async def test_copy_user_message_works(self):
        """copy_message also works on user messages (index 0)."""
        state = make_state()
        results = await consume(state.copy_message(0))
        assert len(results) >= 1


# ---------------------------------------------------------------------------
# handle_message_feedback  (like / dislike)
# ---------------------------------------------------------------------------

class TestHandleMessageFeedback:
    """handle_message_feedback stores the feedback type on the target message."""

    @pytest.mark.asyncio
    async def test_like_sets_feedback_field(self):
        """Feedback type 'like' is written to messages[idx]['feedback']."""
        state = make_state()
        await consume(state.handle_message_feedback(1, "like"))
        assert state.messages[1].get("feedback") == "like"

    @pytest.mark.asyncio
    async def test_dislike_sets_feedback_field(self):
        """Feedback type 'dislike' is written to messages[idx]['feedback']."""
        state = make_state()
        await consume(state.handle_message_feedback(1, "dislike"))
        assert state.messages[1].get("feedback") == "dislike"

    @pytest.mark.asyncio
    async def test_feedback_overwrites_previous(self):
        """A second feedback call should overwrite the first."""
        state = make_state()
        await consume(state.handle_message_feedback(1, "like"))
        await consume(state.handle_message_feedback(1, "dislike"))
        assert state.messages[1]["feedback"] == "dislike"

    @pytest.mark.asyncio
    async def test_feedback_timestamp_is_recorded(self):
        """A feedback_timestamp string is always stored alongside feedback."""
        state = make_state()
        await consume(state.handle_message_feedback(1, "like"))
        ts = state.messages[1].get("feedback_timestamp", "")
        assert len(ts) > 0

    @pytest.mark.asyncio
    async def test_feedback_on_out_of_range_index_is_silent(self):
        """Out-of-range index must not raise or touch existing messages."""
        state = make_state()
        await consume(state.handle_message_feedback(50, "like"))
        assert "feedback" not in state.messages[0]
        assert "feedback" not in state.messages[1]

    @pytest.mark.asyncio
    async def test_no_db_call_when_not_authenticated(self):
        """Database must not be touched for unauthenticated users."""
        state = make_state()
        with patch("educhat.services.supabase_client.get_service") as mock_db:
            await consume(state.handle_message_feedback(1, "like"))
        mock_db.assert_not_called()

    @pytest.mark.asyncio
    async def test_like_on_user_message(self):
        """Like can also be applied to a user message (index 0)."""
        state = make_state()
        await consume(state.handle_message_feedback(0, "like"))
        assert state.messages[0].get("feedback") == "like"


# ---------------------------------------------------------------------------
# regenerate_response
# ---------------------------------------------------------------------------

class TestRegenerateResponse:
    """regenerate_response should re-stream AI output into the bot message slot."""

    def _mock_ai(self, chunks=("Nieuw ", "antwoord.")):
        """Return a mock AI service whose chat_stream yields the given chunks."""
        mock = MagicMock()
        mock.chat_stream.return_value = iter(chunks)
        return mock

    @pytest.mark.asyncio
    async def test_regenerate_replaces_bot_message_content(self):
        """After regeneration the bot message should contain the new response."""
        state = make_state()
        mock_ai = self._mock_ai(["Nieuw antwoord."])

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert "Nieuw antwoord." in state.messages[1]["content"]

    @pytest.mark.asyncio
    async def test_regenerate_multi_chunk_stream(self):
        """Multiple stream chunks should be concatenated in the bot message."""
        state = make_state()
        mock_ai = self._mock_ai(["Deel 1. ", "Deel 2. ", "Deel 3."])

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert "Deel 1. Deel 2. Deel 3." in state.messages[1]["content"]

    @pytest.mark.asyncio
    async def test_regenerate_clears_is_loading_on_success(self):
        """is_loading must be False when the handler finishes normally."""
        state = make_state()
        mock_ai = self._mock_ai(["OK."])

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert state.parent_state.is_loading is False

    @pytest.mark.asyncio
    async def test_regenerate_clears_is_loading_on_error(self):
        """is_loading must be False even when the AI service raises."""
        state = make_state()
        mock_ai = MagicMock()
        mock_ai.chat_stream.side_effect = RuntimeError("AI down")

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert state.parent_state.is_loading is False

    @pytest.mark.asyncio
    async def test_regenerate_shows_error_message_on_exception(self):
        """An AI error should produce a Dutch error message in the bot slot."""
        state = make_state()
        mock_ai = MagicMock()
        mock_ai.chat_stream.side_effect = Exception("timeout")

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert "misgegaan" in state.messages[1]["content"].lower()

    @pytest.mark.asyncio
    async def test_regenerate_out_of_range_index_does_nothing(self):
        """Calling with an invalid index must not change state or raise."""
        state = make_state()
        original_content = state.messages[1]["content"]

        await consume(state.regenerate_response(99))

        assert state.messages[1]["content"] == original_content
        assert state.is_loading is False

    @pytest.mark.asyncio
    async def test_regenerate_index_zero_does_nothing(self):
        """Index 0 has no preceding user message so handler should be a no-op."""
        state = make_state()
        original_content = state.messages[0]["content"]

        await consume(state.regenerate_response(0))

        # messages[0] is a user message at index 0; no user msg precedes it
        assert state.messages[0]["content"] == original_content
        assert state.is_loading is False

    @pytest.mark.asyncio
    async def test_regenerate_preserves_message_count(self):
        """Regeneration must not insert or remove messages."""
        state = make_state()
        original_count = len(state.messages)
        mock_ai = self._mock_ai(["Nieuw."])

        with patch("educhat.state.app_state.get_ai_service", return_value=mock_ai):
            await consume(state.regenerate_response(1))

        assert len(state.messages) == original_count
