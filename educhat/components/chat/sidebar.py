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
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(
                        "message-circle",
                        size=16,
                        color="white",
                    ),
                    background=rx.cond(
                        conv_id == current_id,
                        f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                        COLORS["border"]
                    ),
                    padding="0.5rem",
                    border_radius="8px",
                    transition="all 0.3s ease",
                ),
                rx.box(
                    rx.text(
                        conv_title,
                        font_size="0.875rem",
                        color=rx.cond(
                            conv_id == current_id,
                            COLORS["primary_green"],
                            COLORS["text_primary"]
                        ),
                        font_weight=rx.cond(
                            conv_id == current_id,
                            "600",
                            "500"
                        ),
                        overflow="hidden",
                        text_overflow="ellipsis",
                        display="-webkit-box",
                        webkit_line_clamp="2",
                        webkit_box_orient="vertical",
                        line_height="1.4",
                        max_height="2.8em",
                        letter_spacing="-0.01em",
                        title=conv_title,
                    ),
                    flex="1",
                    min_width="0",
                ),
                rx.hstack(
                    rx.box(
                        rx.icon("pencil", size=14, color=COLORS["text_tertiary"]),
                        on_click=AppState.start_rename_conversation(conv_id),
                        cursor="pointer",
                        padding="0.375rem",
                        border_radius=RADIUS["sm"],
                        opacity="0",
                        class_name="conv-action",
                        background="transparent",
                        _hover={
                            "background": f"rgba(16, 163, 127, 0.1)",
                            "color": COLORS["primary_green"],
                            "transform": "scale(1.1)",
                        },
                        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                    ),
                    rx.box(
                        rx.icon("trash-2", size=14, color=COLORS["text_tertiary"]),
                        on_click=AppState.delete_conversation(conv_id),
                        cursor="pointer",
                        padding="0.375rem",
                        border_radius=RADIUS["sm"],
                        opacity="0",
                        class_name="conv-action",
                        background="transparent",
                        _hover={
                            "background": "rgba(220, 38, 38, 0.1)",
                            "color": COLORS["error"],
                            "transform": "scale(1.1)",
                        },
                        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                    ),
                    spacing="1",
                    flex_shrink="0",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            spacing="0",
            width="100%",
        ),
        background=rx.cond(
            conv_id == current_id,
            f"linear-gradient(135deg, rgba(16, 163, 127, 0.08) 0%, rgba(16, 163, 127, 0.12) 100%)",
            "transparent"
        ),
        border_radius=RADIUS["lg"],
        padding="1rem",
        margin="0 0.75rem 0.5rem 0.75rem",
        cursor="pointer",
        on_click=AppState.load_conversation(conv_id),
        border=rx.cond(
            conv_id == current_id,
            f"1px solid {COLORS['primary_green']}",
            f"1px solid {COLORS['border']}"
        ),
        box_shadow=rx.cond(
            conv_id == current_id,
            f"0 2px 8px rgba(16, 163, 127, 0.15)",
            "none"
        ),
        _hover={
            "background": rx.cond(
                conv_id == current_id,
                f"linear-gradient(135deg, rgba(16, 163, 127, 0.12) 0%, rgba(16, 163, 127, 0.15) 100%)",
                f"rgba(0, 0, 0, 0.02)"
            ),
            "transform": "translateX(4px)",
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 4px 12px rgba(16, 163, 127, 0.2)",
            ".conv-action": {"opacity": "1"},
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        animation="fadeInUp 0.3s ease-out",
    )


