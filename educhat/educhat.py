"""Main application entry point for EduChat."""

import reflex as rx
from educhat.pages import index
from educhat.pages.onboarding import onboarding


# Create the app instance
app = rx.App()

# Add pages
app.add_page(onboarding, route="/onboarding")
app.add_page(index, route="/")
