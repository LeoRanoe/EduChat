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
            # Input area with modern styling
            rx.box(
                rx.hstack(
                    # Text area with enhanced styling
                    rx.text_area(
                        placeholder=placeholder,
                        value=value,
                        on_change=on_change,
                        background="transparent",
                        border="none",
                        padding="0",
                        width="100%",
                        min_height=["56px", "56px", "64px"],
                        max_height=["180px", "180px", "220px"],
                        font_size=["0.9375rem", "0.9375rem", "1rem"],
                        color=COLORS["text_primary"],
                        resize="none",
                        line_height="1.6",
                        font_weight="400",
                        letter_spacing="-0.01em",
                        _focus={
                            "outline": "none",
                        },
                        _placeholder={
                            "color": COLORS["text_tertiary"],
                            "font_weight": "400",
                        },
                    ),
                    # Enhanced send button
                    rx.box(
                        circular_button(
                            icon="arrow-up",
                            on_click=on_submit,
                        ),
                        align_self="end",
                    ),
                    spacing="4",
                    align="end",
                    width="100%",
                ),
                background=COLORS["white"],
                border=f"2px solid {COLORS['border_gray']}",
                border_radius=RADIUS["2xl"],
                padding=["1.125rem 1.25rem", "1.125rem 1.25rem", "1.25rem 1.5rem"],
                box_shadow="0 2px 8px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04)",
                _focus_within={
                    "box_shadow": f"0 0 0 4px {COLORS['light_green']}, 0 4px 16px rgba(16, 163, 127, 0.15)",
                    "border_color": COLORS["primary_green"],
                },
                transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
            ),
            
            # Bottom row: character count - hidden for now to avoid errors
            rx.box(
                height="0.5rem",  # Placeholder space
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
            
            spacing="3",
            width="100%",
            max_width="900px",
            margin="0 auto",
        ),
        width="100%",
        padding=["1.25rem 1rem", "1.5rem 1.5rem", "2rem"],
        background=COLORS["white"],
        border_top=f"1px solid {COLORS['border_light']}",
        box_shadow="0 -2px 16px rgba(0,0,0,0.04)",
    )
