"""Database service for EduChat - Supabase/Postgres integration.

This module provides a thin wrapper around the existing supabase_client for backward compatibility.
All database operations now use Supabase/Postgres instead of MongoDB.

For new code, prefer importing directly from supabase_client:
    from educhat.services.supabase_client import get_client, SupabaseService
"""

from educhat.services.supabase_client import get_client, SupabaseService

# Re-export for backward compatibility
DatabaseService = SupabaseService
get_database_service = lambda: SupabaseService()

__all__ = ["DatabaseService", "get_database_service", "get_client", "SupabaseService"]
