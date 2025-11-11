"""Error message component with retry functionality."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS


def error_message(
    message: str = "Er is iets misgegaan. Probeer het opnieuw.",
    error_type: str = "generic",
    on_retry=None,
    suggestions: list = None,
) -> rx.Component:
    """Display friendly error message with retry option.
    
    Args:
        message: Error message to display
        error_type: Type of error ('timeout', 'api_error', 'validation', 'generic')
        on_retry: Handler for retry button click
        suggestions: List of suggestion texts for user
    """
    # Error icon based on type
    error_icons = {
        "timeout": "⏱️",
        "api_error": "⚠️",
        "validation": "❓",
        "generic": "⚠️",
    }
    
    icon = error_icons.get(error_type, "⚠️")
    
    # Build suggestions chips if provided
    suggestion_chips = []
    if suggestions:
        for suggestion in suggestions:
            suggestion_chips.append(
                rx.button(
                    suggestion,
                    background=COLORS["white"],
                    color=COLORS["dark_gray"],
                    border=f"1px solid {COLORS['border']}",
                    border_radius=RADIUS["full"],
                    padding="0.5rem 1rem",
                    font_size="0.875rem",
                    cursor="pointer",
                    _hover={
                        "background": COLORS["light_gray"],
                        "border_color": COLORS["primary"],
                    },
                    on_click=lambda: on_retry(suggestion) if on_retry else None,
                )
            )
    
    return rx.box(
        rx.vstack(
            # Error icon
            rx.text(
                icon,
                font_size="3rem",
                line_height="1",
            ),
            
            # Error message
            rx.text(
                message,
                font_size="1rem",
                color=COLORS["dark_gray"],
                text_align="center",
                max_width="400px",
                line_height="1.5",
            ),
            
            # Retry button
            rx.cond(
                on_retry is not None,
                rx.button(
                    rx.hstack(
                        rx.icon(tag="refresh-cw", size=16),
                        rx.text("Probeer opnieuw"),
                        spacing="2",
                        align="center",
                    ),
                    background=COLORS["primary"],
                    color=COLORS["white"],
                    border_radius=RADIUS["md"],
                    padding="0.75rem 1.5rem",
                    font_size="1rem",
                    cursor="pointer",
                    _hover={
                        "background": COLORS["primary_dark"],
                    },
                    on_click=on_retry,
                ),
                rx.fragment(),
            ),
            
            # Suggestion chips
            rx.cond(
                len(suggestion_chips) > 0,
                rx.vstack(
                    rx.text(
                        "Of probeer een van deze vragen:",
                        font_size="0.875rem",
                        color=COLORS["gray"],
                        margin_top="1rem",
                    ),
                    rx.wrap(
                        *suggestion_chips,
                        spacing="2",
                        justify="center",
                    ),
                    spacing="2",
                    align="center",
                ),
                rx.fragment(),
            ),
            
            spacing="4",
            align="center",
            padding="2rem",
        ),
        background=COLORS["white"],
        border=f"1px solid {COLORS['border']}",
        border_radius=RADIUS["lg"],
        max_width="600px",
        margin="2rem auto",
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.1)",
    )


def inline_error_badge(
    message: str = "Fout",
    show_retry: bool = True,
    on_retry=None,
) -> rx.Component:
    """Small inline error badge for message bubbles.
    
    Args:
        message: Short error message
        show_retry: Whether to show retry button
        on_retry: Handler for retry click
    """
    return rx.hstack(
        rx.icon(
            tag="alert-circle",
            size=16,
            color=COLORS["error"],
        ),
        rx.text(
            message,
            font_size="0.875rem",
            color=COLORS["error"],
        ),
        rx.cond(
            show_retry and on_retry is not None,
            rx.button(
                rx.icon(tag="refresh-cw", size=14),
                background="transparent",
                color=COLORS["error"],
                padding="0.25rem",
                cursor="pointer",
                border_radius=RADIUS["sm"],
                _hover={
                    "background": "rgba(239, 68, 68, 0.1)",
                },
                on_click=on_retry,
            ),
            rx.fragment(),
        ),
        spacing="2",
        align="center",
        padding="0.5rem 0.75rem",
        background="rgba(239, 68, 68, 0.1)",
        border_radius=RADIUS["md"],
        border=f"1px solid {COLORS['error']}",
    )
