"""Toast notification component for user feedback.

Professional toast system with:
- Multiple toast types (success, error, warning, info)
- Smooth slide-in animations
- Auto-dismiss with progress indicator
- Accessible with proper ARIA attributes
- Icons for each type
"""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


# Toast configuration for each type
TOAST_CONFIG = {
    "success": {
        "background": COLORS["success_light"],
        "border": COLORS["success"],
        "text": COLORS["success_dark"],
        "icon": "check-circle",
    },
    "error": {
        "background": COLORS["error_light"],
        "border": COLORS["error"],
        "text": COLORS["error_dark"],
        "icon": "x-circle",
    },
    "warning": {
        "background": COLORS["warning_light"],
        "border": COLORS["warning"],
        "text": COLORS["warning_dark"],
        "icon": "alert-triangle",
    },
    "info": {
        "background": COLORS["info_light"],
        "border": COLORS["info"],
        "text": COLORS["info_dark"],
        "icon": "info",
    },
}


def toast_notification(
    message: str,
    toast_type: str = "success",
    show: bool = False,
    on_close=None,
    title: str = "",
    duration: int = 5000,
) -> rx.Component:
    """Toast notification component.
    
    Args:
        message: The message to display
        toast_type: Type of toast - "success", "error", "info", "warning"
        show: Whether to show the toast
        on_close: Callback to call when close button is clicked
        title: Optional title for the toast
        duration: Auto-dismiss duration in ms (0 to disable)
    """
    config = TOAST_CONFIG.get(toast_type, TOAST_CONFIG["info"])
    
    return rx.cond(
        show,
        rx.box(
            # Icon container
            rx.box(
                rx.icon(
                    tag=config["icon"],
                    size=20,
                    color=config["text"],
                ),
                display="flex",
                align_items="center",
                justify_content="center",
                flex_shrink="0",
            ),
            
            # Content
            rx.box(
                rx.cond(
                    title,
                    rx.text(
                        title,
                        font_size="0.9375rem",
                        font_weight="600",
                        color=config["text"],
                        margin_bottom="0.25rem",
                    ),
                    rx.fragment(),
                ),
                rx.text(
                    message,
                    font_size="0.875rem",
                    font_weight="500",
                    color=config["text"],
                    line_height="1.5",
                ),
                flex="1",
                min_width="0",
            ),
            
            # Close button
            rx.box(
                rx.icon(
                    tag="x",
                    size=16,
                    color=config["text"],
                ),
                cursor="pointer",
                padding="0.375rem",
                border_radius=RADIUS["sm"],
                margin_left="0.5rem",
                flex_shrink="0",
                opacity="0.7",
                _hover={
                    "opacity": "1",
                    "background": f"rgba(0, 0, 0, 0.08)",
                },
                on_click=on_close if on_close else lambda: None,
                transition=TRANSITIONS["fast"],
            ),
            
            display="flex",
            align_items="flex-start",
            gap="0.75rem",
            background=config["background"],
            border=f"1px solid {config['border']}",
            border_left=f"4px solid {config['border']}",
            padding="1rem 1.25rem",
            border_radius=RADIUS["lg"],
            box_shadow=SHADOWS["lg"],
            position="fixed",
            top="1.5rem",
            right="1.5rem",
            max_width="400px",
            min_width="300px",
            z_index="9999",
            animation="slideInRight 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
            role="alert",
            aria_live="polite",
        ),
        rx.fragment(),
    )


def inline_alert(
    message: str,
    alert_type: str = "info",
    title: str = "",
    dismissible: bool = False,
    on_dismiss=None,
) -> rx.Component:
    """Inline alert component for contextual messages.
    
    Args:
        message: Alert message
        alert_type: Type - "success", "error", "warning", "info"
        title: Optional title
        dismissible: Show dismiss button
        on_dismiss: Dismiss handler
    """
    config = TOAST_CONFIG.get(alert_type, TOAST_CONFIG["info"])
    
    return rx.box(
        rx.box(
            rx.icon(config["icon"], size=18, color=config["text"]),
            flex_shrink="0",
            margin_top="2px",
        ),
        rx.box(
            rx.cond(
                title,
                rx.text(
                    title,
                    font_size="0.9375rem",
                    font_weight="600",
                    color=config["text"],
                    margin_bottom="0.25rem",
                ),
                rx.fragment(),
            ),
            rx.text(
                message,
                font_size="0.875rem",
                color=config["text"],
                line_height="1.5",
            ),
            flex="1",
        ),
        rx.cond(
            dismissible,
            rx.box(
                rx.icon("x", size=16, color=config["text"]),
                cursor="pointer",
                padding="0.25rem",
                border_radius=RADIUS["sm"],
                opacity="0.7",
                _hover={
                    "opacity": "1",
                    "background": f"rgba(0, 0, 0, 0.08)",
                },
                on_click=on_dismiss,
            ),
            rx.fragment(),
        ),
        display="flex",
        align_items="flex-start",
        gap="0.75rem",
        background=config["background"],
        border=f"1px solid {config['border']}",
        padding="1rem",
        border_radius=RADIUS["lg"],
        width="100%",
    )


