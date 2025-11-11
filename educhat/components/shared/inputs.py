"""Input components for EduChat."""

import reflex as rx
from typing import Optional, Callable
from educhat.styles.theme import COLORS, RADIUS


def text_input(
    placeholder: str = "",
    value: str = "",
    on_change: Optional[Callable] = None,
    on_blur: Optional[Callable] = None,
    width: str = "100%",
    multiline: bool = False,
) -> rx.Component:
    """Text input component with focus states.
    
    Args:
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler function
        on_blur: Blur handler function
        width: Input width
        multiline: Whether to use textarea
    """
    common_style = {
        "background": COLORS["white"],
        "border": f"1px solid {COLORS['border_gray']}",
        "border_radius": RADIUS["md"],
        "padding": "0.75rem 1rem",
        "width": width,
        "font_size": "1rem",
        "color": COLORS["dark_gray"],
        "_focus": {
            "outline": "none",
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 0 0 3px rgba(34, 139, 34, 0.1)",
        },
        "_placeholder": {
            "color": COLORS["gray"],
        },
        "transition": "all 0.2s ease",
    }
    
    if multiline:
        return rx.text_area(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            on_blur=on_blur,
            rows="3",
            resize="vertical",
            **common_style,
        )
    else:
        return rx.input(
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            on_blur=on_blur,
            **common_style,
        )


def search_input(
    placeholder: str = "Zoeken...",
    value: str = "",
    on_change: Optional[Callable] = None,
    width: str = "100%",
) -> rx.Component:
    """Search input with search icon.
    
    Args:
        placeholder: Placeholder text
        value: Input value
        on_change: Change handler function
        width: Input width
    """
    return rx.box(
        rx.hstack(
            rx.text("🔍", font_size="1.2rem", color=COLORS["gray"]),
            rx.input(
                placeholder=placeholder,
                value=value,
                on_change=on_change,
                background="transparent",
                border="none",
                padding="0",
                width="100%",
                font_size="1rem",
                color=COLORS["dark_gray"],
                _focus={
                    "outline": "none",
                },
                _placeholder={
                    "color": COLORS["gray"],
                },
            ),
            spacing="2",
            align="center",
        ),
        background=COLORS["light_gray"],
        border=f"1px solid {COLORS['border_gray']}",
        border_radius=RADIUS["md"],
        padding="0.75rem 1rem",
        width=width,
        _focus_within={
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 0 0 3px rgba(34, 139, 34, 0.1)",
        },
        transition="all 0.2s ease",
    )
