"""Main application entry point for EduChat."""

import reflex as rx
from educhat.pages import index
from educhat.pages.onboarding import onboarding
from educhat.pages.landing import landing
from educhat.styles.theme import COLORS


# Create the app instance with theme configuration
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    ],
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
app.add_page(
    landing,
    route="/",
    title="EduChat - Your AI Study Assistant",
    description="Get instant help with your studies, homework, and exam preparation",
)
app.add_page(
    index,
    route="/chat",
    title="Chat - EduChat",
    description="EduChat helpt je makkelijk informatie te vinden over onderwijs in Suriname",
)
app.add_page(
    onboarding,
    route="/onboarding",
    title="Onboarding - EduChat",
    description="Personaliseer je EduChat ervaring",
)