# =============================================================================
# SKELETON LOADERS
# =============================================================================

def skeleton_box(
    width: str = "100%",
    height: str = "16px",
    border_radius: str = RADIUS["md"],
) -> rx.Component:
    """Basic skeleton loading box.
    
    Args:
        width: Skeleton width
        height: Skeleton height
        border_radius: Border radius
    """
    return rx.box(
        width=width,
        height=height,
        border_radius=border_radius,
        background=f"linear-gradient(90deg, {COLORS['gray_100']} 0%, {COLORS['gray_50']} 50%, {COLORS['gray_100']} 100%)",
        background_size="200% 100%",
        animation="shimmer 1.5s infinite",
        class_name="skeleton",
    )


def skeleton_message(is_user: bool = False) -> rx.Component:
    """Skeleton loading message for chat.
    
    Args:
        is_user: Whether this is a user message (right-aligned)
    """
    return rx.box(
        rx.box(
            # Avatar skeleton (only for bot)
            rx.cond(
                not is_user,
                skeleton_box(width="40px", height="40px", border_radius=RADIUS["full"]),
                rx.fragment(),
            ),
            
            # Message content skeleton
            rx.box(
                skeleton_box(width="80%", height="16px"),
                skeleton_box(width="60%", height="16px"),
                skeleton_box(width="70%", height="16px"),
                display="flex",
                flex_direction="column",
                gap="0.5rem",
                flex="1",
                padding="1rem",
                background=COLORS["white"],
                border_radius=RADIUS["xl"],
                max_width="70%",
            ),
            
            display="flex",
            gap="0.75rem",
            align_items="flex-start",
        ),
        width="100%",
        display="flex",
        justify_content="flex-end" if is_user else "flex-start",
        padding="0.5rem 0",
    )


def skeleton_conversation_item() -> rx.Component:
    """Single skeleton conversation item."""
    return rx.box(
        rx.box(
            skeleton_box(width="28px", height="28px", border_radius=RADIUS["md"]),
            rx.box(
                skeleton_box(width="70%", height="14px"),
                skeleton_box(width="50%", height="12px"),
                display="flex",
                flex_direction="column",
                gap="0.375rem",
                flex="1",
            ),
            display="flex",
            gap="0.75rem",
            align_items="center",
        ),
        padding="0.75rem",
        border_radius=RADIUS["lg"],
        margin_bottom="0.25rem",
    )


def skeleton_conversation_list(count: int = 5) -> rx.Component:
    """Skeleton loading for conversation list.
    
    Args:
        count: Number of skeleton items
    """
    items = [skeleton_conversation_item() for _ in range(count)]
    return rx.box(
        *items,
        padding="0.5rem",
    )


def skeleton_card() -> rx.Component:
    """Skeleton card for content loading."""
    return rx.box(
        skeleton_box(width="40%", height="20px"),
        skeleton_box(width="100%", height="14px"),
        skeleton_box(width="90%", height="14px"),
        skeleton_box(width="60%", height="14px"),
        display="flex",
        flex_direction="column",
        gap="0.75rem",
        padding="1.5rem",
        background=COLORS["white"],
        border_radius=RADIUS["xl"],
        box_shadow=SHADOWS["sm"],
    )


def loading_spinner(
    size: str = "md",
    color: str = "primary",
    text: str = "",
) -> rx.Component:
    """Loading spinner with optional text.
    
    Args:
        size: Spinner size - "sm", "md", "lg"
        color: Spinner color key
        text: Optional loading text
    """
    size_map = {"sm": "1", "md": "2", "lg": "3"}
    spinner_size = size_map.get(size, "2")
    spinner_color = COLORS.get(color, COLORS["primary"])
    
    return rx.box(
        rx.spinner(size=spinner_size, color=spinner_color),
        rx.cond(
            text,
            rx.text(
                text,
                font_size="0.875rem",
                color=COLORS["text_secondary"],
                margin_left="0.75rem",
            ),
            rx.fragment(),
        ),
        display="flex",
        align_items="center",
        justify_content="center",
    )
