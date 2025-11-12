"""Chat container component for EduChat."""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS
from educhat.components.shared import logo, quick_actions_grid, conversation_templates
from educhat.components.chat.message_bubble import message_bubble
from educhat.components.chat.chat_input import chat_input


def welcome_screen(on_quick_action=None) -> rx.Component:
    """Welcome screen shown when no messages yet.
    
    Args:
        on_quick_action: Handler for quick action clicks
    """
    return rx.box(
        rx.vstack(
            # Welcome header with logo
            rx.vstack(
                rx.heading(
                    "Welkom bij",
                    font_size=["1.25rem", "1.5rem", "1.75rem"],
                    font_weight="600",
                    color=COLORS["text_secondary"],
                    text_align="center",
                    line_height="1.2",
                ),
                logo(size="lg"),
                spacing="1",
                align="center",
                margin_bottom="2rem",
            ),
            
            # Description text
            rx.text(
                "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
                font_size=["0.9375rem", "1rem", "1.0625rem"],
                color=COLORS["text_primary"],
                text_align="center",
                max_width="680px",
                line_height="1.7",
                font_weight="400",
            ),
            rx.text(
                "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
                font_size=["0.875rem", "0.9375rem", "1rem"],
                color=COLORS["text_secondary"],
                text_align="center",
                max_width="680px",
                line_height="1.6",
                margin_bottom="3rem",
            ),
            
            # Quick action buttons
            quick_actions_grid(on_action_click=on_quick_action) if on_quick_action else rx.fragment(),
            
            # Conversation templates
            rx.box(
                rx.vstack(
                    rx.text(
                        "Of start met een stap-voor-stap gids:",
                        font_size=["0.875rem", "0.9375rem", "1rem"],
                        color=COLORS["text_primary"],
                        font_weight="600",
                        margin_bottom="1.25rem",
                        text_align="center",
                    ),
                    conversation_templates(on_template_click=on_quick_action) if on_quick_action else rx.fragment(),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                margin_top="3rem",
                width="100%",
                max_width="900px",
            ),
            
            spacing="0",
            align="center",
            justify="center",
            width="100%",
            max_width="900px",
            padding=["1.5rem", "2rem", "3rem"],
        ),
        height="100%",
        display="flex",
        align_items="center",
        justify_content="center",
        overflow_y="auto",
    )


def chat_container(
    messages: List[Dict] = [],
    user_input: str = "",
    is_loading: bool = False,
    on_input_change=None,
    on_send_message=None,
    on_prompts_click=None,
    on_message_action=None,
    on_quick_action=None,
    on_copy=None,
    on_like=None,
    on_dislike=None,
    on_regenerate=None,
) -> rx.Component:
    """Main chat container with messages and input.
    
    Args:
        messages: List of message dicts with 'content', 'is_user', 'timestamp'
        user_input: Current input value
        is_loading: Loading state
        on_input_change: Handler for input change
        on_send_message: Handler for sending message
        on_prompts_click: Handler for prompts button
        on_message_action: Handler for message actions (copy, like, etc.)
        on_quick_action: Handler for quick action button clicks
        on_copy: Handler for copy message action
        on_like: Handler for like message action
        on_dislike: Handler for dislike message action
        on_regenerate: Handler for regenerate response action
    """
    return rx.box(
        rx.vstack(
            # Messages area with improved styling
            rx.box(
                rx.cond(
                    messages.length() == 0,
                    welcome_screen(on_quick_action=on_quick_action),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                messages,
                                lambda msg, idx: message_bubble(
                                    content=msg["content"],
                                    is_user=msg["is_user"],
                                    timestamp=msg.get("timestamp", ""),
                                    on_copy=lambda: on_copy(idx) if on_copy else None,
                                    on_like=lambda: on_like(idx) if on_like else None,
                                    on_dislike=lambda: on_dislike(idx) if on_dislike else None,
                                    on_refresh=lambda: on_regenerate(idx) if on_regenerate else None,
                                    show_suggestions=rx.cond(
                                        (idx == messages.length() - 1) & ~msg["is_user"],
                                        True,
                                        False
                                    ),
                                    on_suggestion_click=on_quick_action,
                                ),
                            ),
                            spacing="0",
                            width="100%",
                            max_width="900px",
                            margin="0 auto",
                            padding=["1.5rem 1rem", "2rem 1.5rem", "2.5rem 2rem"],
                        ),
                        overflow_y="auto",
                        height="100%",
                        width="100%",
                    ),
                ),
                flex="1",
                width="100%",
                overflow_y="auto",
                background=COLORS["background"],
            ),
            
            # Input area with enhanced styling
            chat_input(
                value=user_input,
                on_change=on_input_change,
                on_submit=on_send_message,
                is_loading=is_loading,
            ),
            
            spacing="0",
            height="100vh",
            width="100%",
        ),
        # Responsive layout
        margin_left="0",
        background=COLORS["background"],
        height="100vh",
        width="100vw",
        
        # Desktop: account for sidebar
        **{
            "@media (min-width: 1024px)": {
                "margin_left": "280px",
                "width": "calc(100vw - 280px)",
            }
        }
    )
