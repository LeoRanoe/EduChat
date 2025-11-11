"""Logo component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS


def logo(size: str = "md") -> rx.Component:
    """EduChat logo component with graduation cap and chat bubble.
    
    Args:
        size: Size variant - "sm", "md", "lg"
    """
    size_map = {
        "sm": "24px",
        "md": "32px",
        "lg": "48px"
    }
    
    icon_size = size_map.get(size, "32px")
    
    return rx.hstack(
        # Graduation cap icon (using emoji for simplicity)
        rx.text(
            "🎓",
            font_size=icon_size,
        ),
        rx.text(
            "EduChat",
            font_size=icon_size,
            font_weight="700",
            color=COLORS["primary_green"],
        ),
        spacing="2",
        align="center",
    )
