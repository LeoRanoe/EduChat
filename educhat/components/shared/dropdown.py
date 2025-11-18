"""Dropdown components for EduChat."""

import reflex as rx
from typing import List, Optional, Callable
from educhat.styles.theme import COLORS, RADIUS


def dropdown(
    options: List[str],
    placeholder: str = "Selecteer...",
    value: str = "",
    on_change: Optional[Callable] = None,
    width: str = "100%",
) -> rx.Component:
    """Dropdown/select component.
    
    Args:
        options: List of options
        placeholder: Placeholder text
        value: Selected value
        on_change: Change handler function
        width: Dropdown width
    """
    return rx.select(
        options,
        placeholder=placeholder,
        value=value,
        on_change=on_change,
        background=COLORS["white"],
        border=f"1px solid {COLORS['border_gray']}",
        border_radius=RADIUS["md"],
        padding="0.75rem 1rem",
        width=width,
        font_size="1rem",
        color=COLORS["dark_gray"],
        cursor="pointer",
        _focus={
            "outline": "none",
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 0 0 3px rgba(34, 139, 34, 0.1)",
        },
        transition="all 0.2s ease",
    )

