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
        rx.text(
            title,
            font_size="0.875rem",
            color=rx.cond(is_active, COLORS["primary_green"], COLORS["dark_gray"]),
            font_weight=rx.cond(is_active, "500", "400"),
            white_space="nowrap",
            overflow="hidden",
            text_overflow="ellipsis",
        ),
        background=rx.cond(is_active, COLORS["light_gray"], "transparent"),
        border_left=rx.cond(
            is_active,
            f"3px solid {COLORS['primary_green']}",
            "3px solid transparent"
        ),
        padding="0.75rem 1rem",
        cursor="pointer",
        border_radius=RADIUS["sm"],
        on_click=on_click,
        _hover={
            "background": COLORS["light_gray"],
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
                padding="1.5rem",
                border_bottom=f"1px solid {COLORS['border_gray']}",
            ),
            
            # Action buttons
            rx.vstack(
                secondary_button(
                    text="✏️ Nieuw gesprek",
                    on_click=on_new_conversation,
                    width="100%",
                ),
                spacing="2",
                padding="1rem",
                width="100%",
            ),
            
            # Conversations header
            rx.box(
                rx.text(
                    "Gesprekken ›",
                    font_size="0.75rem",
                    color=COLORS["gray"],
                    text_transform="uppercase",
                    font_weight="600",
                ),
                padding="0 1rem",
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
                            color=COLORS["dark_gray"],
                        ),
                        rx.text(
                            user_email,
                            font_size="0.75rem",
                            color=COLORS["gray"],
                        ),
                        spacing="0",
                        align_items="start",
                    ),
                    rx.box(
                        rx.text("⚙️", font_size="1.2rem", cursor="pointer"),
                        _hover={"opacity": "0.7"},
                    ),
                    spacing="3",
                    align="center",
                    justify="between",
                    width="100%",
                ),
                padding="1rem",
                border_top=f"1px solid {COLORS['border_gray']}",
                width="100%",
            ),
            
            spacing="0",
            height="100vh",
            width="100%",
        ),
        # Responsive width and positioning
        width="280px",
        background=COLORS["white"],
        border_right=f"1px solid {COLORS['border_gray']}",
        height="100vh",
        position="fixed",
        left=rx.cond(is_open, "0", "-280px"),  # Mobile: slide in/out
        top="0",
        z_index="1000",
        transition="left 0.3s ease",
        box_shadow=rx.cond(is_open, "0 0 10px rgba(0,0,0,0.1)", "none"),
        
        # Show sidebar differently on desktop
        **{
            "@media (min-width: 1024px)": {
                "position": "relative",
                "left": "0",
                "z_index": "auto",
                "box_shadow": "none",
            }
        }
    )
