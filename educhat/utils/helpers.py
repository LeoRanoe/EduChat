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
    
    # Check for either DATABASE_URL (Prisma) or SUPABASE_URL + SUPABASE_ANON_KEY
    has_database = os.getenv("DATABASE_URL") or (
        os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_ANON_KEY")
    )
    has_openai = os.getenv("OPENAI_API_KEY")
    
    missing = []
    if not has_database:
        missing.append("DATABASE_URL or (SUPABASE_URL + SUPABASE_ANON_KEY)")
    if not has_openai:
        missing.append("OPENAI_API_KEY")
    
    if missing:
        print(f"⚠️  Missing environment variables: {', '.join(missing)}")
        return False
    
    return True
