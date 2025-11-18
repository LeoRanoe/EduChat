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
        rx.box(
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
                            border="none !important",
                            outline="none !important",
                            box_shadow="none !important",
                            padding="0",
                            width="100%",
                            min_height="24px",
                            max_height=["120px", "160px", "200px"],
                            font_size=["0.9375rem", "0.9375rem", "1rem"],
                            color=COLORS["text_primary"],
                            resize="none",
                            line_height="1.5",
                            font_weight="400",
                            letter_spacing="-0.01em",
                            overflow="auto",
                            id="chat-textarea",
                            _focus={
                                "outline": "none",
                                "border": "none",
                                "box_shadow": "none",
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
                                id="send-button",
                            ),
                            align_self="end",
                            flex_shrink="0",
                        ),
                        spacing="3",
                        align="end",
                        width="100%",
                    ),
                    background=f"linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_gray']}20 100%)",
                    border=f"2px solid {COLORS['border_gray']}",
                    border_radius=RADIUS["2xl"],
                    padding=["0.75rem 1rem", "0.75rem 1rem", "0.875rem 1.125rem"],
                    box_shadow="0 2px 12px rgba(0,0,0,0.05), 0 1px 4px rgba(0,0,0,0.03)",
                    _focus_within={
                        "box_shadow": f"0 0 0 3px {COLORS['light_green']}, 0 8px 24px rgba(16, 163, 127, 0.15), 0 4px 8px rgba(0,0,0,0.08)",
                        "border_color": COLORS["primary_green"],
                        "background": COLORS["white"],
                        "transform": "translateY(-1px)",
                    },
                    transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                    width="100%",
                ),
                
                spacing="3",
                width="100%",
            ),
            width="100%",
            max_width="900px",
            margin="0 auto",
            padding_left="0",
            padding_right="0",
        ),
        width="100%",
        padding=["0.875rem 1rem", "1rem 1.5rem", "1.125rem 2rem"],
        display="flex",
        justify_content="center",
        align_items="center",
        background=COLORS["white"],
        border_top=f"1px solid {COLORS['border_light']}",
        box_shadow="0 -2px 12px rgba(0,0,0,0.04)",
        flex_shrink="0",
    )


