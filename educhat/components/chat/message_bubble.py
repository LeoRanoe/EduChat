"""Message bubble component for EduChat.

Professional, accessible message bubbles with:
- Smooth animations and micro-interactions
- Copy feedback with visual confirmation
- Proper timestamp formatting
- Action buttons with hover states
- Thinking/streaming indicators
"""

import reflex as rx
from typing import Optional
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


# ============================================================================
# MESSAGE STYLES CONFIGURATION
# ============================================================================

MESSAGE_STYLES = {
    "user": {
        "background": f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
        "color": COLORS["white"],
        "border_radius": "20px 20px 4px 20px",
        "shadow": "0 2px 12px rgba(16, 163, 127, 0.25), 0 1px 4px rgba(0,0,0,0.08)",
        "shadow_hover": "0 4px 16px rgba(16, 163, 127, 0.3), 0 2px 6px rgba(0,0,0,0.1)",
    },
    "bot": {
        "background": COLORS["white"],
        "color": COLORS["text_primary"],
        "border_radius": "20px 20px 20px 4px",
        "shadow": SHADOWS["sm"],
        "shadow_hover": SHADOWS["md"],
    },
}

ACTION_BUTTON_STYLES = {
    "base": {
        "width": "32px",
        "height": "32px",
        "border_radius": RADIUS["md"],
        "background": "transparent",
        "cursor": "pointer",
        "transition": TRANSITIONS["fast"],
        "display": "flex",
        "align_items": "center",
        "justify_content": "center",
    },
    "hover": {
        "background": COLORS["light_gray"],
    },
}


# ============================================================================
# ACTION BUTTON COMPONENT
# ============================================================================

def message_action_button(
    icon: str,
    on_click=None,
    tooltip: str = "",
    is_active: bool = False,
    variant: str = "default",  # default, success, danger
) -> rx.Component:
    """Compact action button for message actions.
    
    Args:
        icon: Lucide icon name
        on_click: Click handler
        tooltip: Tooltip text
        is_active: Whether button is in active state
        variant: Color variant (default, success, danger)
    """
    variant_colors = {
        "default": {"color": COLORS["text_tertiary"], "hover_bg": COLORS["light_gray"]},
        "success": {"color": COLORS["success"], "hover_bg": f"rgba(34, 197, 94, 0.1)"},
        "danger": {"color": COLORS["error"], "hover_bg": f"rgba(239, 68, 68, 0.1)"},
    }
    
    colors = variant_colors.get(variant, variant_colors["default"])
    
    return rx.tooltip(
        rx.box(
            rx.icon(
                icon,
                size=14,
                color=colors["color"] if is_active else COLORS["text_tertiary"],
            ),
            width="28px",
            height="28px",
            display="flex",
            align_items="center",
            justify_content="center",
            border_radius=RADIUS["md"],
            background="transparent",
            cursor="pointer",
            on_click=on_click,
            transition=TRANSITIONS["fast"],
            _hover={
                "background": colors["hover_bg"],
                "transform": "scale(1.05)",
            },
            class_name="message-action-btn",
        ),
        content=tooltip,
    )


# ============================================================================
# USER MESSAGE COMPONENT
# ============================================================================

