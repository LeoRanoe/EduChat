"""Button components for EduChat."""

import reflex as rx
from typing import Optional, Callable
from educhat.styles.theme import COLORS, RADIUS


def primary_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    is_loading: bool = False,
    width: str = "auto",
) -> rx.Component:
    """Primary button component with green background.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon (emoji or icon name)
        is_loading: Loading state
        width: Button width
    """
    return rx.button(
        rx.hstack(
            rx.cond(
                is_loading,
                rx.spinner(size="3"),
                rx.fragment(),
            ),
            rx.cond(
                icon,
                rx.text(icon, margin_right="0.5rem"),
                rx.fragment(),
            ),
            rx.text(text),
            spacing="2",
            align="center",
        ),
        on_click=on_click,
        background=COLORS["primary_green"],
        color=COLORS["white"],
        border="none",
        border_radius=RADIUS["md"],
        padding="0.75rem 1.5rem",
        cursor="pointer",
        font_weight="500",
        width=width,
        _hover={
            "background": COLORS["dark_green"],
            "transform": "translateY(-1px)",
        },
        transition="all 0.2s ease",
    )


def secondary_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    width: str = "auto",
) -> rx.Component:
    """Secondary button component with white background and border.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon (emoji or icon name)
        width: Button width
    """
    return rx.button(
        rx.hstack(
            rx.cond(
                icon,
                rx.text(icon, margin_right="0.5rem"),
                rx.fragment(),
            ),
            rx.text(text),
            spacing="2",
            align="center",
        ),
        on_click=on_click,
        background=COLORS["white"],
        color=COLORS["dark_gray"],
        border=f"1px solid {COLORS['border_gray']}",
        border_radius=RADIUS["md"],
        padding="0.75rem 1.5rem",
        cursor="pointer",
        font_weight="500",
        width=width,
        _hover={
            "background": COLORS["light_gray"],
            "border_color": COLORS["gray"],
        },
        transition="all 0.2s ease",
    )


def icon_button(
    icon: str,
    on_click: Optional[Callable] = None,
    tooltip: Optional[str] = None,
    color: str = "gray",
) -> rx.Component:
    """Icon-only button component.
    
    Args:
        icon: Icon emoji or character
        on_click: Click handler function
        tooltip: Optional tooltip text
        color: Icon color scheme
    """
    button = rx.button(
        icon,
        on_click=on_click,
        background="transparent",
        color=COLORS[color] if color in COLORS else color,
        border="none",
        border_radius=RADIUS["sm"],
        padding="0.5rem",
        cursor="pointer",
        font_size="1.2rem",
        width="auto",
        height="auto",
        min_width="auto",
        _hover={
            "background": COLORS["light_gray"],
        },
        transition="all 0.2s ease",
    )
    
    if tooltip:
        return rx.tooltip(button, content=tooltip)
    return button


def circular_button(
    icon: str,
    on_click: Optional[Callable] = None,
    background_color: str = "primary_green",
) -> rx.Component:
    """Circular button for send button.
    
    Args:
        icon: Icon emoji or character
        on_click: Click handler function
        background_color: Background color key from COLORS
    """
    return rx.button(
        icon,
        on_click=on_click,
        background=COLORS[background_color],
        color=COLORS["white"],
        border="none",
        border_radius=RADIUS["full"],
        width="40px",
        height="40px",
        padding="0",
        cursor="pointer",
        display="flex",
        align_items="center",
        justify_content="center",
        _hover={
            "background": COLORS["dark_green"],
            "transform": "scale(1.05)",
        },
        transition="all 0.2s ease",
    )
