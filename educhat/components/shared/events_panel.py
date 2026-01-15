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
                rx.icon("calendar", size=18, color="#3B82F6"),
                width="40px",
                height="40px",
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
                    font_size="0.9375rem",
                    font_weight="600",
                    color=COLORS["text_primary"],
                    line_height="1.4",
                ),
                rx.cond(
                    event.get("institution", "") != "",
                    rx.text(
                        event["institution"],
                        font_size="0.75rem",
                        color=COLORS["primary_green"],
                        font_weight="500",
                        line_height="1.3",
                    ),
                    rx.fragment(),
                ),
                rx.text(
                    rx.cond(
                        event["date"],
                        f"📅 {event['date'][:10]}",
                        "📅 TBD",
                    ),
                    font_size="0.8125rem",
                    color=COLORS["text_tertiary"],
                    line_height="1.3",
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            rx.box(
                rx.icon("bell-plus", size=16, color=COLORS["text_tertiary"]),
                on_click=lambda: AuthState.create_reminder_from_event(event["id"]),
                cursor="pointer",
                padding="0.625rem",
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
        padding="1rem",
        min_height="72px",
        background=COLORS["white"],
        border=f"1px solid {COLORS['border_light']}",
        border_radius=RADIUS["lg"],
        _hover={
            "border_color": "#3B82F6",
            "box_shadow": "0 2px 8px rgba(59, 130, 246, 0.15)",
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
                                    rx.box(
                                        rx.icon("calendar-search", size=56, color="#94A3B8"),
                                        width="80px",
                                        height="80px",
                                        display="flex",
                                        align_items="center",
                                        justify_content="center",
                                        background="rgba(148, 163, 184, 0.1)",
                                        border_radius="50%",
                                        margin_bottom="1rem",
                                    ),
                                    rx.text(
                                        "Geen evenementen gevonden",
                                        font_size="1rem",
                                        color=COLORS["text_primary"],
                                        font_weight="600",
                                        margin_bottom="0.5rem",
                                    ),
                                    rx.text(
                                        "Er zijn momenteel geen komende evenementen beschikbaar.",
                                        font_size="0.875rem",
                                        color=COLORS["text_secondary"],
                                        text_align="center",
                                        line_height="1.6",
                                        max_width="300px",
                                        margin_bottom="0.5rem",
                                    ),
                                    rx.text(
                                        "Check de belangrijke periodes hieronder",
                                        font_size="0.8125rem",
                                        color=COLORS["primary_green"],
                                        font_weight="500",
                                    ),
                                    spacing="3",
                                    align="center",
                                    padding="3rem 2rem",
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
                width=["90%", "420px", "480px"],
                max_width="90vw",
                max_height="85vh",
                overflow_y="auto",
                box_shadow="0 20px 60px rgba(0, 0, 0, 0.15)",
                z_index="1001",
            ),
        ),
        rx.fragment(),
    )
