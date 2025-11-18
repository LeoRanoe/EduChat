"""Helper utility functions."""

from datetime import datetime, timedelta
from typing import Any, Dict, List


def get_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.utcnow().isoformat()


def group_conversations_by_date(conversations: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group conversations by date categories.
    
    Args:
        conversations: List of conversation dicts with 'updated_at' or 'created_at' timestamp
        
    Returns:
        Dict with keys: 'Today', 'Yesterday', 'This Week', 'This Month', 'Older'
    """
    now = datetime.now()
    today = now.date()
    yesterday = (now - timedelta(days=1)).date()
    week_ago = (now - timedelta(days=7)).date()
    month_ago = (now - timedelta(days=30)).date()
    
    groups = {
        "Today": [],
        "Yesterday": [],
        "This Week": [],
        "This Month": [],
        "Older": []
    }
    
    for conv in conversations:
        # Get timestamp from conversation
        timestamp_str = conv.get("updated_at") or conv.get("created_at")
        if not timestamp_str:
            groups["Older"].append(conv)
            continue
            
        try:
            # Parse timestamp
            if isinstance(timestamp_str, str):
                conv_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).date()
            else:
                conv_date = timestamp_str.date()
            
            # Categorize
            if conv_date == today:
                groups["Today"].append(conv)
            elif conv_date == yesterday:
                groups["Yesterday"].append(conv)
            elif conv_date >= week_ago:
                groups["This Week"].append(conv)
            elif conv_date >= month_ago:
                groups["This Month"].append(conv)
            else:
                groups["Older"].append(conv)
        except (ValueError, AttributeError):
            groups["Older"].append(conv)
    
    # Return only non-empty groups
    return {k: v for k, v in groups.items() if v}


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

