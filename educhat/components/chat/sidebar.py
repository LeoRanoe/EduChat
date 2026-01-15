"""Sidebar component for EduChat."""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import logo, secondary_button, search_input, avatar
from educhat.state.app_state import AppState
from educhat.state.auth_state import AuthState


def render_conversation_item(conv, current_id):
    """Render a single conversation item for use in foreach.
    
    Args:
        conv: Conversation dict with 'id' and 'title' (Reflex Var)
        current_id: Currently active conversation ID (Reflex Var)
    """
    conv_id = conv["id"]
    conv_title = conv["title"]
    
    return rx.box(
        rx.hstack(
            # Icon
            rx.box(
                rx.icon(
                    "message-circle",
                    size=14,
                    color=rx.cond(
                        conv_id == current_id,
                        "white",
                        COLORS["text_tertiary"]
                    ),
                ),
                background=rx.cond(
                    conv_id == current_id,
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    COLORS["light_gray"]
                ),
                padding="0.4rem",
                border_radius="6px",
                flex_shrink="0",
            ),
            # Title
            rx.text(
                conv_title,
                font_size="0.8125rem",
                color=rx.cond(
                    conv_id == current_id,
                    COLORS["primary_green"],
                    COLORS["text_primary"]
                ),
                font_weight=rx.cond(
                    conv_id == current_id,
                    "600",
                    "400"
                ),
                overflow="hidden",
                text_overflow="ellipsis",
                white_space="nowrap",
                flex="1",
                min_width="0",
            ),
            # Action buttons (visible on hover)
            rx.hstack(
                rx.box(
                    rx.icon("trash-2", size=12, color=COLORS["text_tertiary"]),
                    on_click=lambda: AppState.delete_conversation(conv_id),
                    cursor="pointer",
                    padding="0.25rem",
                    border_radius="4px",
                    opacity="0",
                    class_name="conv-action",
                    _hover={
                        "background": "rgba(220, 38, 38, 0.1)",
                        "color": COLORS["error"],
                    },
                    transition="all 0.2s ease",
                ),
                spacing="1",
                flex_shrink="0",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        background=rx.cond(
            conv_id == current_id,
            f"rgba(16, 163, 127, 0.08)",
            "transparent"
        ),
        border_radius="8px",
        padding="0.625rem 0.75rem",
        margin_bottom="0.25rem",
        cursor="pointer",
        on_click=AppState.load_conversation(conv_id),
        border_left=rx.cond(
            conv_id == current_id,
            f"3px solid {COLORS['primary_green']}",
            "3px solid transparent"
        ),
        _hover={
            "background": rx.cond(
                conv_id == current_id,
                f"rgba(16, 163, 127, 0.12)",
                COLORS["hover_bg"]
            ),
            ".conv-action": {"opacity": "1"},
        },
        transition="all 0.2s ease",
    )


def sidebar(
    conversations: List[Dict] = [],
    current_conversation_id: str = "",
    on_new_conversation=None,
    on_search=None,
    on_conversation_click=None,
    user_name: str = "John Doe",
    user_email: str = "johndoe@email.com",
    is_open: bool = False,
    is_collapsed: bool = False,
    on_toggle_collapse=None,
) -> rx.Component:
    """Clean, modern sidebar with toggle functionality.
    
    Args:
        conversations: List of conversation dicts with 'id' and 'title'
        current_conversation_id: ID of active conversation
        on_new_conversation: Handler for new conversation button
        on_search: Handler for search input
        on_conversation_click: Handler for conversation click
        user_name: User's display name
        user_email: User's email
        is_open: Whether sidebar is open (for mobile)
        is_collapsed: Whether sidebar is collapsed (for desktop)
        on_toggle_collapse: Handler for collapse toggle
    """
    return rx.box(
        rx.vstack(
            # Header with logo and close/collapse button
            rx.box(
                rx.hstack(
                    # Logo
                    rx.cond(
                        is_collapsed,
                        rx.icon("graduation-cap", size=24, color=COLORS["primary_green"]),
                        logo(size="md"),
                    ),
                    # Close button for mobile, Collapse button for desktop
                    rx.hstack(
                        # Mobile close button
                        rx.box(
                            rx.icon("x", size=20, color=COLORS["text_secondary"]),
                            on_click=AppState.close_sidebar,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius="8px",
                            display=["flex", "flex", "none"],
                            _hover={"background": COLORS["light_gray"]},
                            transition="all 0.2s ease",
                        ),
                        # Desktop collapse button
                        rx.box(
                            rx.icon(
                                rx.cond(is_collapsed, "chevron-right", "chevron-left"),
                                size=18,
                                color=COLORS["text_secondary"],
                            ),
                            on_click=on_toggle_collapse,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius="8px",
                            display=["none", "none", "flex"],
                            _hover={
                                "background": COLORS["light_green"],
                                "color": COLORS["primary_green"],
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="1",
                    ),
                    justify="between",
                    align="center",
                    width="100%",
                ),
                padding="1rem 1rem 0.75rem",
                border_bottom=f"1px solid {COLORS['border_light']}",
                width="100%",
            ),
            
            # New conversation button
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: Icon only
                    rx.box(
                        rx.icon("plus", size=18, color=COLORS["primary_green"]),
                        on_click=on_new_conversation,
                        cursor="pointer",
                        padding="0.75rem",
                        border_radius="8px",
                        border=f"1px dashed {COLORS['primary_green']}",
                        width="100%",
                        display="flex",
                        justify_content="center",
                        _hover={
                            "background": COLORS["light_green"],
                            "border_style": "solid",
                        },
                        transition="all 0.2s ease",
                    ),
                    # Expanded: Full button
                    rx.box(
                        rx.hstack(
                            rx.icon("plus", size=16, color=COLORS["primary_green"]),
                            rx.text(
                                "Nieuw gesprek",
                                font_size="0.875rem",
                                font_weight="500",
                                color=COLORS["primary_green"],
                            ),
                            spacing="2",
                            align="center",
                            justify="center",
                        ),
                        on_click=on_new_conversation,
                        cursor="pointer",
                        padding="0.625rem 1rem",
                        border_radius="8px",
                        border=f"1px dashed {COLORS['primary_green']}",
                        width="100%",
                        _hover={
                            "background": COLORS["light_green"],
                            "border_style": "solid",
                        },
                        transition="all 0.2s ease",
                    ),
                ),
                padding="0.75rem",
                width="100%",
            ),
            
            # Conversations section header (only when expanded)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.hstack(
                        rx.text(
                            "Gesprekken",
                            font_size="0.6875rem",
                            color=COLORS["text_tertiary"],
                            text_transform="uppercase",
                            font_weight="600",
                            letter_spacing="0.5px",
                        ),
                        rx.box(
                            rx.text(
                                conversations.length(),
                                font_size="0.625rem",
                                color="white",
                                font_weight="600",
                            ),
                            background=COLORS["primary_green"],
                            padding="0.125rem 0.5rem",
                            border_radius="10px",
                            min_width="1.25rem",
                            text_align="center",
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    padding="0.5rem 0.75rem",
                    width="100%",
                ),
            ),
            
            # Conversation list
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: Show dots for conversations
                    rx.vstack(
                        rx.foreach(
                            conversations,
                            lambda conv: rx.box(
                                rx.icon(
                                    "message-circle",
                                    size=16,
                                    color=rx.cond(
                                        conv["id"] == current_conversation_id,
                                        COLORS["primary_green"],
                                        COLORS["text_tertiary"]
                                    ),
                                ),
                                on_click=AppState.load_conversation(conv["id"]),
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius="8px",
                                background=rx.cond(
                                    conv["id"] == current_conversation_id,
                                    COLORS["light_green"],
                                    "transparent"
                                ),
                                _hover={"background": COLORS["light_gray"]},
                                transition="all 0.2s ease",
                            ),
                        ),
                        spacing="1",
                        padding="0.5rem",
                        width="100%",
                    ),
                    # Expanded: Full conversation list
                    rx.cond(
                        conversations.length() > 0,
                        rx.box(
                            rx.foreach(
                                conversations,
                                lambda conv: render_conversation_item(conv, current_conversation_id),
                            ),
                            padding="0 0.5rem",
                            width="100%",
                        ),
                        # Empty state
                        rx.box(
                            rx.vstack(
                                rx.icon("message-square", size=32, color=COLORS["border"]),
                                rx.text(
                                    "Geen gesprekken",
                                    font_size="0.8125rem",
                                    color=COLORS["text_tertiary"],
                                    font_weight="500",
                                ),
                                rx.text(
                                    "Start een nieuw gesprek",
                                    font_size="0.75rem",
                                    color=COLORS["text_tertiary"],
                                ),
                                spacing="2",
                                align="center",
                            ),
                            padding="2rem 1rem",
                            text_align="center",
                            width="100%",
                        ),
                    ),
                ),
                flex="1",
                overflow_y="auto",
                overflow_x="hidden",
                width="100%",
            ),
            
            # Onboarding link (only when expanded)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.link(
                        rx.box(
                            rx.hstack(
                                rx.icon("graduation-cap", size=18, color="white"),
                                rx.text(
                                    "Start Onboarding",
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color="white",
                                ),
                                spacing="2",
                                align="center",
                                justify="center",
                            ),
                            width="100%",
                            padding="0.75rem 1rem",
                            border_radius="8px",
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": f"0 4px 12px rgba(16, 163, 127, 0.3)",
                            },
                            transition="all 0.3s ease",
                        ),
                        href="/onboarding",
                        text_decoration="none",
                        width="100%",
                    ),
                    padding="0.875rem",
                    border_top=f"1px solid {COLORS['border_light']}",
                    border_bottom=f"1px solid {COLORS['border_light']}",
                    width="100%",
                ),
            ),
            
            # Footer with user info
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed: Avatar only with logout
                    rx.vstack(
                        avatar(name=user_name, size="sm"),
                        rx.box(
                            rx.icon("log-out", size=16, color=COLORS["text_tertiary"]),
                            on_click=AppState.logout,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius="6px",
                            _hover={
                                "background": f"rgba(220, 38, 38, 0.1)",
                                "color": COLORS["error"],
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    # Expanded: Full user section with all features
                    rx.vstack(
                        # User info
                        rx.hstack(
                            avatar(name=user_name, size="md"),
                            rx.vstack(
                                rx.text(
                                    user_name,
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color=COLORS["text_primary"],
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                    white_space="nowrap",
                                    line_height="1.2",
                                ),
                                rx.cond(
                                    user_email != "",
                                    rx.text(
                                        user_email,
                                        font_size="0.75rem",
                                        color=COLORS["text_tertiary"],
                                        overflow="hidden",
                                        text_overflow="ellipsis",
                                        white_space="nowrap",
                                        line_height="1.2",
                                    ),
                                    rx.box(
                                        rx.text(
                                            "GAST",
                                            font_size="0.625rem",
                                            color=COLORS["primary_green"],
                                            font_weight="700",
                                            letter_spacing="0.5px",
                                        ),
                                        padding="4px 10px",
                                        background=f"rgba(16, 163, 127, 0.1)",
                                        border_radius="6px",
                                        border=f"1px solid {COLORS['primary_green']}",
                                    ),
                                ),
                                spacing="1",
                                align_items="start",
                                flex="1",
                                min_width="0",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        # Action buttons row 1
                        rx.hstack(
                            rx.box(
                                rx.icon("settings", size=16, color=COLORS["text_secondary"]),
                                rx.text("Settings", font_size="0.8125rem", color=COLORS["text_secondary"]),
                                display="flex",
                                align_items="center",
                                gap="8px",
                                on_click=AuthState.toggle_settings_modal,
                                cursor="pointer",
                                padding="0.625rem 0.75rem",
                                border_radius="8px",
                                flex="1",
                                min_height="40px",
                                _hover={
                                    "background": COLORS["light_gray"],
                                },
                                transition="all 0.2s ease",
                            ),
                            rx.box(
                                rx.icon("bell", size=16, color=COLORS["primary_green"]),
                                rx.text("Reminders", font_size="0.8125rem", color=COLORS["text_secondary"]),
                                display="flex",
                                align_items="center",
                                gap="8px",
                                on_click=AuthState.toggle_reminder_modal,
                                cursor="pointer",
                                padding="0.625rem 0.75rem",
                                border_radius="8px",
                                flex="1",
                                min_height="40px",
                                _hover={
                                    "background": f"rgba(16, 163, 127, 0.1)",
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Action buttons row 2
                        rx.hstack(
                            rx.box(
                                rx.icon("calendar", size=16, color="#3B82F6"),
                                rx.text("Events", font_size="0.8125rem", color=COLORS["text_secondary"]),
                                display="flex",
                                align_items="center",
                                gap="8px",
                                on_click=AuthState.toggle_events_panel,
                                cursor="pointer",
                                padding="0.625rem 0.75rem",
                                border_radius="8px",
                                flex="1",
                                min_height="40px",
                                _hover={
                                    "background": "rgba(59, 130, 246, 0.1)",
                                },
                                transition="all 0.2s ease",
                            ),
                            rx.box(
                                rx.cond(
                                    AuthState.dark_mode,
                                    rx.icon("sun", size=16, color="#F59E0B"),
                                    rx.icon("moon", size=16, color="#6B7280"),
                                ),
                                rx.text(
                                    rx.cond(AuthState.dark_mode, "Light", "Dark"),
                                    font_size="0.8125rem",
                                    color=COLORS["text_secondary"],
                                ),
                                display="flex",
                                align_items="center",
                                gap="8px",
                                on_click=AuthState.toggle_dark_mode,
                                cursor="pointer",
                                padding="0.625rem 0.75rem",
                                border_radius="8px",
                                flex="1",
                                min_height="40px",
                                _hover={
                                    "background": COLORS["light_gray"],
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        # Logout button
                        rx.box(
                            rx.hstack(
                                rx.icon("log-out", size=16, color=COLORS["error"]),
                                rx.text("Uitloggen", font_size="0.8125rem", color=COLORS["error"], font_weight="500"),
                                spacing="2",
                                align="center",
                                justify="center",
                            ),
                            on_click=AppState.logout,
                            cursor="pointer",
                            padding="0.625rem 0.875rem",
                            border_radius="8px",
                            width="100%",
                            min_height="40px",
                            border=f"1px solid {COLORS['error']}20",
                            _hover={
                                "background": f"rgba(220, 38, 38, 0.08)",
                                "border_color": COLORS["error"],
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                padding="1rem",
                border_top=f"1px solid {COLORS['border_light']}",
                width="100%",
                background=COLORS["white"],
            ),
            
            spacing="0",
            height="100%",
            width="100%",
        ),
        # Sidebar container styling
        width=rx.cond(
            is_collapsed,
            ["280px", "280px", "72px"],  # Collapsed: narrow on desktop
            ["280px", "280px", "260px"]  # Expanded
        ),
        min_width=rx.cond(
            is_collapsed,
            ["280px", "280px", "72px"],
            ["280px", "280px", "260px"]
        ),
        background=COLORS["white"],
        border_right=f"1px solid {COLORS['border_light']}",
        height="100vh",
        position="fixed",
        top="0",
        flex_shrink="0",
        # Mobile: slide in/out
        left=rx.cond(is_open, "0", "-100%"),
        z_index=["1001", "1001", "auto"],
        transition="all 0.3s ease",
        box_shadow=rx.cond(
            is_open,
            "4px 0 16px rgba(0, 0, 0, 0.1)",
            "none"
        ),
        overflow="hidden",
        # Desktop: always visible
        **{
            "@media (min-width: 1024px)": {
                "left": "0 !important",
                "position": "relative",
                "box_shadow": "none",
            }
        }
    )

