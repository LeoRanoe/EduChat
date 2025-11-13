"""Sidebar component for EduChat."""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import logo, secondary_button, search_input, avatar
from educhat.state.app_state import AppState


def conversation_item(
    title: str,
    conversation_id: str,
    is_active=False,
    is_collapsed=False,
    on_click=None,
    on_delete=None,
    on_archive=None,
) -> rx.Component:
    """Single conversation item in sidebar list.
    
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
                rx.hstack(
                    rx.box(
                        rx.icon("archive", size=14, color=COLORS["text_tertiary"]),
                        on_click=AppState.archive_conversation(conversation_id),
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
                        on_click=AppState.delete_conversation(conversation_id),
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
            
            # Conversations header (hide when collapsed)
            rx.cond(
                is_collapsed,
                rx.fragment(),
                rx.box(
                    rx.text(
                        "GESPREKKEN",
                        font_size="0.6875rem",
                        color=COLORS["text_secondary"],
                        text_transform="uppercase",
                        font_weight="700",
                        letter_spacing="0.5px",
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
                                lambda conv: rx.box(
                                    rx.hstack(
                                        rx.icon(
                                            "message-circle",
                                            size=18,
                                            color=rx.cond(
                                                conv["id"] == current_conversation_id,
                                                COLORS["primary_green"],
                                                COLORS["text_tertiary"]
                                            ),
                                        ),
                                        rx.text(
                                            conv["title"],
                                            font_size="0.875rem",
                                            color=rx.cond(
                                                conv["id"] == current_conversation_id,
                                                COLORS["primary_green"],
                                                COLORS["text_primary"]
                                            ),
                                            font_weight=rx.cond(
                                                conv["id"] == current_conversation_id,
                                                "600",
                                                "500"
                                            ),
                                            white_space="nowrap",
                                            overflow="hidden",
                                            text_overflow="ellipsis",
                                            flex="1",
                                            letter_spacing="-0.01em",
                                        ),
                                        rx.hstack(
                                            rx.box(
                                                rx.icon("archive", size=14, color=COLORS["text_tertiary"]),
                                                on_click=AppState.archive_conversation(conv["id"]),
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
                                                on_click=AppState.delete_conversation(conv["id"]),
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
                                        spacing="3",
                                        align="center",
                                        width="100%",
                                        justify="start",
                                    ),
                                    background=rx.cond(
                                        conv["id"] == current_conversation_id,
                                        f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['light_green']}80 100%)",
                                        "transparent"
                                    ),
                                    border_radius=RADIUS["lg"],
                                    padding="0.875rem 1rem",
                                    margin="0 0.75rem",
                                    cursor="pointer",
                                    on_click=AppState.load_conversation(conv["id"]),
                                    border_left=rx.cond(
                                        conv["id"] == current_conversation_id,
                                        f"3px solid {COLORS['primary_green']}",
                                        "3px solid transparent"
                                    ),
                                    box_shadow=rx.cond(
                                        conv["id"] == current_conversation_id,
                                        f"0 4px 12px {COLORS['primary_green']}15",
                                        "none"
                                    ),
                                    _hover={
                                        "background": rx.cond(
                                            conv["id"] == current_conversation_id,
                                            f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['light_green']}90 100%)",
                                            f"linear-gradient(135deg, {COLORS['hover_bg']} 0%, {COLORS['light_gray']}40 100%)"
                                        ),
                                        "transform": "translateX(4px)",
                                        "box_shadow": f"0 4px 12px {COLORS['primary_green']}20",
                                        ".conv-action": {"opacity": "1"},
                                    },
                                    transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                                ),
                            ),
                            spacing="1",
                            width="100%",
                        ),
                        rx.text(
                            "Geen gesprekken",
                            font_size="0.875rem",
                            color=COLORS["gray"],
                            text_align="center",
                            padding="2rem 1rem",
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
                            rx.icon("user", size=20, color=COLORS["primary_green"]),
                            display="flex",
                            justify_content="center",
                            width="100%",
                        ),
                        rx.hstack(
                            rx.icon("user", size=18, color=COLORS["primary_green"]),
                            rx.text(
                                "Start onboarding",
                                font_size="0.875rem",
                                font_weight="500",
                                color=COLORS["primary_green"],
                            ),
                            spacing="2",
                            align="center",
                            width="100%",
                        ),
                    ),
                    href="/onboarding",
                    text_decoration="none",
                ),
                padding=rx.cond(is_collapsed, "0.875rem", "0.75rem 1.25rem"),
                border_top=f"1px solid {COLORS['border_gray']}",
                border_bottom=f"1px solid {COLORS['border_gray']}",
                cursor="pointer",
                _hover={
                    "background": COLORS["light_green"],
                },
                transition="all 0.2s ease",
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
                            rx.icon("settings", size=18, color=COLORS["text_secondary"]),
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": COLORS["light_gray"],
                            },
                            transition="all 0.2s ease",
                        ),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    # Expanded view
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
                            rx.text(
                                user_email,
                                font_size="0.75rem",
                                color=COLORS["text_secondary"],
                                line_height="1.2",
                                white_space="nowrap",
                                overflow="hidden",
                                text_overflow="ellipsis",
                            ),
                            spacing="1",
                            align_items="start",
                            flex="1",
                            min_width="0",
                        ),
                        rx.box(
                            rx.icon("settings", size=18, color=COLORS["text_secondary"]),
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            flex_shrink="0",
                            _hover={
                                "background": f"linear-gradient(135deg, {COLORS['light_green']} 0%, {COLORS['primary_green']}10 100%)",
                                "color": COLORS["primary_green"],
                                "transform": "rotate(90deg) scale(1.1)",
                            },
                            transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                        ),
                        spacing="3",
                        align="center",
                        justify="between",
                        width="100%",
                    ),
                ),
                padding=["1rem", "1rem", "1.25rem"],
                width="100%",
                background=COLORS["white"],
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
