"""Main application entry point for EduChat."""

import reflex as rx
from educhat.pages import index
from educhat.pages.onboarding import onboarding
from educhat.styles.theme import COLORS


# Create the app instance with theme configuration
app = rx.App(
    stylesheets=[],
    style={
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "background": COLORS["light_gray"],
    },
    theme=rx.theme(
        appearance="light",
        accent_color="green",
    ),
)

# Add pages
app.add_page(onboarding, route="/onboarding")
app.add_page(index, route="/")
