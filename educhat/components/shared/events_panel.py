"""Events panel component for EduChat."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS
from educhat.state.auth_state import AuthState


def event_item(event: dict) -> rx.Component:
    """Single event item in the list."""
    # Determine icon and color based on event type
    event_type = event.get("type", "general")
    
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon("calendar", size=16, color="#3B82F6"),
                width="32px",
                height="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                background="rgba(59, 130, 246, 0.15)",
                border_radius=RADIUS["md"],
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(
                    event["title"],
                    font_size="0.875rem",
                    font_weight="600",
                    color=COLORS["text_primary"],
                ),
                rx.cond(
                    event.get("institution", "") != "",
                    rx.text(
                        event["institution"],
                        font_size="0.7rem",
                        color=COLORS["primary_green"],
                        font_weight="500",
                    ),
                    rx.fragment(),
                ),
                rx.text(
                    rx.cond(
                        event["date"],
                        f"📅 {event['date'][:10]}",
                        "📅 TBD",
                    ),
                    font_size="0.75rem",
                    color=COLORS["text_tertiary"],
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.box(
                rx.icon("bell-plus", size=14, color=COLORS["text_tertiary"]),
                on_click=lambda: AuthState.create_reminder_from_event(event["id"]),
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                title="Maak herinnering",
                _hover={
                    "background": f"{COLORS['primary_green']}10",
                    "color": COLORS["primary_green"],
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
            "border_color": "#3B82F6",
            "box_shadow": "0 2px 8px rgba(59, 130, 246, 0.1)",
        },
        transition="all 0.2s ease",
    )


def events_panel() -> rx.Component:
    """Panel for viewing upcoming events and important dates."""
    return rx.cond(
        AuthState.show_events_panel,
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
                on_click=AuthState.toggle_events_panel,
            ),
            # Panel content
            rx.box(
                rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("calendar", size=20, color="#3B82F6"),
                            rx.text(
                                "Belangrijke Datums",
                                font_size="1.125rem",
                                font_weight="700",
                                color=COLORS["text_primary"],
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=18, color=COLORS["text_secondary"]),
                            on_click=AuthState.toggle_events_panel,
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
                    
                    # Info text
                    rx.box(
                        rx.text(
                            "Klik op het 🔔 icoon om een herinnering aan te maken",
                            font_size="0.75rem",
                            color=COLORS["text_secondary"],
                            font_style="italic",
                        ),
                        padding="0.5rem 0",
                    ),
                    
                    # Events list
                    rx.box(
                        rx.cond(
                            AuthState.upcoming_events.length() > 0,
                            rx.vstack(
                                rx.foreach(
                                    AuthState.upcoming_events,
                                    event_item,
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            rx.box(
                                rx.vstack(
                                    rx.icon("calendar-x", size=48, color=COLORS["border"]),
                                    rx.text(
                                        "Geen evenementen gevonden",
                                        font_size="0.875rem",
                                        color=COLORS["text_secondary"],
                                        font_weight="500",
                                    ),
                                    rx.text(
                                        "Check later voor updates",
                                        font_size="0.75rem",
                                        color=COLORS["text_tertiary"],
                                    ),
                                    spacing="2",
                                    align="center",
                                    padding="2rem",
                                ),
                                width="100%",
                                text_align="center",
                            ),
                        ),
                        max_height="50vh",
                        overflow_y="auto",
                        width="100%",
                        padding_right="0.5rem",
                    ),
                    
                    # Footer with info about important dates
                    rx.box(
                        rx.vstack(
                            rx.text(
                                "📚 Belangrijke Periodes",
                                font_size="0.8rem",
                                font_weight="600",
                                color=COLORS["text_primary"],
                            ),
                            rx.text(
                                "• Inschrijvingen: April - Juli",
                                font_size="0.75rem",
                                color=COLORS["text_secondary"],
                            ),
                            rx.text(
                                "• Schooljaar: September - Juli",
                                font_size="0.75rem",
                                color=COLORS["text_secondary"],
                            ),
                            rx.text(
                                "• Examens: Mei - Juni",
                                font_size="0.75rem",
                                color=COLORS["text_secondary"],
                            ),
                            spacing="1",
                            align_items="start",
                            width="100%",
                        ),
                        padding="1rem",
                        background=f"{COLORS['light_green']}20",
                        border_radius=RADIUS["md"],
                        margin_top="1rem",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                background=COLORS["white"],
                border_radius=RADIUS["xl"],
                padding="1.5rem",
                width=["90%", "400px"],
                max_width="400px",
                max_height="85vh",
                overflow_y="auto",
                box_shadow="0 20px 60px rgba(0, 0, 0, 0.15)",
                z_index="1001",
            ),
        ),
        rx.fragment(),
    )
