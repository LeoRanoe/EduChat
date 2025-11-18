"""Message bubble component for EduChat."""

import reflex as rx
from typing import Optional
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import icon_button


def user_message(content: str, timestamp: Optional[str] = None) -> rx.Component:
    """User message bubble (right-aligned, modern green gradient)."""
    return rx.box(
        rx.vstack(
            rx.box(
                rx.text(
                    content,
                    font_size=["0.9375rem", "0.9375rem", "1rem"],
                    color=COLORS["white"],
                    line_height="1.65",
                    font_weight="400",
                    letter_spacing="0.005em",
                ),
                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                border_radius=RADIUS["2xl"],
                padding=["1.25rem 1.5rem", "1.375rem 1.625rem", "1.5rem 1.75rem"],
                max_width=["90%", "80%", "720px"],
                word_wrap="break-word",
                box_shadow="0 2px 10px rgba(16, 163, 127, 0.2), 0 1px 3px rgba(0,0,0,0.08)",
                transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
                _hover={
                    "transform": "translateY(-1px)",
                    "box_shadow": "0 4px 14px rgba(16, 163, 127, 0.25), 0 2px 4px rgba(0,0,0,0.1)",
                },
                class_name="message-bubble",
            ),
            rx.cond(
                timestamp,
                rx.text(
                    timestamp,
                    font_size=["0.6875rem", "0.6875rem", "0.75rem"],
                    color=COLORS["text_tertiary"],
                    font_weight="500",
                ),
                rx.fragment(),
            ),
            spacing="2",
            align_items="flex-end",
        ),
        width="100%",
        display="flex",
        justify_content="flex-end",
        margin_bottom=["1.25rem", "1.25rem", "1.5rem"],
        padding_left=["1rem", "1.5rem", "2rem"],
    )


