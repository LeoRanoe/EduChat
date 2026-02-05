"""Calendar view component for EduChat.

This component displays a beautiful calendar interface synced with Google Calendar.
Supports month, week, and day views with full interactivity.
"""

import reflex as rx
from datetime import datetime, timedelta
from calendar import monthrange
from educhat.styles.theme import COLORS, RADIUS, T
from educhat.state.auth_state import AuthState
from educhat.components.shared.sync_status import sync_status_badge


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
                    align="center",
                ),
                # Show sync status for reminders
                rx.cond(
                    event.get("type", "") == "reminder",
                    sync_status_badge(
                        status=event.get("sync_status", "pending"),
                        last_sync_time=event.get("last_sync_at", ""),
                        google_link=rx.cond(
                            event.get("google_calendar_event_id", "") != "",
                            f"https://calendar.google.com/calendar/event?eid={event.get('google_calendar_event_id', '')}",
                            ""
                        )
                    ),
                    rx.fragment(),
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
                width="100%",
                align="center",
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
            
            # Sync button
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Synchroniseren",
                on_click=AuthState.sync_calendar_events,
                size="2",
                variant="soft",
                color_scheme="green",
                loading=AuthState.is_syncing_calendar,
                width="100%",
            ),
            
            spacing="3",
            width="100%",
        ),
        padding="1rem",
        class_name="card-panel",
        border_radius=RADIUS["lg"],
    )


def calendar_week_view() -> rx.Component:
    """Week view calendar component."""
    return rx.vstack(
        # Week header with navigation
        rx.hstack(
            rx.box(
                rx.icon("chevron-left", size=20, color=T.text_primary),
                on_click=AuthState.previous_week,
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={"background": T.bg_hover},
            ),
            rx.text(
                AuthState.current_week_range,
                font_size="1.125rem",
                font_weight="700",
                color=T.text_primary,
                flex="1",
                text_align="center",
            ),
            rx.box(
                rx.icon("chevron-right", size=20, color=T.text_primary),
                on_click=AuthState.next_week,
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={"background": T.bg_hover},
            ),
            justify="between",
            width="100%",
            padding="0.5rem 0",
        ),
        # Time slots grid
        rx.box(
            rx.vstack(
                rx.foreach(
                    AuthState.week_time_slots,
                    lambda slot: rx.hstack(
                        rx.text(
                            slot["time"],
                            font_size="0.75rem",
                            color=T.text_secondary,
                            width="60px",
                            text_align="right",
                        ),
                        rx.box(
                            rx.cond(
                                slot["has_event"],
                                rx.box(
                                    rx.text(
                                        slot["event_title"],
                                        font_size="0.75rem",
                                        font_weight="600",
                                        color=T.text_on_primary,
                                    ),
                                    padding="0.5rem",
                                    background=COLORS["primary_green"],
                                    border_radius=RADIUS["sm"],
                                ),
                                rx.fragment(),
                            ),
                            flex="1",
                            min_height="40px",
                            border=f"1px solid {T.border_light}",
                            border_radius=RADIUS["sm"],
                            padding="0.25rem",
                        ),
                        spacing="2",
                        width="100%",
                        align="start",
                    ),
                ),
                spacing="1",
                width="100%",
            ),
            max_height="500px",
            overflow_y="auto",
            width="100%",
        ),
        spacing="3",
        width="100%",
    )


def calendar_day_view() -> rx.Component:
    """Day view calendar component."""
    return rx.vstack(
        # Day header with navigation
        rx.hstack(
            rx.box(
                rx.icon("chevron-left", size=20, color=T.text_primary),
                on_click=AuthState.previous_day,
                cursor="pointer",
                padding="0.5rem",
                border_radius=RADIUS["sm"],
                _hover={"background": T.bg_hover},
            ),
            rx.text(
                AuthState.selected_day_formatted,
                font_size="1.125rem",
                font_weight="700",
                color=T.text_primary,
                flex="1",
                text_align="center",
            ),
            rx.box(
                rx.icon("chevron-right", size=20, color=T.text_primary),
                on_click=AuthState.next_day,
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
        # Events for the day
        rx.box(
            rx.vstack(
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
                            rx.icon("calendar-x", size=48, color=T.text_tertiary),
                            rx.text(
                                "Geen evenementen voor deze dag",
                                font_size="0.875rem",
                                color=T.text_secondary,
                            ),
                            spacing="3",
                            align_items="center",
                        ),
                        padding="3rem",
                        text_align="center",
                    ),
                ),
                spacing="2",
                width="100%",
            ),
            width="100%",
        ),
        spacing="3",
        width="100%",
    )


