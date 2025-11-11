"""Main chat page for EduChat."""

import reflex as rx
from educhat.state.app_state import AppState
from educhat.components.chat import sidebar, chat_container
from educhat.components.shared import mobile_header, sidebar_overlay


def index() -> rx.Component:
    """Main chat interface page with sidebar and chat."""
    return rx.box(
        # Mobile overlay (darkens background when sidebar open)
        sidebar_overlay(
            is_open=AppState.sidebar_open,
            on_click=AppState.close_sidebar,
        ),
        
        # Sidebar
        sidebar(
            conversations=AppState.conversations,
            current_conversation_id=AppState.current_conversation_id,
            on_new_conversation=AppState.create_new_conversation,
            user_name="John Doe",
            user_email="johndoe@email.com",
            is_open=AppState.sidebar_open,
        ),
        
        # Main content area
        rx.box(
            # Mobile header (only visible on mobile)
            rx.box(
                mobile_header(
                    on_menu_click=AppState.toggle_sidebar,
                    is_sidebar_open=AppState.sidebar_open,
                ),
                display="block",
                **{
                    "@media (min-width: 1024px)": {
                        "display": "none",
                    }
                }
            ),
            
            # Chat container
            chat_container(
                messages=AppState.messages,
                user_input=AppState.user_input,
                is_loading=AppState.is_loading,
                on_input_change=AppState.set_user_input,
                on_send_message=AppState.send_message,
                on_quick_action=AppState.send_quick_action,
                on_copy=AppState.copy_message,
                on_like=lambda idx: AppState.handle_message_feedback(idx, "like"),
                on_dislike=lambda idx: AppState.handle_message_feedback(idx, "dislike"),
                on_regenerate=AppState.regenerate_response,
            ),
            
            width="100%",
            height="100vh",
        ),
        
        # Full viewport container
        display="flex",
        width="100vw",
        height="100vh",
        overflow="hidden",
    )
