"""Sync Status UI Components for EduChat.

Visual indicators for Google Calendar sync status with real-time updates.
"""

import reflex as rx
from educhat.styles.theme import COLORS, RADIUS, T


def sync_status_badge(
    status: str,
    last_sync_time: str = "",
    error_message: str = "",
    google_link: str = ""
) -> rx.Component:
    """Sync status badge showing current sync state.
    
    Args:
        status: Sync status (pending, syncing, synced, error)
        last_sync_time: Last sync timestamp (HH:MM format)
        error_message: Error message if status is error
        google_link: Google Calendar event link
        
    Returns:
        Badge component with appropriate styling
    """
    return rx.cond(
        status == "syncing",
        # Syncing state
        rx.hstack(
            rx.icon("loader-2", size=12, class_name="animate-spin"),
            rx.text(
                "Synchroniseren...",
                font_size="0.6875rem",
                color=T.text_secondary,
            ),
            spacing="1",
            padding="0.25rem 0.5rem",
            background=f"{COLORS['primary_green']}10",
            border_radius=RADIUS["sm"],
            align="center",
        ),
        rx.cond(
            status == "synced",
            # Synced state
            rx.cond(
                google_link != "",
                # With Google Calendar link
                rx.link(
                    rx.hstack(
                        rx.icon("check-circle", size=12, color=COLORS["primary_green"]),
                        rx.text(
                            f"✓ {last_sync_time}",
                            font_size="0.6875rem",
                            color=COLORS["primary_green"],
                        ),
                        spacing="1",
                        padding="0.25rem 0.5rem",
                        background=f"{COLORS['primary_green']}15",
                        border_radius=RADIUS["sm"],
                        align="center",
                        _hover={
                            "background": f"{COLORS['primary_green']}25",
                        },
                        transition="all 0.2s ease",
                    ),
                    href=google_link,
                    is_external=True,
                    text_decoration="none",
                ),
                # Without link
                rx.hstack(
                    rx.icon("check-circle", size=12, color=COLORS["primary_green"]),
                    rx.text(
                        f"✓ {last_sync_time}",
                        font_size="0.6875rem",
                        color=COLORS["primary_green"],
                    ),
                    spacing="1",
                    padding="0.25rem 0.5rem",
                    background=f"{COLORS['primary_green']}15",
                    border_radius=RADIUS["sm"],
                    align="center",
                ),
            ),
            rx.cond(
                status == "error",
                # Error state
                rx.box(
                    rx.hstack(
                        rx.icon("alert-circle", size=12, color=T.error),
                        rx.text(
                            "Sync mislukt",
                            font_size="0.6875rem",
                            color=T.error,
                        ),
                        spacing="1",
                        align="center",
                    ),
                    padding="0.25rem 0.5rem",
                    background=f"{T.error}15",
                    border_radius=RADIUS["sm"],
                    title=error_message,
                    cursor="help",
                ),
                rx.cond(
                    status == "pending",
                    # Pending state
                    rx.hstack(
                        rx.icon("clock", size=12, color=T.text_tertiary),
                        rx.text(
                            "Wacht op sync",
                            font_size="0.6875rem",
                            color=T.text_tertiary,
                        ),
                        spacing="1",
                        padding="0.25rem 0.5rem",
                        background=T.bg_tertiary,
                        border_radius=RADIUS["sm"],
                        align="center",
                    ),
                    rx.fragment(),
                ),
            ),
        ),
    )


def sync_retry_button(on_click_handler) -> rx.Component:
    """Retry button for failed syncs.
    
    Args:
        on_click_handler: Click handler function
        
    Returns:
        Retry button component
    """
    return rx.el.button(
        rx.hstack(
            rx.icon("refresh-cw", size=14),
            rx.text("Opnieuw proberen", font_size="0.75rem"),
            spacing="1",
            align="center",
        ),
        on_click=on_click_handler,
        padding="0.375rem 0.75rem",
        background=f"{COLORS['primary_green']}10",
        color=COLORS["primary_green"],
        border=f"1px solid {COLORS['primary_green']}30",
        border_radius=RADIUS["sm"],
        cursor="pointer",
        font_weight="500",
        _hover={
            "background": f"{COLORS['primary_green']}20",
        },
        transition="all 0.2s ease",
    )


def google_calendar_link_button(link: str) -> rx.Component:
    """Button to open event in Google Calendar.
    
    Args:
        link: Google Calendar event link
        
    Returns:
        Link button component
    """
    return rx.link(
        rx.hstack(
            rx.icon("external-link", size=14, color=COLORS["primary_green"]),
            rx.text(
                "Open in Google Calendar",
                font_size="0.75rem",
                color=COLORS["primary_green"],
            ),
            spacing="1",
            align="center",
            padding="0.375rem 0.75rem",
            border=f"1px solid {COLORS['primary_green']}30",
            border_radius=RADIUS["sm"],
            _hover={
                "background": f"{COLORS['primary_green']}10",
                "border_color": COLORS["primary_green"],
            },
            transition="all 0.2s ease",
        ),
        href=link,
        is_external=True,
        text_decoration="none",
    )


def sync_progress_indicator(
    syncing_count: int,
    total_count: int,
    status_text: str = "Synchroniseren..."
) -> rx.Component:
    """Progress indicator for batch sync operations.
    
    Args:
        syncing_count: Number of items currently syncing
        total_count: Total number of items to sync
        status_text: Status message
        
    Returns:
        Progress indicator component
    """
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("loader-2", size=16, class_name="animate-spin", color=COLORS["primary_green"]),
                rx.text(
                    status_text,
                    font_size="0.875rem",
                    font_weight="600",
                    color=T.text_primary,
                ),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                rx.text(
                    f"{syncing_count}",
                    font_size="0.875rem",
                    font_weight="600",
                    color=COLORS["primary_green"],
                ),
                rx.text(
                    f"/ {total_count}",
                    font_size="0.875rem",
                    color=T.text_secondary,
                ),
                spacing="1",
                align="center",
            ),
            # Progress bar
            rx.box(
                rx.box(
                    width=f"{(syncing_count / max(total_count, 1)) * 100}%",
                    height="100%",
                    background=f"linear-gradient(90deg, {COLORS['primary_green']}, {COLORS['dark_green']})",
                    border_radius=RADIUS["sm"],
                    transition="width 0.3s ease",
                ),
                width="100%",
                height="4px",
                background=T.bg_tertiary,
                border_radius=RADIUS["sm"],
                overflow="hidden",
            ),
            spacing="2",
            width="100%",
        ),
        padding="1rem",
        background=T.bg_card,
        border=f"1px solid {T.border_light}",
        border_radius=RADIUS["lg"],
        width="100%",
    )