def user_message(content: str, timestamp: Optional[str] = None) -> rx.Component:
    """User message bubble - right-aligned with gradient background.
    
    Features:
    - Smooth entrance animation
    - Gradient background
    - Subtle hover lift effect
    - Timestamp display
    """
    return rx.box(
        rx.vstack(
            # Message bubble
            rx.box(
                rx.text(
                    content,
                    font_size=["0.9375rem", "0.9375rem", "1rem"],
                    color=MESSAGE_STYLES["user"]["color"],
                    line_height="1.7",
                    font_weight="400",
                    letter_spacing="0.01em",
                    white_space="pre-wrap",
                ),
                background=MESSAGE_STYLES["user"]["background"],
                border_radius=MESSAGE_STYLES["user"]["border_radius"],
                padding=["0.875rem 1.125rem", "1rem 1.25rem", "1.125rem 1.375rem"],
                max_width=["85%", "75%", "600px"],
                word_wrap="break-word",
                box_shadow=MESSAGE_STYLES["user"]["shadow"],
                transition=f"all {TRANSITIONS['normal']}",
                _hover={
                    "transform": "translateY(-1px)",
                    "box_shadow": MESSAGE_STYLES["user"]["shadow_hover"],
                },
                class_name="message-bubble user-message animate-fadeInUp",
            ),
            # Timestamp
            rx.cond(
                timestamp,
                rx.hstack(
                    rx.icon("check-check", size=12, color=COLORS["text_tertiary"]),
                    rx.text(
                        timestamp,
                        font_size="0.6875rem",
                        color=COLORS["text_tertiary"],
                        font_weight="500",
                    ),
                    spacing="1",
                    align="center",
                    opacity="0.8",
                ),
                rx.fragment(),
            ),
            spacing="2",
            align_items="flex-end",
        ),
        width="100%",
        display="flex",
        justify_content="flex-end",
        margin_bottom=["1rem", "1rem", "1.25rem"],
        padding_left=["2rem", "3rem", "4rem"],
        animation="fadeInUp 0.3s ease-out",
    )


# ============================================================================
# THINKING INDICATOR COMPONENT
# ============================================================================

def thinking_indicator() -> rx.Component:
    """Animated thinking indicator with bouncing dots."""
    return rx.hstack(
        rx.box(
            width="8px",
            height="8px",
            border_radius="50%",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            animation="typingDot 1.4s infinite ease-in-out",
            box_shadow="0 2px 6px rgba(16, 163, 127, 0.25)",
        ),
        rx.box(
            width="8px",
            height="8px",
            border_radius="50%",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            animation="typingDot 1.4s infinite ease-in-out 0.2s",
            box_shadow="0 2px 6px rgba(16, 163, 127, 0.25)",
        ),
        rx.box(
            width="8px",
            height="8px",
            border_radius="50%",
            background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
            animation="typingDot 1.4s infinite ease-in-out 0.4s",
            box_shadow="0 2px 6px rgba(16, 163, 127, 0.25)",
        ),
        spacing="2",
        align="center",
        padding="0.75rem 0",
    )


