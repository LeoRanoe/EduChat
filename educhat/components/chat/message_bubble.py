"""Message bubble component for EduChat."""

import reflex as rx
from typing import Optional
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import icon_button


def user_message(content: str, timestamp: Optional[str] = None) -> rx.Component:
    """User message bubble (right-aligned, green background)."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    content,
                    font_size="0.95rem",
                    color=COLORS["white"],
                    line_height="1.5",
                ),
                background=COLORS["primary_green"],
                border_radius=RADIUS["lg"],
                padding="0.875rem 1.25rem",
                max_width="600px",
            ),
            rx.cond(
                timestamp,
                rx.text(
                    timestamp,
                    font_size="0.75rem",
                    color=COLORS["gray"],
                ),
                rx.fragment(),
            ),
            spacing="1",
            align_items="flex-end",
        ),
        width="100%",
        display="flex",
        justify_content="flex-end",
        margin_bottom="1rem",
    )


def bot_message(
    content: str,
    timestamp: Optional[str] = None,
    on_copy=None,
    on_like=None,
    on_dislike=None,
    on_bookmark=None,
    on_refresh=None,
) -> rx.Component:
    """Bot message bubble (left-aligned, white with border)."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    content,
                    font_size="0.95rem",
                    color=COLORS["dark_gray"],
                    line_height="1.6",
                ),
                background=COLORS["white"],
                border=f"1px solid {COLORS['border_gray']}",
                border_radius=RADIUS["lg"],
                padding="0.875rem 1.25rem",
                max_width="600px",
            ),
            # Action icons
            rx.hstack(
                icon_button(icon="📋", on_click=on_copy, tooltip="Kopiëren"),
                icon_button(icon="👍", on_click=on_like, tooltip="Leuk"),
                icon_button(icon="👎", on_click=on_dislike, tooltip="Niet leuk"),
                icon_button(icon="🔖", on_click=on_bookmark, tooltip="Opslaan"),
                icon_button(icon="🔄", on_click=on_refresh, tooltip="Opnieuw genereren"),
                rx.cond(
                    timestamp,
                    rx.text(
                        timestamp,
                        font_size="0.75rem",
                        color=COLORS["gray"],
                        margin_left="auto",
                    ),
                    rx.fragment(),
                ),
                spacing="1",
                align="center",
                width="100%",
            ),
            spacing="2",
            align_items="flex-start",
        ),
        width="100%",
        display="flex",
        justify_content="flex-start",
        margin_bottom="1rem",
    )


def message_bubble(
    content: str,
    is_user=False,
    timestamp: Optional[str] = None,
    on_copy=None,
    on_like=None,
    on_dislike=None,
    on_bookmark=None,
    on_refresh=None,
) -> rx.Component:
    """Message bubble component for chat messages.
    
    Args:
        content: Message text content
        is_user: Whether this is a user message (vs bot message)
        timestamp: Optional timestamp string
        on_copy: Handler for copy action
        on_like: Handler for like action
        on_dislike: Handler for dislike action
        on_bookmark: Handler for bookmark action
        on_refresh: Handler for refresh/regenerate action
    """
    return rx.cond(
        is_user,
        user_message(content, timestamp),
        bot_message(content, timestamp, on_copy, on_like, on_dislike, on_bookmark, on_refresh),
    )
