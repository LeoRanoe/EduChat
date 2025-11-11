"""Main chat page for EduChat."""

import reflex as rx
from educhat.state.app_state import AppState
from educhat.components.chat import sidebar, chat_container


def index() -> rx.Component:
    """Main chat interface page with sidebar and chat."""
    return rx.box(
        # Sidebar
        sidebar(
            conversations=AppState.conversations,
            current_conversation_id=AppState.current_conversation_id,
            on_new_conversation=AppState.create_new_conversation,
            user_name="John Doe",
            user_email="johndoe@email.com",
        ),
        
        # Chat container
        chat_container(
            messages=AppState.messages,
            user_input=AppState.user_input,
            is_loading=AppState.is_loading,
            on_input_change=AppState.set_user_input,
            on_send_message=AppState.send_message,
        ),
        
        # Full viewport container
        width="100vw",
        height="100vh",
        overflow="hidden",
    )
