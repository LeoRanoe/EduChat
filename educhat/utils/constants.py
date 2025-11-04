"""Constants used throughout the application."""

# Application metadata
APP_NAME = "EduChat"
APP_VERSION = "0.1.0"
APP_DESCRIPTION = "AI-powered educational assistant for Surinamese students"

# Database collections
COLLECTIONS = {
    "institutions": "instellingen",
    "questions": "vragen",
    "sessions": "sessies",
    "knowledge_base": "kennisbank",
    "feedback": "feedback",
}

# AI Configuration
AI_CONFIG = {
    "model": "gpt-4",  # or "gemini-pro"
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 30,  # seconds
}

# Response time targets
PERFORMANCE_TARGETS = {
    "response_time": 2.0,  # seconds
    "initial_load": 3.0,   # seconds
}
