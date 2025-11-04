"""Reflex configuration file for EduChat."""

import reflex as rx

config = rx.Config(
    app_name="educhat",
    db_url="sqlite:///reflex.db",  # Will be replaced with MongoDB
    env=rx.Env.DEV,
)
