"""Avatar component for EduChat."""

import reflex as rx
from typing import Optional
from educhat.styles.theme import COLORS, RADIUS


def avatar(
    name: str = "User",
    image_url: Optional[str] = None,
    size: str = "md",
    show_name: bool = False,
) -> rx.Component:
    """User avatar component.
    
    Args:
        name: User name (used for initials if no image)
        image_url: Optional profile image URL
        size: Size variant - "sm", "md", "lg"
        show_name: Whether to show name next to avatar
    """
    size_map = {
        "sm": "32px",
        "md": "40px",
        "lg": "48px"
    }
    
    avatar_size = size_map.get(size, "40px")
    
    # Get first character as initial (simpler approach that works with Reflex Vars)
    # For a full name like "John Doe", we'll just use "J" as initial
    # This avoids .split() which doesn't work with Reflex Vars
    initial = rx.cond(
        name != "",
        name[0].upper(),
        "U"  # Default to "U" for User
    )
    
    avatar_element = rx.cond(
        image_url,
        rx.image(
            src=image_url,
            width=avatar_size,
            height=avatar_size,
            border_radius=RADIUS["full"],
            object_fit="cover",
        ),
        rx.box(
            rx.text(
                initial,
                font_size="0.875rem" if size == "sm" else "1rem",
                font_weight="600",
                color=COLORS["white"],
            ),
            background=COLORS["primary_green"],
            width=avatar_size,
            height=avatar_size,
            border_radius=RADIUS["full"],
            display="flex",
            align_items="center",
            justify_content="center",
        ),
    )
    
    if show_name:
        return rx.hstack(
            avatar_element,
            rx.text(
                name,
                font_size="0.875rem",
                font_weight="500",
                color=COLORS["dark_gray"],
            ),
            spacing="2",
            align="center",
        )
    
    return avatar_element

