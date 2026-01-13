"""Reminders modal component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS
from educhat.state.auth_state import AuthState


def reminder_item(reminder: dict) -> rx.Component:
    """Single reminder item in the list."""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("bell", size=16, color=COLORS["primary_green"]),
                width="32px",
                height="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                background=f"{COLORS['primary_green']}15",
                border_radius=RADIUS["md"],
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    reminder["title"],
                    font_size="0.875rem",
                    font_weight="600",
                    color=COLORS["text_primary"],
                ),
                rx.text(
                    f"📅 {reminder['date']}",
                    font_size="0.75rem",
                    color=COLORS["text_tertiary"],
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.box(
                rx.icon("trash-2", size=14, color=COLORS["text_tertiary"]),
                on_click=lambda: AuthState.delete_reminder(reminder["id"]),
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={
                    "background": f"{COLORS['error']}10",
                    "color": COLORS["error"],
                },
                transition="all 0.2s ease",
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        padding="0.875rem",
        background=COLORS["white"],
        border=f"1px solid {COLORS['border_light']}",
        border_radius=RADIUS["lg"],
        _hover={
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 2px 8px {COLORS['primary_green']}10",
        },
        transition="all 0.2s ease",
    )


def reminders_modal() -> rx.Component:
    """Modal for viewing and managing reminders."""
    return rx.cond(
        AuthState.show_reminder_modal,
        rx.box(
            # Overlay
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background="rgba(0, 0, 0, 0.5)",
                z_index="1000",
                on_click=AuthState.toggle_reminder_modal,
            ),
            # Modal content
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("bell", size=20, color=COLORS["primary_green"]),
                            rx.text(
                                "Mijn Herinneringen",
                                font_size="1.125rem",
                                font_weight="700",
                                color=COLORS["text_primary"],
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=18, color=COLORS["text_secondary"]),
                            on_click=AuthState.toggle_reminder_modal,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": COLORS["light_gray"],
                            },
                            transition="all 0.2s ease",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    
                    # Add reminder form
                    rx.box(
                        rx.vstack(
                            rx.input(
                                placeholder="Titel (bijv. 'Wiskunde toets')",
                                value=AuthState.reminder_title,
                                on_change=AuthState.set_reminder_title,
                                width="100%",
                                padding="0.75rem",
                                border=f"1px solid {COLORS['border_gray']}",
                                border_radius=RADIUS["md"],
                                font_size="0.875rem",
                                _focus={
                                    "border_color": COLORS["primary_green"],
                                    "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                },
                            ),
                            rx.input(
                                type="date",
                                value=AuthState.reminder_date,
                                on_change=AuthState.set_reminder_date,
                                width="100%",
                                padding="0.75rem",
                                border=f"1px solid {COLORS['border_gray']}",
                                border_radius=RADIUS["md"],
                                font_size="0.875rem",
                                _focus={
                                    "border_color": COLORS["primary_green"],
                                    "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                },
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon("plus", size=16),
                                    rx.text("Herinnering Toevoegen"),
                                    spacing="2",
                                    align="center",
                                ),
                                on_click=AuthState.create_reminder,
                                width="100%",
                                padding="0.75rem",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                color="white",
                                font_weight="600",
                                border_radius=RADIUS["md"],
                                cursor="pointer",
                                _hover={
                                    "transform": "translateY(-1px)",
                                    "box_shadow": f"0 4px 12px {COLORS['primary_green']}40",
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        padding="1rem",
                        background=COLORS["light_gray"],
                        border_radius=RADIUS["lg"],
                        width="100%",
                    ),
                    
                    # Reminders list
                    rx.box(
                        rx.cond(
                            AuthState.reminders.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AuthState.reminders,
                                    reminder_item,
                                ),
                                spacing="2",
                                width="100%",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.icon("bell-off", size=40, color=COLORS["text_tertiary"]),
                                    rx.text(
                                        "Geen herinneringen",
                                        font_size="0.875rem",
                                        color=COLORS["text_secondary"],
                                    ),
                                    rx.text(
                                        "Voeg een herinnering toe voor toetsen, deadlines, etc.",
                                        font_size="0.75rem",
                                        color=COLORS["text_tertiary"],
                                        text_align="center",
                                    ),
                                    spacing="2",
                                    align="center",
                                    padding="2rem",
                                ),
                            ),
                        ),
                        max_height="300px",
                        overflow_y="auto",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width=["90%", "400px", "450px"],
                max_width="90vw",
                max_height="85vh",
                background=COLORS["white"],
                border_radius=RADIUS["xl"],
                padding="1.5rem",
                box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                z_index="1001",
                overflow="hidden",
            ),
        ),
    )
