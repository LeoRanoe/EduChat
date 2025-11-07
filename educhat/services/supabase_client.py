"""
Supabase Database Service using Supabase Python SDK

This module provides a high-level interface to interact with the Supabase PostgreSQL
database using the official Supabase Python client. It handles connection management,
CRUD operations, and provides helper methods for common database queries.

Usage:
    from educhat.services.supabase_client import get_client, SupabaseService
    
    # Get database instance
    client = get_client()
    
    # Use service methods
    service = SupabaseService()
    institutions = service.get_all_institutions()
"""

import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Global Supabase client instance
_supabase_client = None


def get_client():
    """
    Get or create the global Supabase client instance.
    
    Returns:
        SupabaseClient: Connected Supabase client instance
    """
    global _supabase_client
    
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY/SUPABASE_ANON_KEY must be set in environment")
        
        _supabase_client = create_client(url, key)
    
    return _supabase_client


class SupabaseService:
    """
    High-level service class for database operations.
    Provides convenient methods for common queries and operations.
    """
    
    def __init__(self):
        self.client = None
    
    def _ensure_connected(self):
        """Ensure database connection is established."""
        if self.client is None:
            self.client = get_client()
    
    # === Institution Methods ===
    
    def get_all_institutions(self, include_studies: bool = False) -> List[Dict[str, Any]]:
        """
        Get all educational institutions.
        
        Args:
            include_studies: Include related studies
            
        Returns:
            List of Institution dictionaries
        """
        self._ensure_connected()
        
        query = self.client.table('institutions').select('*')
        if include_studies:
            query = query.select('*, studies(*)')
        
        response = query.execute()
        return response.data
    
    def get_institution_by_id(
        self, 
        institution_id: str,
        include_studies: bool = True,
        include_events: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Get institution by ID with optional relations."""
        self._ensure_connected()
        
        select_fields = '*'
        if include_studies:
            select_fields += ', studies(*)'
        if include_events:
            select_fields += ', events(*)'
        
        response = self.client.table('institutions').select(select_fields).eq('id', institution_id).execute()
        return response.data[0] if response.data else None
    
    def search_institutions(self, query: str) -> List[Dict[str, Any]]:
        """
        Search institutions by name.
        
        Args:
            query: Search term
            
        Returns:
            List of matching institutions
        """
        self._ensure_connected()
        
        response = self.client.table('institutions').select('*').or_(
            f"name.ilike.%{query}%,short_name.ilike.%{query}%"
        ).execute()
        return response.data
    
    def create_institution(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new institution."""
        self._ensure_connected()
        response = self.client.table('institutions').insert(data).execute()
        return response.data[0]
    
    # === Study Methods ===
    
    def get_studies_by_institution(self, institution_id: str) -> List[Dict[str, Any]]:
        """Get all studies for a specific institution."""
        self._ensure_connected()
        response = self.client.table('studies').select('*').eq('institution_id', institution_id).execute()
        return response.data
    
    def search_studies(
        self, 
        query: Optional[str] = None,
        study_type: Optional[str] = None,
        institution_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search studies with optional filters.
        
        Args:
            query: Search term for title or keywords
            study_type: Filter by study type (Bachelor, MBO, Master)
            institution_id: Filter by institution
            
        Returns:
            List of matching studies
        """
        self._ensure_connected()
        
        q = self.client.table('studies').select('*, institutions(*)')
        
        if query:
            q = q.or_(f"title.ilike.%{query}%,keywords.ilike.%{query}%")
        
        if study_type:
            q = q.eq('type', study_type)
        
        if institution_id:
            q = q.eq('institution_id', institution_id)
        
        response = q.execute()
        return response.data
    
    def create_study(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new study program."""
        self._ensure_connected()
        response = self.client.table('studies').insert(data).execute()
        return response.data[0]
    
    # === Event Methods ===
    
    def get_upcoming_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get upcoming events sorted by date."""
        self._ensure_connected()
        response = (
            self.client.table('events')
            .select('*, institutions(*)')
            .gte('date', datetime.now().isoformat())
            .order('date', desc=False)
            .limit(limit)
            .execute()
        )
        return response.data
    
    def create_event(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new event."""
        self._ensure_connected()
        response = self.client.table('events').insert(data).execute()
        return response.data[0]
    
    # === User Methods ===
    
    def create_user(self, email: str, password: str, settings: Optional[Dict] = None) -> Dict[str, Any]:
        """Create a new user."""
        self._ensure_connected()
        data = {
            'email': email,
            'password': password,
            'settings': settings or {}
        }
        response = self.client.table('users').insert(data).execute()
        return response.data[0]
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        self._ensure_connected()
        response = self.client.table('users').select('*').eq('email', email).execute()
        return response.data[0] if response.data else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        self._ensure_connected()
        response = self.client.table('users').select('*').eq('id', user_id).execute()
        return response.data[0] if response.data else None
    
    # === Session Methods ===
    
    def create_session(
        self, 
        user_id: Optional[str] = None,
        anonymous_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new chat session.
        
        Args:
            user_id: Authenticated user ID (optional)
            anonymous_id: Anonymous session identifier (optional)
            
        Returns:
            Created Session dictionary
        """
        self._ensure_connected()
        data = {
            'user_id': user_id,
            'anonymous_id': anonymous_id
        }
        response = self.client.table('sessions').insert(data).execute()
        return response.data[0]
    
    def get_session_by_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID with messages."""
        self._ensure_connected()
        response = (
            self.client.table('sessions')
            .select('*, messages(*)')
            .eq('id', session_id)
            .execute()
        )
        return response.data[0] if response.data else None
    
    def get_user_sessions(self, user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent sessions for a user."""
        self._ensure_connected()
        response = (
            self.client.table('sessions')
            .select('*')
            .eq('user_id', user_id)
            .order('last_active', desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
    
    def update_session_activity(self, session_id: str):
        """Update session's last active timestamp."""
        self._ensure_connected()
        self.client.table('sessions').update({
            'last_active': datetime.now().isoformat()
        }).eq('id', session_id).execute()
    
    # === Message Methods ===
    
    def create_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a new message in a session.
        
        Args:
            session_id: Session ID
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata (response_time, is_out_of_domain, etc.)
            
        Returns:
            Created Message dictionary
        """
        self._ensure_connected()
        data = {
            'session_id': session_id,
            'role': role,
            'content': content,
            'metadata': metadata or {}
        }
        response = self.client.table('messages').insert(data).execute()
        return response.data[0]
    
    def get_session_messages(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a session."""
        self._ensure_connected()
        response = (
            self.client.table('messages')
            .select('*')
            .eq('session_id', session_id)
            .order('timestamp', desc=False)
            .execute()
        )
        return response.data
    
    def update_message_feedback(
        self,
        message_id: str,
        rating: Optional[int] = None,
        comment: Optional[str] = None
    ):
        """Update message feedback."""
        self._ensure_connected()
        feedback = {}
        if rating is not None:
            feedback['rating'] = rating
        if comment:
            feedback['comment'] = comment
        
        self.client.table('messages').update({
            'feedback': feedback
        }).eq('id', message_id).execute()
    
    # === Onboarding Methods ===
    
    def create_onboarding(
        self,
        session_id: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new onboarding record."""
        self._ensure_connected()
        data = {
            'session_id': session_id,
            'user_id': user_id
        }
        response = self.client.table('onboarding').insert(data).execute()
        return response.data[0]
    
    def get_onboarding_by_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get onboarding record for a session."""
        self._ensure_connected()
        response = (
            self.client.table('onboarding')
            .select('*, onboarding_answers(*, onboarding_questions(*))')
            .eq('session_id', session_id)
            .execute()
        )
        return response.data[0] if response.data else None
    
    def update_onboarding(
        self,
        onboarding_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update onboarding record."""
        self._ensure_connected()
        data['updated_at'] = datetime.now().isoformat()
        response = self.client.table('onboarding').update(data).eq('id', onboarding_id).execute()
        return response.data[0]
    
    def get_onboarding_questions(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """Get all onboarding questions."""
        self._ensure_connected()
        query = self.client.table('onboarding_questions').select('*')
        
        if active_only:
            query = query.eq('active', True)
        
        response = query.order('order_num', desc=False).execute()
        return response.data
    
    def save_onboarding_answer(
        self,
        onboarding_id: str,
        question_id: str,
        selected_option: str
    ) -> Dict[str, Any]:
        """Save an onboarding answer."""
        self._ensure_connected()
        data = {
            'onboarding_id': onboarding_id,
            'question_id': question_id,
            'selected_option': selected_option
        }
        response = self.client.table('onboarding_answers').insert(data).execute()
        return response.data[0]
    
    # === Reminder Methods ===
    
    def create_reminder(
        self,
        user_id: str,
        title: str,
        date: datetime,
        event_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create a new reminder."""
        self._ensure_connected()
        data = {
            'user_id': user_id,
            'title': title,
            'date': date.isoformat(),
            'event_id': event_id
        }
        response = self.client.table('reminders').insert(data).execute()
        return response.data[0]
    
    def get_user_reminders(
        self,
        user_id: str,
        include_sent: bool = False
    ) -> List[Dict[str, Any]]:
        """Get reminders for a user."""
        self._ensure_connected()
        query = self.client.table('reminders').select('*, events(*)').eq('user_id', user_id)
        
        if not include_sent:
            query = query.eq('sent', False)
        
        response = query.order('date', desc=False).execute()
        return response.data
    
    def get_pending_reminders(self, before_date: datetime) -> List[Dict[str, Any]]:
        """Get all pending reminders before a certain date."""
        self._ensure_connected()
        response = (
            self.client.table('reminders')
            .select('*, users(*), events(*)')
            .eq('sent', False)
            .lte('date', before_date.isoformat())
            .execute()
        )
        return response.data
    
    def mark_reminder_sent(self, reminder_id: str):
        """Mark a reminder as sent."""
        self._ensure_connected()
        self.client.table('reminders').update({'sent': True}).eq('id', reminder_id).execute()


# Singleton instance
_service_instance: Optional[SupabaseService] = None


def get_service() -> SupabaseService:
    """Get or create the singleton SupabaseService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = SupabaseService()
    return _service_instance
