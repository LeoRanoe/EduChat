"""Calendar view component for EduChat.

This component displays a beautiful calendar interface synced with Google Calendar.
Supports month, week, and day views with full interactivity.
"""

import reflex as rx
from datetime import datetime, timedelta
from calendar import monthrange
from educhat.styles.theme import COLORS, RADIUS, T
from educhat.state.auth_state import AuthState


def calendar_day_cell(day_data: dict) -> rx.Component:
    """Single day cell in calendar month view."""
    return rx.box(
        rx.vstack(
            rx.text(
                day_data["day"],
                font_size="0.875rem",
                font_weight=rx.cond(day_data["is_today"], "600", "500"),
                color=rx.cond(
                    day_data["is_today"],
                    T.text_on_primary,
                    rx.cond(
                        day_data["is_current_month"],
                        T.text_primary,
                        T.text_tertiary
                    )
                ),
            ),
            rx.cond(
                day_data["events_count"],  # 0 is falsy, positive numbers are truthy
                rx.box(
                    rx.text(
                        day_data["events_count"],
                        font_size="0.625rem",
                        font_weight="600",
                        color=T.text_on_primary,
                    ),
                    width="16px",
                    height="16px",
                    border_radius="50%",
                    background=COLORS["primary_green"],
                    display="flex",
                    align_items="center",
                    justify_content="center",
                ),
                rx.fragment(),
            ),
            spacing="1",
            align_items="center",
        ),
        padding="0.5rem",
        min_height="60px",
        background=rx.cond(
            day_data["is_today"],
            COLORS["primary_green"],
            rx.cond(
                day_data["is_current_month"],
                T.bg_card,
                T.bg_secondary
            )
        ),
        border=f"1px solid {T.border_light}",
        border_radius=RADIUS["md"],
        cursor="pointer",
        _hover={
            "background": rx.cond(
                day_data["is_today"],
                COLORS["primary_green"],
                T.bg_hover
            ),
            "border_color": COLORS["primary_green"],
        },
        transition="all 0.2s ease",
    )