def bot_message(
    content: str,
    timestamp: Optional[str] = None,
    on_copy=None,
    on_like=None,
    on_dislike=None,
    on_bookmark=None,
    on_refresh=None,
    show_suggestions: bool = False,
    on_suggestion_click=None,
    is_thinking: bool = False,
    is_streaming: bool = False,
) -> rx.Component:
    """Bot message bubble (left-aligned, modern card style)."""
    from educhat.components.shared import contextual_follow_ups
    
    return rx.box(
        rx.vstack(
            # Main message card
            rx.box(
                rx.hstack(
                    # Avatar/Icon
                    rx.box(
                        rx.icon(
                            "graduation-cap",
                            size=20,
                            color=COLORS["primary_green"],
                        ),
                        width="36px",
                        height="36px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=COLORS["light_green"],
                        border_radius=RADIUS["full"],
                        flex_shrink="0",
                    ),
                    # Message content
                    rx.box(
                        rx.cond(
                            is_thinking,
                            # Thinking indicator with smooth, attractive animation
                            rx.hstack(
                                rx.box(
                                    width="8px",
                                    height="8px",
                                    border_radius="50%",
                                    background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                    animation="pulse 1.4s infinite ease-in-out 0s",
                                    box_shadow="0 2px 6px rgba(16, 163, 127, 0.3)",
                                ),
                                rx.box(
                                    width="8px",
                                    height="8px",
                                    border_radius="50%",
                                    background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                    animation="pulse 1.4s infinite ease-in-out 0.2s",
                                    box_shadow="0 2px 6px rgba(16, 163, 127, 0.3)",
                                ),
                                rx.box(
                                    width="8px",
                                    height="8px",
                                    border_radius="50%",
                                    background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                    animation="pulse 1.4s infinite ease-in-out 0.4s",
                                    box_shadow="0 2px 6px rgba(16, 163, 127, 0.3)",
                                ),
                                spacing="2",
                                align="center",
                                padding="0.75rem 0",
                                animation="breathe 3s infinite ease-in-out",
                            ),
                            # Normal markdown content with optional typing cursor
                            rx.box(
                                rx.markdown(
                                    content,
                                    class_name="bot-message-content",
                                    color=COLORS["text_primary"],
                                    font_size=["0.9375rem", "0.9375rem", "1rem"],
                                    line_height="1.7",
                                ),
                                # Show typing cursor when streaming
                                rx.cond(
                                    is_streaming,
                                    rx.box(
                                        class_name="typing-cursor",
                                        display="inline-block",
                                        width="2px",
                                        height="1em",
                                        background=COLORS["primary_green"],
                                        margin_left="2px",
                                        vertical_align="middle",
                                        animation="blink 1s infinite",
                                    ),
                                    rx.fragment(),
                                ),
                                display="flex",
                                align_items="center",
                            ),
                        ),
                        flex="1",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                background=COLORS["white"],
                border=f"1px solid {COLORS['border_light']}",
                border_radius=RADIUS["2xl"],
                padding=["1.125rem 1.375rem", "1.25rem 1.5rem", "1.375rem 1.625rem"],
                max_width=["85%", "75%", "720px"],
                word_wrap="break-word",
                box_shadow="0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.03)",
                transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
                _hover={
                    "box_shadow": "0 4px 16px rgba(0,0,0,0.07), 0 2px 6px rgba(0,0,0,0.04)",
                    "border_color": COLORS["border_gray"],
                    "transform": "translateY(-1px)",
                },
                class_name="message-bubble",
            ),
            # Action icons
            rx.hstack(
                icon_button(icon="copy", on_click=on_copy, tooltip="Kopiëren"),
                icon_button(icon="thumbs-up", on_click=on_like, tooltip="Leuk"),
                icon_button(icon="thumbs-down", on_click=on_dislike, tooltip="Niet leuk"),
                icon_button(icon="bookmark", on_click=on_bookmark, tooltip="Opslaan"),
                icon_button(icon="refresh-cw", on_click=on_refresh, tooltip="Opnieuw genereren"),
                rx.cond(
                    timestamp,
                    rx.text(
                        timestamp,
                        font_size=["0.6875rem", "0.6875rem", "0.75rem"],
                        color=COLORS["text_tertiary"],
                        margin_left="auto",
                        font_weight="500",
                    ),
                    rx.fragment(),
                ),
                spacing="2",
                align="center",
                width="100%",
                flex_wrap="wrap",
                padding_left=["3rem", "3rem", "3rem"],
            ),
            # Follow-up suggestions (contextual) - disabled for now due to Var typing issues
            # TODO: Re-enable with proper Var handling
            # rx.cond(
            #     show_suggestions,
            #     contextual_follow_ups(
            #         last_bot_message=content,
            #         on_suggestion_click=on_suggestion_click,
            #     ),
            #     rx.fragment(),
            # ),
            spacing="2",
            align_items="flex-start",
        ),
        width="100%",
        display="flex",
        justify_content="flex-start",
        margin_bottom=["1.25rem", "1.25rem", "1.5rem"],
        padding_right=["1rem", "1.5rem", "2rem"],
    )


def message_bubble(
    content: str,
    is_user=False,
    timestamp: Optional[str] = None,
    on_copy=None,
    on_like=None,
    on_dislike=None,
    on_bookmark=None,
    on_refresh=None,
    show_suggestions: bool = False,
    on_suggestion_click=None,
    is_thinking: bool = False,
    is_streaming: bool = False,
) -> rx.Component:
    """Message bubble component for chat messages.
    
    Args:
        content: Message text content
        is_user: Whether this is a user message (vs bot message)
        timestamp: Optional timestamp string
        on_copy: Handler for copy action
        on_like: Handler for like action
        on_dislike: Handler for dislike action
        on_bookmark: Handler for bookmark action
        on_refresh: Handler for refresh/regenerate action
        show_suggestions: Whether to show follow-up suggestions (only for bot messages)
        on_suggestion_click: Handler for suggestion click
        is_thinking: Whether the bot is currently thinking (typing indicator)
        is_streaming: Whether the bot is currently streaming response (typing animation)
    """
    return rx.cond(
        is_user,
        user_message(content, timestamp),
        bot_message(content, timestamp, on_copy, on_like, on_dislike, on_bookmark, on_refresh, show_suggestions, on_suggestion_click, is_thinking, is_streaming),
    )

