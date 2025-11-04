"""Main chat page for EduChat."""

import reflex as rx
from educhat.state.app_state import AppState


def index() -> rx.Component:
    """Main chat interface page."""
    return rx.container(
        rx.vstack(
            rx.heading("🎓 EduChat", size="9"),
            rx.text(
                "Welkom bij EduChat - Jouw AI-assistent voor educatie in Suriname",
                size="5",
                color_scheme="gray",
            ),
            rx.text(
                "Chat interface will be built in the next phase...",
                size="3",
                color_scheme="gray",
                style={"font-style": "italic"},
            ),
            spacing="4",
            align="center",
            min_height="100vh",
            justify="center",
        ),
        size="3",
    )
