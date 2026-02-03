"""Google Events Import Modal for EduChat.

UI for selecting which Google Calendar events to import as reminders.
"""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, T
from educhat.state.auth_state import AuthState


def google_event_checkbox(event: dict) -> rx.Component:
    """Checkbox item for a Google Calendar event.
    
    Args:
        event: Event dict with title, date, description
        
    Returns:
        Checkbox component
    """
    return rx.box(
        rx.hstack(
            rx.checkbox(
                value=event.get("id", ""),
                on_change=lambda checked: AuthState.toggle_google_event_selection(event.get("id", "")),
            ),
            rx.vstack(
                rx.text(
                    event.get("title", "Untitled Event"),
                    font_size="0.9375rem",
                    font_weight="600",
                    color=T.text_primary,
                ),
                rx.text(
                    f"📅 {event.get('date', '')}",
                    font_size="0.8125rem",
                    color=T.text_secondary,
                ),
                rx.cond(
                    event.get("description", "") != "",
                    rx.text(
                        event.get("description", ""),
                        font_size="0.75rem",
                        color=T.text_tertiary,
                        max_width="300px",
                        overflow="hidden",
                        text_overflow="ellipsis",
                        white_space="nowrap",
                    ),
                    rx.fragment(),
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        padding="0.75rem",
        border=f"1px solid {T.border_light}",
        border_radius=RADIUS["md"],
        _hover={
            "background": T.bg_hover,
            "border_color": COLORS["primary_green"],
        },
        cursor="pointer",
        transition="all 0.2s ease",
    )


def google_events_import_modal() -> rx.Component:
    """Modal for importing Google Calendar events as reminders."""
    return rx.cond(
        AuthState.show_google_events_modal,
        rx.box(
            # Overlay
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background=T.overlay,
                z_index="1200",
                on_click=AuthState.close_google_events_modal,
            ),
            # Modal content
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("calendar-plus", size=24, color=COLORS["primary_green"]),
                            rx.vstack(
                                rx.text(
                                    "Nieuwe Google Calendar Evenementen",
                                    font_size="1.125rem",
                                    font_weight="700",
                                    color=T.text_primary,
                                ),
                                rx.text(
                                    f"{AuthState.new_google_events.length()} nieuwe evenementen gevonden",
                                    font_size="0.8125rem",
                                    color=T.text_secondary,
                                ),
                                spacing="1",
                                align_items="start",
                            ),
                            spacing="3",
                            align="start",
                        ),
                        rx.box(
                            rx.icon("x", size=20, color=T.text_secondary),
                            on_click=AuthState.close_google_events_modal,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={"background": T.bg_hover},
                        ),
                        justify="between",
                        width="100%",
                        align="start",
                    ),
                    
                    # Info box
                    rx.box(
                        rx.hstack(
                            rx.icon("info", size=16, color=COLORS["primary_green"]),
                            rx.text(
                                "Selecteer evenementen om herinneringen voor aan te maken in EduChat",
                                font_size="0.8125rem",
                                color=T.text_secondary,
                            ),
                            spacing="2",
                            align="center",
                        ),
                        padding="0.75rem",
                        background=f"{COLORS['primary_green']}10",
                        border=f"1px solid {COLORS['primary_green']}30",
                        border_radius=RADIUS["md"],
                        width="100%",
                    ),
                    
                    # Select all checkbox
                    rx.hstack(
                        rx.checkbox(
                            checked=AuthState.all_google_events_selected,
                            on_change=AuthState.toggle_all_google_events,
                        ),
                        rx.text(
                            "Selecteer alle evenementen",
                            font_size="0.875rem",
                            font_weight="600",
                            color=T.text_primary,
                        ),
                        spacing="2",
                        padding="0.5rem",
                        width="100%",
                    ),
                    
                    # Events list
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                AuthState.new_google_events,
                                google_event_checkbox,
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        max_height="400px",
                        overflow_y="auto",
                        width="100%",
                        padding="0.5rem 0",
                    ),
                    
                    # Action buttons
                    rx.hstack(
                        rx.button(
                            "Annuleren",
                            on_click=AuthState.close_google_events_modal,
                            size="3",
                            variant="soft",
                            color_scheme="gray",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("plus", size=16),
                                rx.text(
                                    rx.cond(
                                        AuthState.selected_google_events.length() > 0,
                                        f"Maak {AuthState.selected_google_events.length()} Herinneringen",
                                        "Selecteer evenementen",
                                    ),
                                ),
                                spacing="2",
                            ),
                            on_click=AuthState.create_reminders_from_google_events,
                            size="3",
                            variant="solid",
                            color_scheme="green",
                            disabled=AuthState.selected_google_events.length() == 0,
                            loading=AuthState.is_creating_reminders,
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width=["90%", "500px", "600px"],
                max_width="90vw",
                max_height="85vh",
                background=T.modal_bg,
                border_radius=RADIUS["xl"],
                padding="1.5rem",
                box_shadow=T.shadow_xl,
                z_index="1201",
                overflow_y="auto",
            ),
        ),
        rx.fragment(),
    )