def calendar_month_view() -> rx.Component:
    """Month view calendar component."""
    return rx.vstack(
        # Calendar header with month/year navigation
        rx.hstack(
            rx.box(
                rx.icon("chevron-left", size=20, color=T.text_primary),
                on_click=AuthState.previous_month,
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={"background": T.bg_hover},
            ),
            rx.text(
                AuthState.current_calendar_month_year,
                font_size="1.125rem",
                font_weight="700",
                color=T.text_primary,
                flex="1",
                text_align="center",
            ),
            rx.box(
                rx.icon("chevron-right", size=20, color=T.text_primary),
                on_click=AuthState.next_month,
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={"background": T.bg_hover},
            ),
            rx.button(
                "Vandaag",
                on_click=AuthState.go_to_today,
                size="2",
                variant="soft",
                color_scheme="green",
            ),
            justify="between",
            width="100%",
            padding="0.5rem 0",
        ),
        
        # Weekday headers
        rx.grid(
            rx.text("Ma", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Di", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Wo", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Do", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Vr", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Za", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            rx.text("Zo", font_size="0.75rem", font_weight="600", color=T.text_secondary, text_align="center"),
            columns="7",
            spacing="2",
            width="100%",
        ),
        
        # Calendar grid
        rx.box(
            rx.foreach(
                AuthState.calendar_days,
                calendar_day_cell,
            ),
            display="grid",
            grid_template_columns="repeat(7, 1fr)",
            gap="0.5rem",
            width="100%",
        ),
        
        spacing="3",
        width="100%",
    )


def event_card_mini(event: dict) -> rx.Component:
    """Mini event card for day view."""
    return rx.box(
        rx.hstack(
            rx.box(
                width="4px",
                height="100%",
                background=COLORS["primary_green"],
                border_radius="2px",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(
                        event.get("start_time", "00:00"),  # Display full time
                        font_size="0.75rem",
                        font_weight="600",
                        color=COLORS["primary_green"],
                    ),
                    rx.text(
                        event["title"],
                        font_size="0.875rem",
                        font_weight="600",
                        color=T.text_primary,
                        flex="1",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.cond(
                    event.get("institution", "") != "",
                    rx.text(
                        event["institution"],
                        font_size="0.75rem",
                        color=T.text_secondary,
                    ),
                    rx.fragment(),
                ),
                spacing="1",
                align_items="start",
                flex="1",
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        padding="0.75rem",
        background=T.bg_card,
        border=f"1px solid {T.border_light}",
        border_radius=RADIUS["md"],
        cursor="pointer",
        _hover={
            "border_color": COLORS["primary_green"],
            "box_shadow": f"0 2px 8px {COLORS['primary_green']}15",
        },
        transition="all 0.2s ease",
        on_click=lambda: AuthState.show_event_details(event["id"]),
    )


def calendar_day_events() -> rx.Component:
    """Display events for selected day."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("calendar-days", size=18, color=COLORS["primary_green"]),
                rx.text(
                    AuthState.selected_day_formatted,
                    font_size="1rem",
                    font_weight="700",
                    color=T.text_primary,
                ),
                spacing="2",
            ),
            
            rx.cond(
                AuthState.selected_day_events.length() > 0,
                rx.vstack(
                    rx.foreach(
                        AuthState.selected_day_events,
                        event_card_mini,
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.box(
                    rx.vstack(
                        rx.icon("calendar-x", size=32, color=T.text_tertiary),
                        rx.text(
                            "Geen evenementen",
                            font_size="0.875rem",
                            color=T.text_secondary,
                        ),
                        spacing="2",
                        align_items="center",
                    ),
                    padding="2rem",
                    text_align="center",
                ),
            ),
            
            spacing="3",
            width="100%",
        ),
        padding="1rem",
        class_name="card-panel",
        border_radius=RADIUS["lg"],
    )


def calendar_view_controls() -> rx.Component:
    """View controls for calendar."""
    return rx.hstack(
        rx.hstack(
            rx.button(
                rx.icon("calendar", size=16),
                "Maand",
                on_click=lambda: AuthState.set_calendar_view("month"),
                size="2",
                variant=rx.cond(
                    AuthState.calendar_view == "month",
                    "solid",
                    "soft"
                ),
                color_scheme="green",
            ),
            rx.button(
                rx.icon("calendar-days", size=16),
                "Week",
                on_click=lambda: AuthState.set_calendar_view("week"),
                size="2",
                variant=rx.cond(
                    AuthState.calendar_view == "week",
                    "solid",
                    "soft"
                ),
                color_scheme="green",
            ),
            rx.button(
                rx.icon("calendar-clock", size=16),
                "Dag",
                on_click=lambda: AuthState.set_calendar_view("day"),
                size="2",
                variant=rx.cond(
                    AuthState.calendar_view == "day",
                    "solid",
                    "soft"
                ),
                color_scheme="green",
            ),
            spacing="2",
        ),
        
        rx.hstack(
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Sync",
                on_click=AuthState.sync_calendar_events,
                size="2",
                variant="soft",
                color_scheme="green",
                loading=AuthState.is_syncing_calendar,
            ),
            spacing="2",
        ),
        
        justify="between",
        width="100%",
        padding="0.5rem 0",
    )


def calendar_view() -> rx.Component:
    """Main calendar view component."""
    return rx.cond(
        AuthState.show_calendar_view,
        rx.box(
            # Overlay
            rx.box(
                position="fixed",
                top="0",
                left="0",
                right="0",
                bottom="0",
                background=T.overlay,
                z_index="1002",
                on_click=AuthState.toggle_calendar_view,
            ),
            # Calendar modal
            rx.box(
                rx.box(
                    rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("calendar", size=24, color=COLORS["primary_green"]),
                            rx.text(
                                "Kalender",
                                font_size="1.25rem",
                                font_weight="700",
                                color=T.text_primary,
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=20, color=T.text_secondary),
                            on_click=AuthState.toggle_calendar_view,
                            cursor="pointer",
                            padding="0.5rem",
                            border_radius=RADIUS["sm"],
                            _hover={"background": T.bg_hover},
                            transition="all 0.2s ease",
                        ),
                        justify="between",
                        width="100%",
                    ),
                    
                    # View controls
                    calendar_view_controls(),
                    
                    rx.divider(),
                    
                    # Main calendar content
                    rx.cond(
                        AuthState.calendar_view == "month",
                        rx.hstack(
                            # Month view
                            rx.box(
                                calendar_month_view(),
                                flex="2",
                            ),
                            # Events sidebar
                            rx.box(
                                calendar_day_events(),
                                flex="1",
                                min_width="250px",
                            ),
                            spacing="4",
                            width="100%",
                            align="start",
                        ),
                        # Week and day views would go here
                        rx.box(
                            rx.text(
                                "Week en Dag weergaven komen binnenkort!",
                                color=T.text_secondary,
                                font_size="0.875rem",
                            ),
                            padding="2rem",
                            text_align="center",
                        ),
                    ),
                    
                    spacing="4",
                    width="100%",
                    height="100%",
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
                padding="2rem",
                position="relative",
                z_index="2",
            ),
            position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                width="min(95vw, 1100px)",
                max_height="90vh",
                overflow_y="auto",
                class_name="calendar-modal",
                border_radius=RADIUS["xl"],
                box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
                z_index="1003",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="1000",
        ),
        rx.fragment(),
    )
