"""Reflex configuration file for EduChat."""

import os
import reflex as rx

# Determine environment
app_env = os.getenv("APP_ENV", "development")
is_production = app_env == "production"

config = rx.Config(
    app_name="educhat",
    
    # Environment
    env=rx.Env.PROD if is_production else rx.Env.DEV,
    
    # Database (using Supabase, not Reflex's internal DB)
    # db_url not needed as we use Supabase client directly
    
    # API Configuration
    api_url="https://educhat.onrender.com" if is_production else "http://localhost:8000",
    
    # Frontend Configuration
    frontend_port=3000,
    backend_port=8000,
    
    # Production optimizations
    timeout=120 if is_production else 600,
    
    # Logging
    loglevel="info" if is_production else "debug",
)
