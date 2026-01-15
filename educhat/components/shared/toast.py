"""Toast notification component for user feedback."""

import reflex as rx
from educhat.styles.theme import COLORS


def toast_notification(message: str, toast_type: str = "success", show: bool = False, on_close=None) -> rx.Component:
    """
    Toast notification component.
    
    Args:
        message: The message to display
        toast_type: Type of toast - "success", "error", "info", "warning"
        show: Whether to show the toast
        on_close: Callback to call when close button is clicked
    """
    
    # Define colors and icons for different toast types
    toast_configs = {
        "success": {
            "bg": "#dcfce7",
            "border": "#86efac",
            "text": "#166534",
            "icon": "check",
        },
        "error": {
            "bg": "#fee2e2",
            "border": "#fecaca",
            "text": "#dc2626",
            "icon": "triangle-alert",
        },
        "info": {
            "bg": "#dbeafe",
            "border": "#93c5fd",
            "text": "#1e40af",
            "icon": "info",
        },
        "warning": {
            "bg": "#fef3c7",
            "border": "#fde047",
            "text": "#92400e",
            "icon": "triangle-alert",
        },
    }
    
    config = toast_configs.get(toast_type, toast_configs["info"])
    
    return rx.cond(
        show,
        rx.box(
            rx.icon(
                tag=config["icon"],
                size=20,
                color=config["text"],
                margin_right="12px",
                flex_shrink="0",
            ),
            rx.text(
                message,
                color=config["text"],
                font_size="14px",
                font_weight="500",
                flex="1",
                line_height="1.5",
            ),
            # Close button
            rx.box(
                rx.icon(
                    tag="x",
                    size=18,
                    color=config["text"],
                ),
                cursor="pointer",
                padding="4px",
                border_radius="4px",
                margin_left="12px",
                flex_shrink="0",
                _hover={
                    "background": f"rgba(0, 0, 0, 0.1)",
                },
                on_click=on_close if on_close else lambda: None,
            ),
            display="flex",
            align_items="center",
            background=config["bg"],
            border=f"1px solid {config['border']}",
            padding="12px 16px",
            border_radius="8px",
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.15)",
            position="fixed",
            top="24px",
            right="24px",
            max_width="400px",
            z_index="9999",
            animation="slideInRight 0.3s ease-out",
            custom_attrs={"data-toast": "true"},
        )
    )


def skeleton_message() -> rx.Component:
    """Skeleton loading message for chat."""
    
    return rx.box(
        rx.box(
            # Avatar skeleton
            rx.box(
                background=COLORS["border"],
                width="32px",
                height="32px",
                border_radius="50%",
                animation="pulse 1.5s ease-in-out infinite",
            ),
            
            # Message content skeleton
            rx.box(
                rx.box(
                    background=COLORS["border"],
                    height="16px",
                    border_radius="4px",
                    margin_bottom="8px",
                    width="80%",
                    animation="pulse 1.5s ease-in-out infinite",
                ),
                rx.box(
                    background=COLORS["border"],
                    height="16px",
                    border_radius="4px",
                    margin_bottom="8px",
                    width="60%",
                    animation="pulse 1.5s ease-in-out infinite 0.2s",
                ),
                rx.box(
                    background=COLORS["border"],
                    height="16px",
                    border_radius="4px",
                    width="70%",
                    animation="pulse 1.5s ease-in-out infinite 0.4s",
                ),
                flex="1",
            ),
            
            display="flex",
            gap="12px",
            padding="16px",
            background="white",
            border_radius="12px",
            max_width="85%",
        ),
        width="100%",
        display="flex",
    )


def skeleton_conversation_list() -> rx.Component:
    """Skeleton loading for conversation list."""
    
    return rx.box(
        skeleton_conversation_item(),
        skeleton_conversation_item(),
        skeleton_conversation_item(),
        skeleton_conversation_item(),
        skeleton_conversation_item(),
        padding="8px",
    )


def skeleton_conversation_item() -> rx.Component:
    """Single skeleton conversation item."""
    
    return rx.box(
        rx.box(
            background=COLORS["border"],
            height="12px",
            border_radius="4px",
            margin_bottom="8px",
            width="70%",
            animation="pulse 1.5s ease-in-out infinite",
        ),
        rx.box(
            background=COLORS["border"],
            height="10px",
            border_radius="4px",
            width="50%",
            animation="pulse 1.5s ease-in-out infinite 0.2s",
        ),
        padding="12px 16px",
        margin_bottom="8px",
        border_radius="8px",
        background="white",
    )
