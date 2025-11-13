"""Reflex configuration file for EduChat."""

import os
import reflex as rx
from reflex.utils.console import LogLevel

# Determine environment - check multiple env vars for Render
app_env = os.getenv("APP_ENV", os.getenv("RENDER", "development"))
is_production = app_env in ("production", "true", "1")

# Detect if running on Render (they set RENDER=true)
is_render = os.getenv("RENDER") is not None

config = rx.Config(
    app_name="educhat",
    
    # Environment
    env=rx.Env.PROD if is_production else rx.Env.DEV,
    
    # Database (using Supabase, not Reflex's internal DB)
    # db_url not needed as we use Supabase client directly
    
    # API Configuration
    api_url="https://educhat-dgxn.onrender.com" if is_render else "http://localhost:8001",
    
    # Frontend Configuration
    frontend_port=3000,
    backend_port=10000 if is_render else 8001,
    backend_host="0.0.0.0",
    
    # Production optimizations
    timeout=120 if is_production else 600,
    
    # Logging
    loglevel=LogLevel.INFO if is_production else LogLevel.DEBUG,
    
    # Custom stylesheets and scripts
    stylesheets=[
        "/custom.css",  # Custom animations and styles
    ],
    scripts=[
        "/auto-expand.js",  # Auto-expanding textarea
        "/auto-scroll.js",  # Auto-scroll to new messages
    ],
)