# ============================================================================
# BOT MESSAGE COMPONENT
# ============================================================================

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
    """Bot message bubble - left-aligned with card style.
    
    Features:
    - Avatar with gradient background
    - Markdown rendering
    - Action buttons (copy, like, dislike, bookmark, refresh)
    - Thinking/streaming indicators
    - Smooth animations
    """
    from educhat.components.shared import contextual_follow_ups
    
    return rx.box(
        rx.vstack(
            # Main message card
            rx.box(
                rx.hstack(
                    # Bot Avatar
                    rx.box(
                        rx.icon(
                            "graduation-cap",
                            size=18,
                            color=COLORS["primary_green"],
                        ),
                        width="36px",
                        height="36px",
                        min_width="36px",
                        display="flex",
                        align_items="center",
                        justify_content="center",
                        background=f"linear-gradient(135deg, {COLORS['light_green']} 0%, rgba(16, 163, 127, 0.15) 100%)",
                        border_radius=RADIUS["full"],
                        border=f"1.5px solid rgba(16, 163, 127, 0.2)",
                        flex_shrink="0",
                    ),
                    # Message content
                    rx.box(
                        rx.cond(
                            is_thinking,
                            thinking_indicator(),
                            # Normal markdown content with optional typing cursor
                            rx.box(
                                rx.markdown(
                                    content,
                                    class_name="bot-message-content",
                                ),
                                # Show typing cursor when streaming
                                rx.cond(
                                    is_streaming,
                                    rx.box(
                                        display="inline-block",
                                        width="2px",
                                        height="1.2em",
                                        background=COLORS["primary_green"],
                                        margin_left="2px",
                                        vertical_align="text-bottom",
                                        animation="blink 1s infinite",
                                        border_radius="1px",
                                    ),
                                    rx.fragment(),
                                ),
                            ),
                        ),
                        flex="1",
                        min_width="0",
                        color=MESSAGE_STYLES["bot"]["color"],
                        font_size=["0.9375rem", "0.9375rem", "1rem"],
                        line_height="1.7",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                background=MESSAGE_STYLES["bot"]["background"],
                border=f"1px solid {COLORS['border_light']}",
                border_radius=MESSAGE_STYLES["bot"]["border_radius"],
                padding=["1rem 1.125rem", "1.125rem 1.25rem", "1.25rem 1.375rem"],
                max_width=["85%", "75%", "700px"],
                word_wrap="break-word",
                box_shadow=MESSAGE_STYLES["bot"]["shadow"],
                transition=f"all {TRANSITIONS['normal']}",
                _hover={
                    "box_shadow": MESSAGE_STYLES["bot"]["shadow_hover"],
                    "border_color": COLORS["border_gray"],
                },
                class_name="message-bubble bot-message animate-fadeInUp",
            ),
            # Action bar
            rx.hstack(
                # Action buttons
                rx.hstack(
                    message_action_button(icon="copy", on_click=on_copy, tooltip="Kopiëren"),
                    message_action_button(icon="thumbs-up", on_click=on_like, tooltip="Nuttig"),
                    message_action_button(icon="thumbs-down", on_click=on_dislike, tooltip="Niet nuttig"),
                    message_action_button(icon="bookmark", on_click=on_bookmark, tooltip="Opslaan"),
                    message_action_button(icon="refresh-cw", on_click=on_refresh, tooltip="Opnieuw genereren"),
                    spacing="1",
                    align="center",
                    opacity="0.6",
                    transition=TRANSITIONS["fast"],
                    _group_hover={"opacity": "1"},
                    class_name="message-actions",
                ),
                # Timestamp
                rx.cond(
                    timestamp,
                    rx.text(
                        timestamp,
                        font_size="0.6875rem",
                        color=COLORS["text_tertiary"],
                        margin_left="auto",
                        font_weight="500",
                    ),
                    rx.fragment(),
                ),
                spacing="2",
                align="center",
                width="100%",
                padding_left="3rem",
                margin_top="0.375rem",
            ),
            spacing="1",
            align_items="flex-start",
            role="group",
        ),
        width="100%",
        display="flex",
        justify_content="flex-start",
        margin_bottom=["1rem", "1rem", "1.25rem"],
        padding_right=["2rem", "3rem", "4rem"],
        animation="fadeInUp 0.3s ease-out",
    )


# ============================================================================
# MAIN MESSAGE BUBBLE COMPONENT
# ============================================================================
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
    
    A unified component that renders either user or bot messages based on the
    is_user flag. Provides consistent styling, animations, and interaction
    patterns for both message types.
    
    Args:
        content: Message text content (supports markdown for bot messages)
        is_user: Whether this is a user message (vs bot message)
        timestamp: Optional timestamp string (e.g., "2:30 PM")
        on_copy: Handler for copy action (bot messages only)
        on_like: Handler for like action (bot messages only)
        on_dislike: Handler for dislike action (bot messages only)
        on_bookmark: Handler for bookmark action (bot messages only)
        on_refresh: Handler for refresh/regenerate action (bot messages only)
        show_suggestions: Whether to show follow-up suggestions (bot messages only)
        on_suggestion_click: Handler for suggestion click
        is_thinking: Show thinking indicator (bot messages only)
        is_streaming: Show streaming cursor (bot messages only)
    
    Returns:
        A Reflex component rendering the appropriate message bubble.
    """
    return rx.cond(
        is_user,
        user_message(content, timestamp),
        bot_message(
            content,
            timestamp,
            on_copy,
            on_like,
            on_dislike,
            on_bookmark,
            on_refresh,
            show_suggestions,
            on_suggestion_click,
            is_thinking,
            is_streaming,
        ),
    )

