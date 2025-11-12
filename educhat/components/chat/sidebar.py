"""Sidebar component for EduChat."""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import logo, secondary_button, search_input, avatar


def conversation_item(
    title: str,
    conversation_id: str,
    is_active=False,
    on_click=None,
) -> rx.Component:
    """Single conversation item in sidebar list.
    
    Args:
        title: Conversation title
        conversation_id: Unique conversation ID
        is_active: Whether this is the active conversation
        on_click: Click handler
    """
    return rx.box(
        rx.hstack(
            rx.icon(
                "message-circle",
                size=18,
                color=rx.cond(is_active, COLORS["primary_green"], COLORS["text_tertiary"]),
            ),
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
            spacing="3",
            align="center",
            width="100%",
        ),
        background=rx.cond(is_active, COLORS["light_green"], "transparent"),
        border_radius=RADIUS["lg"],
        padding="0.875rem 1rem",
        margin="0 0.75rem",
        cursor="pointer",
        on_click=on_click,
        border_left=rx.cond(
            is_active,
            f"3px solid {COLORS['primary_green']}",
            "3px solid transparent"
        ),
        _hover={
            "background": rx.cond(is_active, COLORS["light_green"], COLORS["hover_bg"]),
            "transform": "translateX(2px)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
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
            # Logo section
            rx.box(
                logo(size="md"),
                padding=["1.25rem", "1.25rem", "1.5rem"],
                border_bottom=f"1px solid {COLORS['border_gray']}",
            ),
            
            # Action buttons
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
            
            # Conversations header
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
            
            # Conversation list
            rx.box(
                rx.cond(
                    conversations.length() > 0,
                    rx.vstack(
                        rx.foreach(
                            conversations,
                            lambda conv: conversation_item(
                                title=conv["title"],
                                conversation_id=conv["id"],
                                is_active=conv["id"] == current_conversation_id,
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
            
            # User profile section
            rx.box(
                rx.hstack(
                    avatar(name=user_name, size="md"),
                    rx.vstack(
                        rx.text(
                            user_name,
                            font_size="0.875rem",
                            font_weight="600",
                            color=COLORS["text_primary"],
                            line_height="1.2",
                        ),
                        rx.text(
                            user_email,
                            font_size="0.75rem",
                            color=COLORS["text_secondary"],
                            line_height="1.2",
                        ),
                        spacing="1",
                        align_items="start",
                    ),
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
                    spacing="3",
                    align="center",
                    justify="between",
                    width="100%",
                ),
                padding=["1rem", "1rem", "1.25rem"],
                border_top=f"1px solid {COLORS['border_gray']}",
                width="100%",
                background=COLORS["white"],
            ),
            
            spacing="0",
            height="100vh",
            width="100%",
        ),
        # Modern responsive styling
        width=["280px", "280px", "280px"],
        background=COLORS["white"],
        border_right=f"1px solid {COLORS['border_light']}",
        height="100vh",
        position="fixed",
        left=rx.cond(is_open, "0", "-280px"),
        top="0",
        z_index="1000",
        transition="left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        box_shadow=rx.cond(is_open, "0 8px 32px rgba(0,0,0,0.12)", "none"),
        overflow_y="auto",
        
        # Desktop styling
        **{
            "@media (min-width: 1024px)": {
                "position": "relative",
                "left": "0",
                "z_index": "auto",
                "box_shadow": "0 0 1px rgba(0,0,0,0.1)",
            }
        }
    )
