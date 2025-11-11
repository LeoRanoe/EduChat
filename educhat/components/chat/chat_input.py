"""Chat input component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS
from educhat.components.shared import circular_button, secondary_button


def chat_input(
    value: str = "",
    on_change=None,
    on_submit=None,
    on_prompts_click=None,
    is_loading: bool = False,
    placeholder: str = "Vraag mij van alles!",
    max_chars: int = 2000,
) -> rx.Component:
    """Chat input component with send button and prompts.
    
    Args:
        value: Current input value
        on_change: Handler for input change
        on_submit: Handler for submit/send
        on_prompts_click: Handler for prompts button
        is_loading: Loading state
        placeholder: Placeholder text
        max_chars: Maximum character limit
    """
    return rx.box(
        rx.vstack(
            # Input area
            rx.box(
                rx.hstack(
                    # Text area
                    rx.text_area(
                        placeholder=placeholder,
                        value=value,
                        on_change=on_change,
                        background="transparent",
                        border="none",
                        padding="0",
                        width="100%",
                        min_height="60px",
                        max_height="200px",
                        font_size="1rem",
                        color=COLORS["dark_gray"],
                        resize="none",
                        _focus={
                            "outline": "none",
                        },
                        _placeholder={
                            "color": COLORS["gray"],
                        },
                    ),
                    # Send button
                    rx.box(
                        circular_button(
                            icon="⬆",
                            on_click=on_submit,
                        ),
                        align_self="end",
                    ),
                    spacing="3",
                    align="end",
                    width="100%",
                ),
                background=COLORS["white"],
                border=f"2px solid {COLORS['primary_green']}",
                border_radius=RADIUS["lg"],
                padding="1rem",
                _focus_within={
                    "box_shadow": f"0 0 0 3px rgba(34, 139, 34, 0.1)",
                },
                transition="all 0.2s ease",
            ),
            
            # Bottom row: character count only (removed prompts button)
            rx.hstack(
                rx.text(
                    rx.cond(
                        value,
                        f"{value.length()} / {max_chars}",
                        f"0 / {max_chars}"
                    ),
                    font_size="0.75rem",
                    color=rx.cond(value.length() < max_chars, COLORS["gray"], COLORS["primary_green"]),
                ),
                spacing="3",
                justify="end",
                width="100%",
            ),
            
            # Loading indicator
            rx.cond(
                is_loading,
                rx.hstack(
                    rx.spinner(size="2"),
                    rx.text(
                        "EduChat is aan het typen...",
                        font_size="0.875rem",
                        color=COLORS["gray"],
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.fragment(),
            ),
            
            spacing="2",
            width="100%",
        ),
        width="100%",
        padding="1.5rem",
        background=COLORS["white"],
        border_top=f"1px solid {COLORS['border_gray']}",
    )
