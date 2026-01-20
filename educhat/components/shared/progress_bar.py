"""Progress bar component for quiz navigation."""
import reflex as rx
from educhat.styles.theme import COLORS


def progress_bar(current_step: rx.Var[int], total_steps: rx.Var[int]) -> rx.Component:
    """
    Progress bar with segments indicating current step.
    
    Args:
        current_step: Current step number (0-indexed)
        total_steps: Total number of steps
    """
    return rx.hstack(
        rx.foreach(
            rx.Var.range(total_steps),
            lambda i: rx.box(
                width="100%",
                height="4px",
                background=rx.cond(
                    i <= current_step,
                    COLORS["primary_green"],
                    COLORS["gray_200"]
                ),
                border_radius="2px",
                transition="background 0.3s ease, transform 0.2s ease",
                _hover={
                    "transform": "scaleY(1.25)",
                },
            )
        ),
        spacing="2",
        width="100%",
        max_width="360px",
    )


def progress_dots(current_step: rx.Var[int], total_steps: rx.Var[int]) -> rx.Component:
    """
    Alternative progress indicator with circular dots.
    
    Args:
        current_step: Current step number (0-indexed)
        total_steps: Total number of steps
    """
    return rx.hstack(
        rx.foreach(
            rx.Var.range(total_steps),
            lambda i: rx.box(
                width="10px",
                height="10px",
                border_radius="50%",
                background=rx.cond(
                    i <= current_step,
                    COLORS["primary_green"],
                    COLORS["border"]
                ),
                transition="background 0.3s ease",
            )
        ),
        spacing="2",
        justify="center",
        width="100%",
    )

