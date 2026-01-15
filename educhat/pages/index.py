"""Main chat page for EduChat."""

import reflex as rx
from educhat.state.app_state import AppState
from educhat.state.auth_state import AuthState
from educhat.components.chat import sidebar, chat_container
from educhat.components.shared import mobile_header, sidebar_overlay, reminders_modal, events_panel, settings_modal
from educhat.components.auth import auth_modal
from educhat.components.shared.toast import toast_notification
from educhat.styles.theme import COLORS


def index() -> rx.Component:
    """Main chat interface page with sidebar and chat.
    
    This page requires authentication (either as a logged-in user or guest).
    Unauthenticated users are redirected to the landing page.
    """
    return rx.box(
        rx.cond(
            (AppState.is_authenticated == True) | (AppState.is_guest == True),
            # Show authenticated chat interface
            authenticated_chat(),
            # Redirect unauthenticated users to landing page
            rx.box(
                rx.text("Redirecting...", color=COLORS["text_secondary"]),
                on_mount=AppState.redirect_to_landing,
                display="flex",
                justify_content="center",
                align_items="center",
                height="100vh",
                width="100vw",
            ),
        ),
    )


def authenticated_chat() -> rx.Component:
    """Chat interface for authenticated/guest users."""
    return rx.box(
        # Auth modal (for login/signup)
        auth_modal(),
        
        # Settings modal
        settings_modal(),
        
        # Reminders modal
        reminders_modal(),
        
        # Events panel
        events_panel(),
        
        # Toast notification
        toast_notification(
            message=AppState.toast_message,
            toast_type=AppState.toast_type,
            show=AppState.show_toast,
        ),
        
        # Guest banner (shown only for guest users who haven't dismissed it)
        rx.cond(
            AppState.is_guest & ~AuthState.guest_banner_dismissed,
            guest_banner(),
        ),
        
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
            user_name=rx.cond(AppState.user_name, AppState.user_name, "User"),
            user_email=rx.cond(AppState.user_email, AppState.user_email, ""),
            is_open=AppState.sidebar_open,
            is_collapsed=AppState.sidebar_collapsed,
            on_toggle_collapse=AppState.toggle_sidebar_collapse,
        ),
        
        # Main content area
        rx.box(
            # Guest banner padding spacer (only when banner is visible)
            rx.cond(
                AppState.is_guest & ~AuthState.guest_banner_dismissed,
                rx.box(height="64px"),  # Spacer to prevent content being hidden
                rx.fragment(),
            ),
            
            # Mobile header (only visible on mobile)
            rx.box(
                mobile_header(
                    on_menu_click=AppState.toggle_sidebar,
                    is_sidebar_open=AppState.sidebar_open,
                ),
                display=["block", "block", "none"],
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
            background=rx.cond(AuthState.dark_mode, "#111827", COLORS["light_gray"]),
            display="flex",
            flex_direction="column",
        ),
        
        # Full viewport container
        display="flex",
        flex_direction="row",
        width="100vw",
        height="100vh",
        overflow="hidden",
        background=rx.cond(AuthState.dark_mode, "#111827", COLORS["light_gray"]),
        margin="0",
        padding="0",
        position="relative",
        # Apply dark mode class
        class_name=rx.cond(AuthState.dark_mode, "dark-mode", ""),
        on_mount=AppState.initialize_chat,
    )


def guest_banner() -> rx.Component:
    """Banner shown to guest users encouraging signup - Enhanced."""
    return rx.box(
            rx.box(
                rx.box(
                    # Icon with gradient background
                    rx.box(
                        rx.icon(
                            tag="circle-user",
                            size=22,
                            color=COLORS["primary_green"],
                        ),
                        width="40px",
                        height="40px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                        border_radius="10px",
                        flex_shrink="0",
                        margin_right="16px",
                    ),
                    
                    rx.box(
                        rx.text(
                            "Je gebruikt EduChat als gast. ",
                            rx.text(
                                "Meld je aan",
                                as_="span",
                                font_weight="700",
                                cursor="pointer",
                                color=COLORS["primary_green"],
                                text_decoration="underline",
                                text_decoration_thickness="2px",
                                text_underline_offset="2px",
                                _hover={
                                    "opacity": "0.8",
                                    "text_decoration_color": COLORS["dark_green"],
                                },
                                on_click=AuthState.toggle_auth_modal,
                            ),
                            " om je gesprekken op te slaan en toegang te krijgen tot meer functies.",
                            font_size="14px",
                            color=COLORS["text_primary"],
                            line_height="1.6",
                            font_weight="500",
                        ),
                        flex="1",
                    ),
                    display="flex",
                    align_items="center",
                    flex="1",
                ),
                
                # Close button with hover effect
                rx.box(
                    rx.icon(
                        tag="x",
                        size=18,
                        color=COLORS["text_secondary"],
                    ),
                    cursor="pointer",
                    transition="all 0.3s ease",
                    flex_shrink="0",
                    padding="8px",
                    border_radius="8px",
                    _hover={
                        "color": COLORS["text_primary"],
                        "background": f"rgba(0, 0, 0, 0.05)",
                        "transform": "rotate(90deg)",
                    },
                    on_click=AuthState.dismiss_guest_banner,
                ),
                display="flex",
                justify_content="space-between",
                align_items="center",
                padding="16px 24px",
                gap="16px",
                background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.05) 0%, rgba(13, 138, 107, 0.08) 100%)",
                backdrop_filter="blur(10px)",
                border_bottom=f"2px solid rgba(16, 163, 127, 0.15)",
                width="100%",
                box_shadow="0 4px 16px rgba(16, 163, 127, 0.08)",
                animation="slideDown 0.4s ease-out",
            ),
            position="fixed",
            top="0",
            left=["0", "0", "260px"],  # Offset by sidebar width on desktop
            right="0",
            width=["100%", "100%", "auto"],
            z_index="900",
        )

