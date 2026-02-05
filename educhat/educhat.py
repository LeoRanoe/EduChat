"""Main application entry point for EduChat."""

import reflex as rx
from educhat.pages import index
from educhat.pages.onboarding import onboarding
from educhat.pages.landing import landing
from educhat.pages.auth_callback import auth_callback
from educhat.pages.reset_password import reset_password_page


# Create the app instance with theme configuration
# Using Reflex's built-in color mode system with next-themes
# The "inherit" appearance respects system preference and persists user toggle
app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
        "/landing-animations.css",
    ],
    style={
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        "background": "var(--bg-primary)",
        "color": "var(--text-primary)",
        "min_height": "100vh",
        "transition": "background-color 0.3s ease, color 0.3s ease",
    },
    theme=rx.theme(
        appearance="inherit",  # Respects system preference + persists user toggle
        accent_color="green",
        has_background=True,
        radius="medium",
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
app.add_page(
    auth_callback,
    route="/auth/callback",
    title="Authenticating...",
    description="Processing OAuth authentication",
)
app.add_page(
    reset_password_page,
    route="/auth/reset-password",
    title="Reset Password - EduChat",
    description="Reset your EduChat password",
)

