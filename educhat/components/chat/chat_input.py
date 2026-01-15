"""Chat input component for EduChat.

Professional chat input with:
- Auto-expanding textarea
- Character counter
- Loading state indicator
- Keyboard shortcuts
- Accessibility features
"""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, SHADOWS, TRANSITIONS


def chat_input(
    value: str = "",
    on_change=None,
    on_submit=None,
    on_prompts_click=None,
    is_loading: bool = False,
    placeholder: str = "Vraag mij van alles over onderwijs...",
    max_chars: int = 2000,
) -> rx.Component:
    """Professional chat input component with send button.
    
    Features:
    - Auto-expanding textarea
    - Character counter (shows when > 80% full)
    - Loading state with disabled send
    - Smooth focus states and transitions
    - Accessible labels and keyboard support
    
    Args:
        value: Current input value
        on_change: Handler for input change
        on_submit: Handler for submit/send
        on_prompts_click: Handler for prompts button
        is_loading: Loading state (disables input and shows spinner)
        placeholder: Placeholder text
        max_chars: Maximum character limit
    """
    # Calculate if we should show the character counter
    char_count_visible = f"(({value}.length() / {max_chars}) > 0.8)"
    
    return rx.box(
        rx.box(
            rx.vstack(
                # Main input container
                rx.box(
                    rx.hstack(
                        # Text area
                        rx.el.textarea(
                            placeholder=placeholder,
                            value=value,
                            on_change=on_change,
                            disabled=is_loading,
                            max_length=max_chars,
                            rows=1,
                            id="chat-textarea",
                            aria_label="Typ je bericht",
                            style={
                                "width": "100%",
                                "min_height": "24px",
                                "max_height": "150px",
                                "padding": "0",
                                "border": "none",
                                "outline": "none",
                                "background": "transparent",
                                "resize": "none",
                                "font_size": "0.9375rem",
                                "font_family": "inherit",
                                "line_height": "1.6",
                                "color": COLORS["text_primary"],
                                "overflow_y": "auto",
                            },
                            class_name="chat-textarea",
                        ),
                        # Send button
                        rx.box(
                            rx.cond(
                                is_loading,
                                # Loading spinner
                                rx.box(
                                    rx.icon("loader-2", size=18, color="white"),
                                    width="40px",
                                    height="40px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    background=COLORS["text_tertiary"],
                                    border_radius=RADIUS["full"],
                                    animation="spin 1s linear infinite",
                                ),
                                # Send button
                                rx.box(
                                    rx.icon("arrow-up", size=18, color="white"),
                                    width="40px",
                                    height="40px",
                                    display="flex",
                                    align_items="center",
                                    justify_content="center",
                                    background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                    border_radius=RADIUS["full"],
                                    cursor="pointer",
                                    on_click=on_submit,
                                    box_shadow=SHADOWS["primary_sm"],
                                    transition=TRANSITIONS["fast"],
                                    _hover={
                                        "transform": "scale(1.05)",
                                        "box_shadow": SHADOWS["primary_md"],
                                    },
                                    _active={
                                        "transform": "scale(0.95)",
                                    },
                                    aria_label="Verstuur bericht",
                                ),
                            ),
                            align_self="flex-end",
                            flex_shrink="0",
                        ),
                        spacing="3",
                        align="end",
                        width="100%",
                    ),
                    background=COLORS["white"],
                    border=f"2px solid {COLORS['border_gray']}",
                    border_radius="24px",
                    padding=["0.75rem 0.875rem 0.75rem 1rem", "0.75rem 1rem 0.75rem 1.125rem", "0.875rem 1rem 0.875rem 1.25rem"],
                    box_shadow=SHADOWS["sm"],
                    transition=f"all {TRANSITIONS['normal']}",
                    _focus_within={
                        "border_color": COLORS["primary_green"],
                        "box_shadow": f"0 0 0 3px rgba(16, 163, 127, 0.15), {SHADOWS['md']}",
                    },
                    width="100%",
                    position="relative",
                ),
                
                # Bottom row: hint text and character counter
                rx.hstack(
                    # Keyboard hint (desktop only)
                    rx.text(
                        "Enter om te versturen",
                        font_size="0.6875rem",
                        color=COLORS["text_tertiary"],
                        display=["none", "none", "block"],
                    ),
                    rx.spacer(),
                    # Character counter (shows when approaching limit)
                    rx.text(
                        rx.fragment(value.length(), " / ", max_chars),
                        font_size="0.6875rem",
                        color=rx.cond(
                            value.length() > (max_chars * 0.9),
                            COLORS["error"],
                            COLORS["text_tertiary"]
                        ),
                        font_weight=rx.cond(
                            value.length() > (max_chars * 0.9),
                            "600",
                            "400"
                        ),
                        opacity=rx.cond(
                            value.length() > (max_chars * 0.7),
                            "1",
                            "0"
                        ),
                        transition=TRANSITIONS["fast"],
                    ),
                    width="100%",
                    padding_x="0.5rem",
                ),
                
                spacing="2",
                width="100%",
            ),
            width="100%",
            max_width="800px",
            margin="0 auto",
        ),
        # Container styling
        width="100%",
        padding=["0.75rem 1rem", "1rem 1.5rem", "1.25rem 2rem"],
        background=f"linear-gradient(to top, {COLORS['white']} 0%, {COLORS['background']} 100%)",
        border_top=f"1px solid {COLORS['border_light']}",
        flex_shrink="0",
    )


