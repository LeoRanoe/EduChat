"""Logo component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS


def logo(size: str = "md") -> rx.Component:
    """EduChat logo component with graduation cap icon.
    
    Args:
        size: Size variant - "sm", "md", "lg"
    """
    size_config = {
        "sm": {
            "icon": 20,
            "text": "1.125rem",
            "spacing": "2"
        },
        "md": {
            "icon": 28,
            "text": "1.5rem",
            "spacing": "2"
        },
        "lg": {
            "icon": 48,
            "text": "2.25rem",
            "spacing": "3"
        }
    }
    
    config = size_config.get(size, size_config["md"])
    
    return rx.hstack(
        # Graduation cap icon
        rx.icon(
            "graduation-cap",
            size=config["icon"],
            color=COLORS["primary_green"],
        ),
        rx.text(
            "EduChat",
            font_size=config["text"],
            font_weight="700",
            color=COLORS["primary_green"],
            line_height="1",
        ),
        spacing=config["spacing"],
        align="center",
    )

