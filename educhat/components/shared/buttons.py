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
    """Modern primary button with gradient background and shadow.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon name from lucide-react icon set
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
                rx.icon(icon, size=18, flex_shrink="0"),
                rx.fragment(),
            ),
            rx.text(
                text, 
                font_size=["0.9375rem", "0.9375rem", "1rem"],
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        on_click=on_click,
        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
        color=COLORS["white"],
        border="none",
        border_radius=RADIUS["2xl"],
        padding=["0.875rem 1.75rem", "0.875rem 1.75rem", "1rem 2rem"],
        cursor="pointer",
        font_weight="600",
        width=width,
        box_shadow="0 4px 12px rgba(16, 163, 127, 0.3), 0 2px 4px rgba(0,0,0,0.1)",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 6px 20px rgba(16, 163, 127, 0.4), 0 3px 6px rgba(0,0,0,0.15)",
        },
        _active={
            "transform": "translateY(0)",
            "box_shadow": "0 2px 8px rgba(16, 163, 127, 0.3), 0 1px 3px rgba(0,0,0,0.1)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
        min_height=["44px", "44px", "48px"],
    )


def secondary_button(
    text: str,
    on_click: Optional[Callable] = None,
    icon: Optional[str] = None,
    width: str = "auto",
) -> rx.Component:
    """Modern secondary button with subtle shadow and better spacing.
    
    Args:
        text: Button text
        on_click: Click handler function
        icon: Optional icon name from lucide-react icon set
        width: Button width
    """
    return rx.button(
        rx.hstack(
            rx.cond(
                icon,
                rx.icon(icon, size=18, flex_shrink="0", color=COLORS["primary_green"]),
                rx.fragment(),
            ),
            rx.text(
                text,
                font_size=["0.875rem", "0.875rem", "0.9375rem"],
                white_space="nowrap",
                overflow="hidden",
                text_overflow="ellipsis",
            ),
            spacing="2",
            align="center",
            width="100%",
        ),
        on_click=on_click,
        background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_green']}15 100%)",
        color=COLORS["dark_gray"],
        border=f"1.5px solid {COLORS['border_gray']}",
        border_radius=RADIUS["xl"],
        padding=["0.75rem 1.5rem", "0.75rem 1.5rem", "0.875rem 1.75rem"],
        cursor="pointer",
        font_weight="500",
        width=width,
        min_height=["44px", "44px", "48px"],
        box_shadow="0 2px 8px rgba(16, 163, 127, 0.08), 0 1px 3px rgba(0,0,0,0.04)",
        _hover={
            "background": f"linear-gradient(135deg, {COLORS['light_green']}30 0%, {COLORS['light_green']}10 100%)",
            "border_color": COLORS["primary_green"],
            "box_shadow": "0 6px 20px rgba(16, 163, 127, 0.15), 0 3px 6px rgba(0,0,0,0.08)",
            "transform": "translateY(-2px)",
        },
        _active={
            "transform": "translateY(0)",
        },
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
    )


def icon_button(
    icon: str,
    on_click: Optional[Callable] = None,
    tooltip: Optional[str] = None,
    color: str = "gray",
) -> rx.Component:
    """Icon-only button component.
    
    Args:
        icon: Icon name from lucide-react icon set
        on_click: Click handler function
        tooltip: Optional tooltip text
        color: Icon color scheme
    """
    button = rx.button(
        rx.icon(icon, size=18),
        on_click=on_click,
        background="transparent",
        color=COLORS[color] if color in COLORS else color,
        border="none",
        border_radius=RADIUS["md"],
        padding=["0.5rem", "0.5rem", "0.625rem"],
        cursor="pointer",
        width="auto",
        height="auto",
        min_width=["36px", "36px", "40px"],
        min_height=["36px", "36px", "40px"],
        display="flex",
        align_items="center",
        justify_content="center",
        _hover={
            "background": COLORS["light_gray"],
            "transform": "scale(1.05)",
        },
        _active={
            "background": COLORS["border_gray"],
            "transform": "scale(0.95)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
    )
    
    if tooltip:
        return rx.tooltip(button, content=tooltip)
    return button


def circular_button(
    icon: str,
    on_click: Optional[Callable] = None,
    background_color: str = "primary_green",
    id: Optional[str] = None,
) -> rx.Component:
    """Modern circular button with gradient for send button.
    
    Args:
        icon: Icon name from lucide-react icon set
        on_click: Click handler function
        background_color: Background color key from COLORS
        id: Optional HTML id attribute
    """
    return rx.button(
        rx.icon(icon, size=18),
        on_click=on_click,
        id=id,
        background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
        color=COLORS["white"],
        border="none",
        border_radius=RADIUS["full"],
        width=["36px", "36px", "40px"],
        height=["36px", "36px", "40px"],
        min_width=["36px", "36px", "40px"],
        min_height=["36px", "36px", "40px"],
        padding="0",
        cursor="pointer",
        display="flex",
        align_items="center",
        justify_content="center",
        flex_shrink="0",
        box_shadow="0 2px 8px rgba(16, 163, 127, 0.3), 0 1px 3px rgba(0,0,0,0.1)",
        _hover={
            "transform": "scale(1.1) translateY(-1px)",
            "box_shadow": "0 4px 12px rgba(16, 163, 127, 0.4), 0 2px 4px rgba(0,0,0,0.15)",
        },
        _active={
            "transform": "scale(0.95)",
        },
        transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
    )

