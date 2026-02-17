"""Calendar sync status bar component - Compact header for quick sync and connection status."""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, TRANSITIONS, T
from educhat.state.auth_state import AuthState
from educhat.state.app_state import AppState
from educhat.utils.translations import t


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
            
            # Personalization indicator (shown when onboarding data is loaded)
            rx.cond(
                AppState.onboarding_loaded & (AppState.user_context != None),
                rx.hstack(
                    rx.icon("user-check", size=14, color=COLORS["primary_green"]),
                    rx.text(
                        t("personalized"),
                        font_size="0.7rem",
                        font_weight="600",
                        color=T.text_secondary,
                    ),
                    spacing="1",
                    align="center",
                    padding="6px 10px",
                    background=f"linear-gradient(135deg, rgba(16, 163, 127, 0.06) 0%, rgba(13, 138, 107, 0.1) 100%)",
                    border=f"1px solid rgba(16, 163, 127, 0.15)",
                    border_radius="8px",
                    display=["none", "none", "flex"],  # Only show on desktop
                ),
                rx.fragment(),
            ),
            
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