def calendar_view_controls() -> rx.Component:
    """View controls for calendar."""
    return rx.hstack(
        rx.hstack(
            rx.button(
                rx.hstack(
                    rx.icon("calendar", size=16),
                    rx.text("Maand"),
                    spacing="2",
                    align="center",
                ),
                on_click=lambda: AuthState.set_calendar_view("month"),
                padding="0.75rem 1rem",
                background=rx.cond(
                    AuthState.calendar_view == "month",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    T.bg_secondary,
                ),
                color=rx.cond(AuthState.calendar_view == "month", T.text_on_primary, T.text_primary),
                font_weight="600",
                border_radius=RADIUS["md"],
                cursor="pointer",
                _hover={"transform": "translateY(-1px)"},
                transition="all 0.2s ease",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("calendar-days", size=16),
                    rx.text("Week"),
                    spacing="2",
                    align="center",
                ),
                on_click=lambda: AuthState.set_calendar_view("week"),
                padding="0.75rem 1rem",
                background=rx.cond(
                    AuthState.calendar_view == "week",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    T.bg_secondary,
                ),
                color=rx.cond(AuthState.calendar_view == "week", T.text_on_primary, T.text_primary),
                font_weight="600",
                border_radius=RADIUS["md"],
                cursor="pointer",
                _hover={"transform": "translateY(-1px)"},
                transition="all 0.2s ease",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("calendar-clock", size=16),
                    rx.text("Dag"),
                    spacing="2",
                    align="center",
                ),
                on_click=lambda: AuthState.set_calendar_view("day"),
                padding="0.75rem 1rem",
                background=rx.cond(
                    AuthState.calendar_view == "day",
                    f"linear-gradient(135deg, {COLORS['primary_green']} 0%, {COLORS['dark_green']} 100%)",
                    T.bg_secondary,
                ),
                color=rx.cond(AuthState.calendar_view == "day", T.text_on_primary, T.text_primary),
                font_weight="600",
                border_radius=RADIUS["md"],
                cursor="pointer",
                _hover={"transform": "translateY(-1px)"},
                transition="all 0.2s ease",
            ),
            spacing="2",
            flex_wrap="wrap",
        ),
        # Google Calendar sync indicator
        rx.cond(
            AuthState.last_calendar_sync != "",
            rx.hstack(
                rx.icon("check_check", size=14, color=COLORS["primary_green"]),
                rx.text(
                    "Gesynchroniseerd",
                    font_size="0.8125rem",
                    color=T.text_secondary,
                    font_weight="500",
                ),
                spacing="2",
                padding="0.65rem 1rem",
                background=f"{COLORS['primary_green']}12",
                border=f"1px solid {COLORS['primary_green']}30",
                border_radius=RADIUS["md"],
                align="center",
            ),
            rx.fragment(),
        ),
        width="100%",
        padding="1rem 0",
        flex_wrap="wrap",
        gap="1rem",
        align="center",
        justify="between",
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
                z_index="999",
                on_click=AuthState.toggle_calendar_view,
            ),
            # Calendar modal
            rx.box(
                rx.box(
                    rx.vstack(
                    # Header
                    rx.hstack(
                        rx.hstack(
                            rx.icon("calendar", size=28, color=COLORS["primary_green"]),
                            rx.text(
                                "Kalender",
                                font_size="1.5rem",
                                font_weight="700",
                                color=T.text_primary,
                                letter_spacing="-0.5px",
                            ),
                            spacing="3",
                            align="center",
                        ),
                        rx.box(
                            rx.icon("x", size=24, color=T.text_secondary),
                            on_click=AuthState.toggle_calendar_view,
                            cursor="pointer",
                            padding="0.75rem",
                            border_radius=RADIUS["sm"],
                            _hover={
                                "background": T.bg_hover,
                                "color": T.text_primary,
                            },
                            transition="all 0.2s ease",
                        ),
                        justify="between",
                        width="100%",
                        padding_bottom="1.5rem",
                        border_bottom=f"2px solid {T.border_light}",
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
                        rx.cond(
                            AuthState.calendar_view == "week",
                            # Week view
                            calendar_week_view(),
                            # Day view
                            calendar_day_view(),
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
                overflow="hidden",
            ),
            position="fixed",
            top="50%",
            left="50%",
            transform="translate(-50%, -50%)",
            width="min(95vw, 1100px)",
            max_height="90vh",
            overflow_y="auto",
            overflow_x="hidden",
            class_name="calendar-modal",
            border_radius=RADIUS["xl"],
            box_shadow="0 25px 50px -12px rgba(0, 0, 0, 0.25)",
            z_index="999",
            ),
            position="fixed",
            top="0",
            left="0",
            right="0",
            bottom="0",
            z_index="998",
        ),
        rx.fragment(),
    )
