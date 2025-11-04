"""Main application entry point for EduChat."""

import reflex as rx
from educhat.pages import index


# Create the app instance
app = rx.App()

# Add pages
app.add_page(index, route="/")
