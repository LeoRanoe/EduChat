"""Sync Manager Service for EduChat.

Handles bidirectional synchronization between EduChat database and Google Calendar
with real-time updates, concurrent requests, and conflict resolution.
"""

import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
from concurrent.futures import ThreadPoolExecutor
import traceback

from educhat.services.google_calendar_service import GoogleCalendarService


class SyncResult:
    """Result of a sync operation."""
    
    def __init__(self, success: bool, item_id: str, google_event_id: Optional[str] = None, 
                 error: Optional[str] = None, sync_direction: str = "local_to_google"):
        self.success = success
        self.item_id = item_id
        self.google_event_id = google_event_id
        self.error = error
        self.sync_direction = sync_direction
        self.synced_at = datetime.now() if success else None


class SyncManager:
    """Manages all Google Calendar synchronization operations."""
    
    def __init__(self, user_id: str):
        """Initialize sync manager.
        
        Args:
            user_id: User ID for Google Calendar authentication
        """
        self.user_id = user_id
        self.calendar_service = GoogleCalendarService(user_id=user_id)
        self._executor = ThreadPoolExecutor(max_workers=5)  # Concurrent API requests
        
    def authenticate(self) -> bool:
        """Authenticate with Google Calendar.
        
        Returns:
            True if authenticated, False otherwise
        """
        return self.calendar_service.authenticate()
    
    async def sync_reminder_to_google(self, reminder: Dict[str, Any]) -> SyncResult:
        """Sync a single reminder to Google Calendar.
        
        Args:
            reminder: Reminder dict with title, date/datetime, description, etc.
            
        Returns:
            SyncResult with success status and Google Calendar event ID
        """
        try:
            # Get datetime - prefer 'datetime' field, fallback to 'date'
            datetime_str = reminder.get("datetime", "") or reminder.get("date", "")
            if not datetime_str:
                return SyncResult(False, reminder.get("id", ""), error="Missing date")
            
            # Convert to datetime
            if "T" in datetime_str:
                # Full datetime provided
                event_time = datetime.fromisoformat(datetime_str.replace("Z", ""))
            else:
                # Only date provided, use time if available
                date_obj = datetime.fromisoformat(datetime_str)
                time_str = reminder.get("time", "09:00")
                hour, minute = map(int, time_str.split(":"))
                event_time = date_obj.replace(hour=hour, minute=minute, second=0)
            
            # Create event in Google Calendar
            loop = asyncio.get_event_loop()
            event = await loop.run_in_executor(
                self._executor,
                self._create_google_event,
                reminder,
                event_time
            )
            
            if event:
                return SyncResult(
                    success=True,
                    item_id=reminder.get("id", ""),
                    google_event_id=event['id'],
                    sync_direction="local_to_google"
                )
            else:
                return SyncResult(False, reminder.get("id", ""), error="Failed to create event")
                
        except Exception as e:
            print(f"Error syncing reminder to Google: {e}")
            traceback.print_exc()
            return SyncResult(False, reminder.get("id", ""), error=str(e))
    
    def _create_google_event(self, reminder: Dict[str, Any], event_time: datetime) -> Optional[Dict]:
        """Create Google Calendar event (runs in thread pool).
        
        Args:
            reminder: Reminder data
            event_time: Already parsed datetime for the event
            
        Returns:
            Created event dict or None
        """
        try:
            title = f"🔔 {reminder.get('title', 'Reminder')}"
            description = reminder.get('description', 'Herinnering aangemaakt via EduChat')
            
            return self.calendar_service.create_event(
                title=title,
                start_time=event_time,
                end_time=event_time + timedelta(hours=1),
                description=description,
                location=reminder.get('location', ''),
                reminders={
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 24 * 60},  # 1 day before
                        {'method': 'popup', 'minutes': 60},       # 1 hour before
                    ],
                }
            )
        except Exception as e:
            print(f"Error creating Google event: {e}")
            return None
    
    async def sync_reminders_to_google(self, reminders: List[Dict[str, Any]]) -> List[SyncResult]:
        """Sync multiple reminders to Google Calendar concurrently.
        
        Args:
            reminders: List of reminder dicts
            
        Returns:
            List of SyncResult for each reminder
        """
        if not reminders:
            return []
        
        # Sync all reminders concurrently
        tasks = [self.sync_reminder_to_google(r) for r in reminders]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions
        sync_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                sync_results.append(SyncResult(
                    False, 
                    reminders[i].get("id", ""),
                    error=str(result)
                ))
            else:
                sync_results.append(result)
        
        return sync_results
    
    async def update_google_event(self, google_event_id: str, updates: Dict[str, Any]) -> SyncResult:
        """Update an existing Google Calendar event.
        
        Args:
            google_event_id: Google Calendar event ID
            updates: Dict of fields to update (title, date, description, location)
            
        Returns:
            SyncResult with success status
        """
        try:
            loop = asyncio.get_event_loop()
            updated_event = await loop.run_in_executor(
                self._executor,
                self.calendar_service.update_event,
                google_event_id,
                updates
            )
            
            if updated_event:
                return SyncResult(
                    success=True,
                    item_id=google_event_id,
                    google_event_id=google_event_id,
                    sync_direction="local_to_google"
                )
            else:
                return SyncResult(False, google_event_id, error="Update failed")
                
        except Exception as e:
            print(f"Error updating Google event: {e}")
            return SyncResult(False, google_event_id, error=str(e))
    
    async def delete_google_event(self, google_event_id: str) -> SyncResult:
        """Delete an event from Google Calendar.
        
        Args:
            google_event_id: Google Calendar event ID
            
        Returns:
            SyncResult with success status
        """
        try:
            loop = asyncio.get_event_loop()
            success = await loop.run_in_executor(
                self._executor,
                self.calendar_service.delete_event,
                google_event_id
            )
            
            if success:
                return SyncResult(
                    success=True,
                    item_id=google_event_id,
                    google_event_id=google_event_id,
                    sync_direction="local_to_google"
                )
            else:
                return SyncResult(False, google_event_id, error="Delete failed")
                
        except Exception as e:
            print(f"Error deleting Google event: {e}")
            return SyncResult(False, google_event_id, error=str(e))
    
    async def fetch_google_events(self, days_ahead: int = 90) -> Tuple[List[Dict], Optional[str]]:
        """Fetch events from Google Calendar.
        
        Args:
            days_ahead: Number of days ahead to fetch
            
        Returns:
            Tuple of (events list, error message if any)
        """
        try:
            loop = asyncio.get_event_loop()
            events = await loop.run_in_executor(
                self._executor,
                self.calendar_service.get_upcoming_events,
                100,  # max_results
                days_ahead
            )
            
            return (events, None)
            
        except Exception as e:
            print(f"Error fetching Google events: {e}")
            return ([], str(e))
    
    async def sync_event_to_google(self, event: Dict[str, Any]) -> SyncResult:
        """Sync a single event to Google Calendar.
        
        Args:
            event: Event dict with title, date, description, location, etc.
            
        Returns:
            SyncResult with success status and Google Calendar event ID
        """
        try:
            # Parse date
            date_str = event.get("date", "")
            if not date_str:
                return SyncResult(False, event.get("id", ""), error="Missing date")
            
            if "T" in date_str:
                event_time = datetime.fromisoformat(date_str.replace("Z", ""))
            else:
                date_obj = datetime.fromisoformat(date_str)
                event_time = date_obj.replace(hour=10, minute=0, second=0)
            
            # Create event in Google Calendar
            loop = asyncio.get_event_loop()
            google_event = await loop.run_in_executor(
                self._executor,
                self._create_google_event_from_event,
                event
            )
            
            if google_event:
                return SyncResult(
                    success=True,
                    item_id=event.get("id", ""),
                    google_event_id=google_event['id'],
                    sync_direction="local_to_google"
                )
            else:
                return SyncResult(False, event.get("id", ""), error="Failed to create event")
                
        except Exception as e:
            print(f"Error syncing event to Google: {e}")
            return SyncResult(False, event.get("id", ""), error=str(e))
    
    def _create_google_event_from_event(self, event: Dict[str, Any]) -> Optional[Dict]:
        """Create Google Calendar event from EduChat event (runs in thread pool).
        
        Args:
            event: Event data
            
        Returns:
            Created event dict or None
        """
        try:
            date_str = event.get("date", "")
            if "T" in date_str:
                event_time = datetime.fromisoformat(date_str.replace("Z", ""))
            else:
                date_obj = datetime.fromisoformat(date_str)
                event_time = date_obj.replace(hour=10, minute=0, second=0)
            
            return self.calendar_service.create_event(
                title=event.get('title', 'Event'),
                start_time=event_time,
                end_time=event_time + timedelta(hours=2),
                description=event.get('description', ''),
                location=event.get('location', event.get('institution', '')),
            )
        except Exception as e:
            print(f"Error creating Google event from event: {e}")
            return None
    
    def compare_with_local(self, google_events: List[Dict], 
                          local_reminders: List[Dict],
                          local_events: List[Dict]) -> Dict[str, List[Dict]]:
        """Compare Google Calendar events with local data.
        
        Args:
            google_events: Events from Google Calendar
            local_reminders: Reminders from local database
            local_events: Events from local database
            
        Returns:
            Dict with 'new_in_google', 'updated_in_google', 'deleted_locally' lists
        """
        # Create lookup maps
        local_google_ids = set()
        
        # Map reminder google IDs
        for reminder in local_reminders:
            google_id = reminder.get("google_calendar_event_id")
            if google_id:
                local_google_ids.add(google_id)
        
        # Map event google IDs
        for event in local_events:
            google_id = event.get("google_calendar_event_id")
            if google_id:
                local_google_ids.add(google_id)
        
        # Find new events in Google Calendar
        new_in_google = []
        for g_event in google_events:
            if g_event['id'] not in local_google_ids:
                new_in_google.append(g_event)
        
        return {
            'new_in_google': new_in_google,
            'updated_in_google': [],  # TODO: Implement update detection
            'deleted_locally': []      # TODO: Implement deletion detection
        }


def get_sync_manager(user_id: str) -> SyncManager:
    """Get or create sync manager instance.
    
    Args:
        user_id: User ID
        
    Returns:
        SyncManager instance
    """
    return SyncManager(user_id)
