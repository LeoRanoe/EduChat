"""Reminders modal component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, T
from educhat.state.auth_state import AuthState
from educhat.components.shared.sync_status import sync_status_badge


def reminder_item(reminder: dict) -> rx.Component:
    """Single reminder item in the list."""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("bell", size=16, color=COLORS["primary_green"]),
                width="36px",
                height="36px",
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
                    font_size="0.9375rem",
                    font_weight="600",
                    color=T.text_primary,
                    line_height="1.4",
                ),
                rx.text(
                    rx.cond(
                        reminder.get("time", "") != "",
                        f"📅 {reminder['date']} om {reminder.get('time', '')}",
                        f"📅 {reminder['date']}",
                    ),
                    font_size="0.8125rem",
                    color=T.text_tertiary,
                    line_height="1.4",
                ),
                # Show description if exists
                rx.cond(
                    reminder.get("description", "") != "",
                    rx.text(
                        reminder.get("description", ""),
                        font_size="0.8125rem",
                        color=T.text_tertiary,
                        line_height="1.4",
                        max_width="400px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    rx.fragment(),
                ),
                # Show location if exists
                rx.cond(
                    reminder.get("location", "") != "",
                    rx.text(
                        f"📍 {reminder.get('location', '')}",
                        font_size="0.8125rem",
                        color=T.text_tertiary,
                        line_height="1.4",
                    ),
                    rx.fragment(),
                ),
                # Sync status badge
                sync_status_badge(
                    status=reminder.get("sync_status", "pending"),
                    last_sync_time=reminder.get("last_sync_time", ""),
                    error_message=reminder.get("sync_error", ""),
                    google_link=reminder.get("google_link", ""),
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.box(
                rx.icon("trash-2", size=16, color=T.text_tertiary),
                on_click=lambda: AuthState.delete_reminder(reminder["id"]),
                cursor="pointer",
                padding="0.625rem",
                border_radius=RADIUS["sm"],
                _hover={
                    "background": T.error_light,
                    "color": T.error,
                },
                transition="all 0.2s ease",
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        padding="1rem",
        min_height="60px",
        background=T.bg_card,
        border=f"1px solid {T.border_light}",
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
                background=T.overlay,
                z_index="1000",
                on_click=AuthState.toggle_reminder_modal,
            ),
            # Modal content
            rx.box(
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
                                color=T.text_primary,
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=18, color=T.text_secondary),
                            on_click=AuthState.toggle_reminder_modal,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": T.bg_hover,
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
                                padding="0.875rem 1rem",
                                min_height="48px",
                                background=rx.color_mode_cond(light="#FFFFFF", dark="#1a1d24"),
                                color=rx.color_mode_cond(light="#000000", dark="#E5E7EB"),
                                border=f"1px solid {T.border}",
                                border_radius=RADIUS["md"],
                                font_size="0.9375rem",
                                line_height="1.5",
                                _focus={
                                    "border_color": COLORS["primary_green"],
                                    "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                },
                            ),
                            rx.hstack(
                                rx.input(
                                    type="date",
                                    value=AuthState.reminder_date,
                                    on_change=AuthState.set_reminder_date,
                                    width="100%",
                                    padding="0.875rem 1rem",
                                    min_height="48px",
                                    background=rx.color_mode_cond(light="#FFFFFF", dark="#1a1d24"),
                                    color=rx.color_mode_cond(light="#000000", dark="#E5E7EB"),
                                    border=f"1px solid {T.border}",
                                    border_radius=RADIUS["md"],
                                    font_size="0.9375rem",
                                    line_height="1.5",
                                    _focus={
                                        "border_color": COLORS["primary_green"],
                                        "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                    },
                                ),
                                rx.input(
                                    type="time",
                                    value=AuthState.reminder_time,
                                    on_change=AuthState.set_reminder_time,
                                    width="140px",
                                    padding="0.875rem 1rem",
                                    min_height="48px",
                                    background=rx.color_mode_cond(light="#FFFFFF", dark="#1a1d24"),
                                    color=rx.color_mode_cond(light="#000000", dark="#E5E7EB"),
                                    border=f"1px solid {T.border}",
                                    border_radius=RADIUS["md"],
                                    font_size="0.9375rem",
                                    line_height="1.5",
                                    _focus={
                                        "border_color": COLORS["primary_green"],
                                        "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                    },
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            rx.text_area(
                                placeholder="Beschrijving (optioneel)",
                                value=AuthState.reminder_description,
                                on_change=AuthState.set_reminder_description,
                                width="100%",
                                min_height="80px",
                                padding="0.875rem 1rem",
                                background=rx.color_mode_cond(light="#FFFFFF", dark="#1a1d24"),
                                color=rx.color_mode_cond(light="#000000", dark="#E5E7EB"),
                                border=f"1px solid {T.border}",
                                border_radius=RADIUS["md"],
                                font_size="0.9375rem",
                                line_height="1.5",
                                resize="vertical",
                                _focus={
                                    "border_color": COLORS["primary_green"],
                                    "box_shadow": f"0 0 0 3px {COLORS['primary_green']}15",
                                },
                            ),
                            rx.input(
                                placeholder="Locatie (optioneel)",
                                value=AuthState.reminder_location,
                                on_change=AuthState.set_reminder_location,
                                width="100%",
                                padding="0.875rem 1rem",
                                min_height="48px",
                                background=rx.color_mode_cond(light="#FFFFFF", dark="#1a1d24"),
                                color=rx.color_mode_cond(light="#000000", dark="#E5E7EB"),
                                border=f"1px solid {T.border}",
                                border_radius=RADIUS["md"],
                                font_size="0.9375rem",
                                line_height="1.5",
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
                                padding="0.875rem",
                                min_height="48px",
                                background=f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                                color=T.text_on_primary,
                                font_weight="600",
                                border_radius=RADIUS["md"],
                                cursor="pointer",
                                _hover={
                                    "transform": "translateY(-1px)",
                                    "box_shadow": T.shadow_md,
                                },
                                transition="all 0.2s ease",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        padding="1rem",
                        background=T.bg_tertiary,
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
                                    rx.icon("bell-off", size=40, color=T.text_tertiary),
                                    rx.text(
                                        "Geen herinneringen",
                                        font_size="0.875rem",
                                        color=T.text_secondary,
                                    ),
                                    rx.text(
                                        "Voeg een herinnering toe voor toetsen, deadlines, etc.",
                                        font_size="0.75rem",
                                        color=T.text_tertiary,
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
                background=rx.color_mode_cond(
                    light="#FFFFFF",
                    dark="#111217"
                ),
                border=rx.color_mode_cond(
                    light="1px solid #E5E7EB",
                    dark="1px solid #2d3039"
                ),
                width="100%",
                height="100%",
                border_radius=RADIUS["xl"],
                padding="1.5rem",
                position="relative",
                z_index="2",
            ),
            position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width=["90%", "400px", "450px"],
                max_width="90vw",
                max_height="85vh",
                class_name="reminder-modal",
                border_radius=RADIUS["xl"],
                box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                z_index="1001",
                overflow="hidden",
            ),
        ),
    )
