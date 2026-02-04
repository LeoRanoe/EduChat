"""Calendar sync status bar component - Compact header for quick sync and connection status."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, TRANSITIONS, T
from educhat.state.auth_state import AuthState


def calendar_sync_bar() -> rx.Component:
    """Subtle Google Calendar sync status bar - integrated with theme.
    
    Shows:
    - Google Calendar connection with matching theme icon
    - Quick manual sync button
    """
    return rx.box(
        rx.hstack(
            # Google Calendar label + status (very subtle)
            rx.hstack(
                # Calendar icon (matching theme)
                rx.icon("calendar", size=15, color=COLORS["primary_green"]),
                
                # Compact status text
                rx.text(
                    "Google Calendar",
                    font_size="0.75rem",
                    font_weight="500",
                    color=T.text_secondary,
                ),
                
                spacing="1",
                align="center",
            ),
            
            # Subtle sync status
            rx.cond(
                AuthState.last_calendar_sync != "",
                rx.text(
                    rx.cond(
                        AuthState.is_manual_syncing,
                        "syncing...",
                        f"sync: {AuthState.last_calendar_sync}",
                    ),
                    font_size="0.7rem",
                    color=T.text_tertiary,
                    opacity="0.7",
                ),
                rx.fragment(),
            ),
            
            # Spacer
            rx.spacer(),
            
            # Minimal sync button (icon only on desktop, icon + text on hover)
            rx.box(
                rx.hstack(
                    rx.cond(
                        AuthState.is_manual_syncing,
                        rx.icon("loader-circle", size=14, color=COLORS["primary_green"], class_name="spin"),
                        rx.icon("refresh-cw", size=14, color=COLORS["primary_green"]),
                    ),
                    spacing="0",
                ),
                on_click=AuthState.manual_sync_calendar,
                cursor=rx.cond(AuthState.is_manual_syncing, "not-allowed", "pointer"),
                opacity=rx.cond(AuthState.is_manual_syncing, "0.5", "0.7"),
                padding="0.375rem 0.5rem",
                border_radius=RADIUS["md"],
                background="transparent",
                transition=TRANSITIONS["fast"],
                _hover={
                    "opacity": rx.cond(AuthState.is_manual_syncing, "0.5", "1"),
                    "background": rx.cond(
                        AuthState.is_manual_syncing,
                        "transparent",
                        f"rgba(16, 163, 127, 0.08)",
                    ),
                },
                title="Synchroniseer met Google Calendar",
            ),
            
            width="100%",
            spacing="2",
            align="center",
            padding="0.5rem 0.875rem",
            background="transparent",
            border_bottom=f"1px solid {T.border}",
            justify="between",
        ),
    )
