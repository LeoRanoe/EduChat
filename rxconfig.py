"""Reflex configuration file for EduChat."""

import os
import reflex as rx
from reflex.utils.console import LogLevel

# Determine environment - Render sets RENDER=true
is_render = os.getenv("RENDER") == "true"
is_production = is_render or os.getenv("APP_ENV") == "production"

# Get port - Render exposes PORT env var (defaults to 10000)
# CRITICAL: Must use PORT env var for Render to detect the service
port = int(os.getenv("PORT", "8000"))

config = rx.Config(
    app_name="educhat",
    
    # Environment
    env=rx.Env.PROD if is_production else rx.Env.DEV,
    
    # Database (using Supabase, not Reflex's internal DB)
    # db_url not needed as we use Supabase client directly
    
    # API Configuration
    api_url=f"https://educhat-dgxn.onrender.com" if is_render else f"http://localhost:{port}",
    
    # Port Configuration
    backend_port=port,
    backend_host="0.0.0.0",
    
    # Production optimizations
    timeout=120 if is_production else 600,
    
    # Logging
    loglevel=LogLevel.INFO if is_production else LogLevel.DEBUG,
    
    # Disable sitemap plugin to avoid warnings
    disable_plugins=["reflex.plugins.sitemap.SitemapPlugin"],
    
    # Custom stylesheets and scripts
    stylesheets=[
        "/custom.css",  # Custom animations and styles
    ],
    scripts=[
        "/auto-expand.js",  # Auto-expanding textarea
        "/auto-scroll.js",  # Auto-scroll to new messages
    ],
)
