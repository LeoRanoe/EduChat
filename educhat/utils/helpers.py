"""Helper utility functions."""

from datetime import datetime
from typing import Any, Dict


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def format_message(role: str, content: str) -> Dict[str, Any]:
    """Format a message for storage."""
    return {
        "role": role,
        "content": content,
        "timestamp": get_timestamp(),
    }


def validate_env_vars() -> bool:
    """Validate that required environment variables are set."""
    import os
    
    required_vars = ["MONGODB_URI", "OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        return False
    
    return True
