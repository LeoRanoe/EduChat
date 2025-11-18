"""Chat container component for EduChat."""

import reflex as rx
from typing import List, Dict
from educhat.styles.theme import COLORS
from educhat.components.shared import logo, quick_actions_grid, conversation_templates
from educhat.components.chat.message_bubble import message_bubble
from educhat.components.chat.chat_input import chat_input


def welcome_screen(on_quick_action=None) -> rx.Component:
    """Welcome screen shown when no messages yet - Enhanced.
    
    Args:
        on_quick_action: Handler for quick action clicks
    """
    return rx.box(
        # Animated gradient background
        rx.html(
            f'''<svg width="100%" height="100%" viewBox="0 0 1200 800" fill="none" xmlns="http://www.w3.org/2000/svg" style="position: absolute; top: 0; left: 0; opacity: 0.04; pointer-events: none;">
                <circle cx="200" cy="100" r="120" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="120;150;120" dur="6s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.6;1;0.6" dur="6s" repeatCount="indefinite"/>
                </circle>
                <circle cx="1000" cy="150" r="150" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="150;180;150" dur="7s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.5;0.9;0.5" dur="7s" repeatCount="indefinite"/>
                </circle>
                <circle cx="600" cy="600" r="100" fill="{COLORS['primary_green']}">
                    <animate attributeName="r" values="100;130;100" dur="5s" repeatCount="indefinite"/>
                    <animate attributeName="opacity" values="0.7;1;0.7" dur="5s" repeatCount="indefinite"/>
                </circle>
                <path d="M0,300 Q300,200 600,300 T1200,300" stroke="{COLORS['primary_green']}" stroke-width="2" fill="none" opacity="0.3">
                    <animate attributeName="d" 
                        values="M0,300 Q300,200 600,300 T1200,300;
                                M0,300 Q300,250 600,300 T1200,300;
                                M0,300 Q300,200 600,300 T1200,300" 
                        dur="8s" repeatCount="indefinite"/>
                </path>
            </svg>''',
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            pointer_events="none",
            z_index="0",
        ),
        
        rx.box(
            rx.vstack(
                # Welcome header with enhanced logo
                rx.vstack(
                    # Badge above logo
                    rx.box(
                        rx.icon("sparkles", size=14, color=COLORS["primary_green"]),
                        rx.text("Jouw AI Studiegids", font_size="12px", font_weight="700", color=COLORS["primary_green"]),
                        display="flex",
                        align_items="center",
                        gap="6px",
                        padding="6px 16px",
                        background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.1) 0%, rgba(13, 138, 107, 0.15) 100%)",
                        border_radius="50px",
                        border=f"1.5px solid {COLORS['primary_green']}",
                        margin_bottom="20px",
                        animation="scaleIn 0.6s ease-out",
                    ),
                    
                    rx.heading(
                        "Welkom bij",
                        font_size=["1.5rem", "1.75rem", "2rem"],
                        font_weight="600",
                        color=COLORS["text_secondary"],
                        text_align="center",
                        line_height="1.2",
                        margin_bottom="16px",
                        animation="fadeIn 0.8s ease-out",
                    ),
                    
                    rx.box(
                        rx.box(
                            logo(size="lg"),
                            padding="1.5rem",
                            background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_green']}40 100%)",
                            border_radius="28px",
                            box_shadow=f"0 12px 40px rgba(16, 163, 127, 0.15), 0 4px 12px rgba(0,0,0,0.06)",
                            border=f"2px solid rgba(16, 163, 127, 0.1)",
                            position="relative",
                            overflow="hidden",
                        ),
                        animation="fadeIn 1s ease-out 0.2s backwards",
                    ),
                    
                    spacing="2",
                    align="center",
                    margin_bottom="32px",
                ),
                
                # Description with enhanced styling
                rx.box(
                    rx.text(
                        "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
                        font_size=["1rem", "1.0625rem", "1.125rem"],
                        color=COLORS["text_primary"],
                        text_align="center",
                        line_height="1.7",
                        font_weight="500",
                        margin_bottom="16px",
                    ),
                    rx.text(
                        "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
                        font_size=["0.9375rem", "1rem", "1.0625rem"],
                        color=COLORS["text_secondary"],
                        text_align="center",
                        line_height="1.6",
                    ),
                    max_width="720px",
                    width="100%",
                    padding="24px 32px",
                    background="white",
                    border_radius="20px",
                    box_shadow="0 4px 20px rgba(0, 0, 0, 0.06)",
                    border=f"1px solid {COLORS['border']}",
                    margin_bottom="40px",
                    animation="fadeInUp 0.8s ease-out 0.4s backwards",
                ),
                
                # Section header for popular questions
                rx.box(
                    rx.text(
                        "Populaire vragen:",
                        font_size=["0.9375rem", "1rem", "1.0625rem"],
                        color=COLORS["text_primary"],
                        font_weight="700",
                        text_align="center",
                        margin_bottom="24px",
                    ),
                    width="100%",
                    max_width="800px",
                    animation="fadeIn 0.8s ease-out 0.5s backwards",
                ),
                
                # Quick action buttons with stagger animation
                rx.box(
                    quick_actions_grid(on_action_click=on_quick_action) if on_quick_action else rx.fragment(),
                    width="100%",
                    max_width="800px",
                    animation="fadeInUp 0.8s ease-out 0.6s backwards",
                ),
                
                # Conversation templates section
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Of start met een stap-voor-stap gids:",
                            font_size=["0.9375rem", "1rem", "1.0625rem"],
                            color=COLORS["text_primary"],
                            font_weight="700",
                            text_align="center",
                            margin_bottom="20px",
                        ),
                        conversation_templates(on_template_click=on_quick_action) if on_quick_action else rx.fragment(),
                        spacing="3",
                        align="center",
                        width="100%",
                    ),
                    margin_top="48px",
                    width="100%",
                    max_width="800px",
                    animation="fadeIn 0.8s ease-out 0.7s backwards",
                ),
                
                spacing="4",
                align="center",
                width="100%",
            ),
            width="100%",
            max_width="1000px",
            margin="0 auto",
            padding=["2rem 1rem", "2.5rem 1.5rem", "4rem 2rem"],
            position="relative",
            z_index="1",
        ),
        
        width="100%",
        height="100%",
        overflow_y="auto",
        display="flex",
        align_items="start",
        justify_content="start",
        position="relative",
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
                                    is_thinking=msg.get("is_thinking", False),
                                    is_streaming=msg.get("is_streaming", False),
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
                        custom_attrs={"data-chat-container": "true"},
                    ),
                ),
                flex="1",
                width="100%",
                overflow_y="auto",
                background=COLORS["background"],
                min_height="0",
            ),
            
            # Input area with enhanced styling
            chat_input(
                value=user_input,
                on_change=on_input_change,
                on_submit=on_send_message,
                is_loading=is_loading,
            ),
            
            spacing="0",
            height="100%",
            width="100%",
        ),
        # Responsive layout
        background=COLORS["background"],
        height="100%",
        width="100%",
        flex="1",
        overflow="hidden",
    )