def conversation_item(
    title: str,
    conversation_id: str,
    is_active=False,
    is_collapsed=False,
    on_click=None,
    on_delete=None,
    on_archive=None,
) -> rx.Component:
    """Single conversation item in sidebar list (DEPRECATED - kept for backwards compatibility).
    
    Args:
        title: Conversation title
        conversation_id: Unique conversation ID
        is_active: Whether this is the active conversation
        is_collapsed: Whether sidebar is collapsed
        on_click: Click handler
        on_delete: Delete handler
        on_archive: Archive handler
    """
    return rx.box(
        rx.hstack(
            rx.icon(
                "message-circle",
                size=18,
                color=rx.cond(is_active, COLORS["primary_green"], COLORS["text_tertiary"]),
            ),
            # Show text only when not collapsed
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.text(
                    title,
                    font_size="0.875rem",
                    color=rx.cond(is_active, COLORS["primary_green"], COLORS["text_primary"]),
                    font_weight=rx.cond(is_active, "600", "500"),
                    white_space="nowrap",
                    overflow="hidden",
                    text_overflow="ellipsis",
                    flex="1",
                    letter_spacing="-0.01em",
                ),
            ),
            # Action buttons (show only when expanded and on hover)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.box(
                        rx.icon("archive", size=14, color=COLORS["text_tertiary"]),
                        on_click=lambda: AppState.archive_conversation(conversation_id),
                        cursor="pointer",
                        padding="0.375rem",
                        border_radius=RADIUS["sm"],
                        opacity="0",
                        class_name="conv-action",
                        background="transparent",
                        _hover={
                            "background": f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['primary_green']}10 100%)",
                            "color": COLORS["primary_green"],
                            "transform": "scale(1.1)",
                        },
                        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                    ),
                    rx.box(
                        rx.icon("trash-2", size=14, color=COLORS["text_tertiary"]),
                        on_click=lambda: AppState.delete_conversation(conversation_id),
                        cursor="pointer",
                        padding="0.375rem",
                        border_radius=RADIUS["sm"],
                        opacity="0",
                        class_name="conv-action",
                        background="transparent",
                        _hover={
                            "background": f"linear-gradient(135deg, {COLORS['error']}15 0%, {COLORS['error']}25 100%)",
                            "color": COLORS["error"],
                            "transform": "scale(1.1)",
                        },
                        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
                    ),
                    spacing="1",
                    flex_shrink="0",
                ),
            ),
            spacing="3",
            align="center",
            width="100%",
            justify=rx.cond(is_collapsed, "center", "start"),
        ),
        background=rx.cond(
            is_active, 
            f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['light_green']}80 100%)",
            "transparent"
        ),
        border_radius=RADIUS["lg"],
        padding=rx.cond(is_collapsed, "0.875rem", "0.875rem 1rem"),
        margin=rx.cond(is_collapsed, "0 0.5rem", "0 0.75rem"),
        cursor="pointer",
        on_click=on_click,
        border_left=rx.cond(
            is_active,
            f"3px solid {COLORS['primary_green']}",
            "3px solid transparent"
        ),
        box_shadow=rx.cond(
            is_active,
            f"0 4px 12px {COLORS['primary_green']}15",
            "none"
        ),
        _hover={
            "background": rx.cond(
                is_active, 
                f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['light_green']}90 100%)",
                f"linear-gradient(135deg, {COLORS['hover_bg']} 0%, {COLORS['light_gray']}40 100%)"
            ),
            "transform": rx.cond(is_collapsed, "scale(1.08)", "translateX(4px)"),
            "box_shadow": f"0 4px 12px {COLORS['primary_green']}20",
            ".conv-action": {"opacity": "1"},
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
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
    """Sidebar component with logo, search, and conversation list.
    
    Args:
        conversations: List of conversation dicts with 'id' and 'title'
        current_conversation_id: ID of active conversation
        on_new_conversation: Handler for new conversation button
        on_search: Handler for search input
        on_conversation_click: Handler for conversation click
        user_name: User's display name
        user_email: User's email
        is_open: Whether sidebar is open (for mobile)
    """
    return rx.box(
        rx.vstack(
            # Logo section with collapse button and gradient background
            rx.box(
                rx.hstack(
                    rx.cond(
                        is_collapsed,
                        rx.box(
                            rx.icon(
                                "graduation-cap",
                                size=24,
                                color=COLORS["primary_green"],
                            ),
                            width="100%",
                            display="flex",
                            justify_content="center",
                        ),
                        logo(size="md"),
                    ),
                    # Collapse toggle button (desktop only)
                    rx.box(
                        rx.icon(
                            rx.cond(is_collapsed, "panel-right", "panel-left"),
                            size=18,
                            color=COLORS["text_secondary"],
                        ),
                        on_click=on_toggle_collapse,
                        cursor="pointer",
                        padding="0.5rem",
                        border_radius=RADIUS["md"],
                        display=["none", "none", "flex"],
                        background="transparent",
                        border=f"1px solid {COLORS['border_light']}",
                        _hover={
                            "background": f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['primary_green']}15 100%)",
                            "transform": "scale(1.1) rotate(180deg)",
                            "border_color": COLORS["primary_green"],
                            "color": COLORS["primary_green"],
                        },
                        transition="all 0.4s cubic-bezier(0.4, 0, 0.2, 1)",
                    ),
                    spacing="2",
                    align="center",
                    justify="between",
                    width="100%",
                ),
                padding=["1.25rem", "1.25rem", "1.5rem"],
                border_bottom=f"1px solid {COLORS['border_gray']}",
                background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_green']}08 100%)",
            ),
            
            # Action buttons
            rx.cond(
                is_collapsed,
                # Collapsed view - icon only
                rx.vstack(
                    rx.box(
                        rx.icon("pencil", size=20, color=COLORS["primary_green"]),
                        on_click=on_new_conversation,
                        cursor="pointer",
                        padding="0.875rem",
                        border_radius=RADIUS["lg"],
                        border=f"1.5px solid {COLORS['border_gray']}",
                        background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_green']}20 100%)",
                        box_shadow=f"0 2px 8px {COLORS['primary_green']}10",
                        _hover={
                            "background": f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['primary_green']}15 100%)",
                            "border_color": COLORS["primary_green"],
                            "transform": "scale(1.05) rotate(5deg)",
                            "box_shadow": f"0 4px 16px {COLORS['primary_green']}25",
                        },
                        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                        width="100%",
                        display="flex",
                        justify_content="center",
                    ),
                    spacing="2",
                    padding=["1rem", "1rem", "1.25rem"],
                    width="100%",
                ),
                # Expanded view
                rx.vstack(
                    secondary_button(
                        text="Nieuw gesprek",
                        icon="pencil",
                        on_click=on_new_conversation,
                        width="100%",
                    ),
                    spacing="2",
                    padding=["1rem", "1rem", "1.25rem"],
                    width="100%",
                ),
            ),
            
            # Conversations header with count (hide when collapsed)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.hstack(
                        rx.text(
                            "GESPREKKEN",
                            font_size="0.6875rem",
                            color=COLORS["text_secondary"],
                            text_transform="uppercase",
                            font_weight="700",
                            letter_spacing="0.5px",
                        ),
                        rx.box(
                            rx.text(
                                conversations.length(),
                                font_size="0.625rem",
                                color=COLORS["white"],
                                font_weight="600",
                            ),
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            padding="0.125rem 0.5rem",
                            border_radius="12px",
                            min_width="1.5rem",
                            text_align="center",
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    padding="0.75rem 1.25rem 0.5rem",
                ),
            ),
            
            # Conversation list (hide when collapsed)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.cond(
                        conversations.length() > 0,
                        rx.vstack(
                            rx.foreach(
                                conversations,
                                lambda conv: render_conversation_item(conv, current_conversation_id),
                            ),
                            spacing="0",
                            width="100%",
                        ),
                        rx.box(
                            rx.icon(
                                tag="message-square",
                                size=48,
                                color=COLORS["border"],
                                margin_bottom="16px",
                            ),
                            rx.text(
                                "No conversations yet",
                                font_size="0.875rem",
                                color=COLORS["text_secondary"],
                                font_weight="500",
                                margin_bottom="4px",
                            ),
                            rx.text(
                                "Start a new chat to begin",
                                font_size="0.75rem",
                                color=COLORS["text_tertiary"],
                            ),
                            display="flex",
                            flex_direction="column",
                            align_items="center",
                            justify_content="center",
                            padding="3rem 1rem",
                            text_align="center",
                        ),
                    ),
                    flex="1",
                    overflow_y="auto",
                    width="100%",
                ),
            ),
            
            # Onboarding link section
            rx.box(
                rx.link(
                    rx.cond(
                        is_collapsed,
                        rx.box(
                            rx.icon("graduation-cap", size=20, color=COLORS["primary_green"]),
                            display="flex",
                            justify_content="center",
                            width="100%",
                        ),
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
                            border_radius=RADIUS["md"],
                            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                            _hover={
                                "transform": "translateY(-2px)",
                                "box_shadow": f"0 4px 12px rgba(16, 163, 127, 0.3)",
                            },
                            transition="all 0.3s ease",
                        ),
                    ),
                    href="/onboarding",
                    text_decoration="none",
                    width="100%",
                ),
                padding=rx.cond(is_collapsed, "0.875rem", "0.75rem"),
                border_top=f"1px solid {COLORS['border_gray']}",
                border_bottom=f"1px solid {COLORS['border_gray']}",
                width="100%",
            ),
            
            # User profile section
            rx.box(
                rx.cond(
                    is_collapsed,
                    # Collapsed view - avatar only
                    rx.vstack(
                        avatar(name=user_name, size="md"),
                        rx.box(
                            rx.icon("log-out", size=18, color=COLORS["text_secondary"]),
                            on_click=AppState.logout,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": COLORS["light_gray"],
                                "color": COLORS["error"],
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    # Expanded view
                    rx.vstack(
                        rx.hstack(
                            avatar(name=user_name, size="md"),
                            rx.vstack(
                                rx.text(
                                    user_name,
                                    font_size="0.875rem",
                                    font_weight="600",
                                    color=COLORS["text_primary"],
                                    line_height="1.2",
                                    white_space="nowrap",
                                    overflow="hidden",
                                    text_overflow="ellipsis",
                                ),
                                rx.cond(
                                    user_email != "",
                                    rx.text(
                                        user_email,
                                        font_size="0.75rem",
                                        color=COLORS["text_secondary"],
                                        line_height="1.2",
                                        white_space="nowrap",
                                        overflow="hidden",
                                        text_overflow="ellipsis",
                                    ),
                                    rx.box(
                                        rx.text(
                                            "GUEST",
                                            font_size="0.65rem",
                                            color=COLORS["primary_green"],
                                            font_weight="700",
                                            letter_spacing="0.5px",
                                        ),
                                        padding="3px 10px",
                                        background=f"rgba(16, 163, 127, 0.15)",
                                        border_radius="12px",
                                        border=f"1px solid {COLORS['primary_green']}",
                                        display="inline-block",
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
                        rx.hstack(
                            rx.box(
                                rx.icon("settings", size=16, color="black"),
                                rx.text("Settings", font_size="0.8rem", margin_left="8px", color="black"),
                                display="flex",
                                align_items="center",
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["sm"],
                                flex="1",
                                _hover={
                                    "background": COLORS["light_gray"],
                                },
                                transition="all 0.2s ease",
                            ),
                            # Reminders button
                            rx.box(
                                rx.icon("bell", size=16, color=COLORS["primary_green"]),
                                rx.text("Reminders", font_size="0.8rem", margin_left="8px", color="black"),
                                display="flex",
                                align_items="center",
                                on_click=AuthState.toggle_reminder_modal,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["sm"],
                                flex="1",
                                _hover={
                                    "background": f"{COLORS['primary_green']}10",
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="2",
                            width="100%",
                            flex_wrap="wrap",
                        ),
                        rx.hstack(
                            # Events button
                            rx.box(
                                rx.icon("calendar", size=16, color="#3B82F6"),
                                rx.text("Events", font_size="0.8rem", margin_left="8px", color="black"),
                                display="flex",
                                align_items="center",
                                on_click=AuthState.toggle_events_panel,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["sm"],
                                flex="1",
                                _hover={
                                    "background": "rgba(59, 130, 246, 0.1)",
                                },
                                transition="all 0.2s ease",
                            ),
                            # Dark mode toggle
                            rx.box(
                                rx.cond(
                                    AuthState.dark_mode,
                                    rx.icon("sun", size=16, color="#F59E0B"),
                                    rx.icon("moon", size=16, color="#6B7280"),
                                ),
                                rx.text(
                                    rx.cond(AuthState.dark_mode, "Light", "Dark"),
                                    font_size="0.8rem",
                                    margin_left="8px",
                                    color="black",
                                ),
                                display="flex",
                                align_items="center",
                                on_click=AuthState.toggle_dark_mode,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["sm"],
                                flex="1",
                                _hover={
                                    "background": COLORS["light_gray"],
                                },
                                transition="all 0.2s ease",
                            ),
                            rx.box(
                                rx.icon("log-out", size=16, color="black"),
                                rx.text("Logout", font_size="0.8rem", margin_left="8px", color="black"),
                                display="flex",
                                align_items="center",
                                on_click=AppState.logout,
                                cursor="pointer",
                                padding="0.5rem",
                                border_radius=RADIUS["sm"],
                                flex="1",
                                _hover={
                                    "background": f"{COLORS['error']}10",
                                    "color": COLORS["error"],
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="2",
                            width="100%",
                            flex_wrap="wrap",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),
                padding=["1rem", "1rem", "1.25rem"],
                width="100%",
                background=COLORS["white"],
                border_top=f"1px solid {COLORS['border_gray']}",
            ),
            
            spacing="0",
            height="100vh",
            width="100%",
        ),
        # Modern responsive styling with collapse animation
        width=rx.cond(
            is_collapsed,
            ["280px", "280px", "80px"],  # Collapsed: 80px on desktop, full on mobile
            ["280px", "280px", "280px"]  # Expanded
        ),
        background=f"linear-gradient(180deg, {COLORS['white']} 0%, {COLORS['light_green']}05 100%)",
        border_right=f"1px solid {COLORS['border_light']}",
        height="100vh",
        position="fixed",
        top="0",
        overflow_y="auto",
        overflow_x="hidden",
        flex_shrink="0",
        # Mobile: slide in/out based on is_open, above overlay
        left=rx.cond(is_open, "0", "-100%"),
        z_index=["1001", "1001", "auto"],
        transition="width 0.3s cubic-bezier(0.4, 0, 0.2, 1), left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        box_shadow=rx.cond(
            is_open,
            "0 8px 32px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.08)",
            "none"
        ),
        backdrop_filter="blur(8px)",
        
        # Desktop: always visible
        **{
            "@media (min-width: 1024px)": {
                "left": "0 !important",
                "position": "relative",
                "box_shadow": "0 0 1px rgba(0,0,0,0.08), 0 4px 16px rgba(0,0,0,0.04)",
            }
        }
    )

