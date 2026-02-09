"""Google Calendar Service for EduChat.

This service handles all interactions with Google Calendar API including:
- OAuth authentication and authorization
- Creating, updating, deleting events
- Fetching events and reminders
- Syncing educational events with Google Calendar
"""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarService:
    """Service for interacting with Google Calendar API."""
    
    def __init__(self, user_id: Optional[str] = None):
        """Initialize Google Calendar service.
        
        Args:
            user_id: User ID for storing separate credentials per user.
        """
        self.user_id = user_id or "default"
        self.service = None
        self.credentials = None
        self._credentials_dir = Path(__file__).parent.parent.parent / "credentials"
        self._credentials_dir.mkdir(exist_ok=True)
        
    def _get_token_path(self) -> Path:
        """Get the path to the token file for this user."""
        return self._credentials_dir / f"token_{self.user_id}.pickle"
    
    def _get_credentials_path(self) -> Path:
        """Get the path to the OAuth credentials file."""
        return self._credentials_dir / "credentials.json"
    
    def save_credentials_from_oauth(self, access_token: str, refresh_token: Optional[str] = None) -> bool:
        """Save Google OAuth credentials from Supabase provider tokens.
        
        Args:
            access_token: Google OAuth access token
            refresh_token: Google OAuth refresh token (optional)
            
        Returns:
            True if saved successfully
        """
        try:
            from google.oauth2.credentials import Credentials
            
            # Create credentials object from tokens
            creds = Credentials(
                token=access_token,
                refresh_token=refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=None,  # Not needed for token-based auth
                client_secret=None,
                scopes=SCOPES
            )
            
            # Save to pickle file
            token_path = self._get_token_path()
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
            
            print(f"[CALENDAR] Saved credentials to {token_path}")
            return True
        except Exception as e:
            print(f"[CALENDAR] Error saving credentials: {e}")
            return False
    
    def authenticate(self) -> bool:
        """Authenticate with Google Calendar API.
        
        Returns:
            True if authentication successful, False otherwise.
        """
        creds = None
        token_path = self._get_token_path()
        
        # Load existing token if available
        if token_path.exists():
            try:
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)
                print("[CALENDAR] Loaded existing credentials from file")
            except Exception as e:
                print(f"[CALENDAR] Error loading token: {e}")
        
        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    print("[CALENDAR] Refreshing expired credentials...")
                    creds.refresh(Request())
                    # Save refreshed credentials
                    with open(token_path, 'wb') as token:
                        pickle.dump(creds, token)
                    print("[CALENDAR] Credentials refreshed successfully")
                except Exception as e:
                    print(f"[CALENDAR] Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                # No saved credentials - user needs to authenticate via OAuth
                print("[CALENDAR] No valid credentials found")
                print("[CALENDAR] User should sign in with Google to grant calendar access")
                return False
        
        self.credentials = creds
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            print("[CALENDAR] Calendar service built successfully")
            return True
        except Exception as e:
            print(f"[CALENDAR] Error building calendar service: {e}")
            return False
    
    def create_event(
        self, 
        title: str, 
        start_time: datetime, 
        end_time: Optional[datetime] = None,
        description: str = "",
        location: str = "",
        calendar_id: str = 'primary',
        reminders: Optional[Dict] = None
    ) -> Optional[Dict]:
        """Create a new calendar event.
        
        Args:
            title: Event title
            start_time: Event start time
            end_time: Event end time (defaults to start_time + 1 hour)
            description: Event description
            location: Event location
            calendar_id: Calendar ID (default: 'primary')
            reminders: Reminder settings (e.g., {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 30}]})
        
        Returns:
            Created event dict or None if error
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        if not end_time:
            end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': title,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'America/Paramaribo',  # Suriname timezone
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'America/Paramaribo',
            },
        }
        
        if reminders:
            event['reminders'] = reminders
        else:
            # Default reminders: 1 day and 1 hour before
            event['reminders'] = {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 24 * 60},  # 1 day
                    {'method': 'popup', 'minutes': 60},       # 1 hour
                ],
            }
        
        try:
            event = self.service.events().insert(
                calendarId=calendar_id, 
                body=event
            ).execute()
            print(f"Event created: {event.get('htmlLink')}")
            return event
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def get_upcoming_events(
        self, 
        max_results: int = 50, 
        days_ahead: int = 90,
        calendar_id: str = 'primary'
    ) -> List[Dict]:
        """Get upcoming events from calendar.
        
        Args:
            max_results: Maximum number of events to return
            days_ahead: Number of days ahead to fetch events
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            List of event dictionaries
        """
        if not self.service:
            if not self.authenticate():
                return []
        
        try:
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            end_time = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
            
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=end_time,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            # Format events for our app
            formatted_events = []
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                formatted_event = {
                    'id': event['id'],
                    'title': event.get('summary', 'Untitled Event'),
                    'description': event.get('description', ''),
                    'location': event.get('location', ''),
                    'date': start,
                    'start_time': start,
                    'end_time': event['end'].get('dateTime', event['end'].get('date')),
                    'html_link': event.get('htmlLink', ''),
                    'source': 'google_calendar',
                    'institution': event.get('location', ''),  # Use location as institution
                }
                formatted_events.append(formatted_event)
            
            return formatted_events
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def update_event(
        self, 
        event_id: str, 
        updates: Dict[str, Any],
        calendar_id: str = 'primary'
    ) -> Optional[Dict]:
        """Update an existing event.
        
        Args:
            event_id: Event ID to update
            updates: Dictionary of fields to update
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            Updated event dict or None if error
        """
        if not self.service:
            if not self.authenticate():
                return None
        
        try:
            # First get the event
            event = self.service.events().get(
                calendarId=calendar_id, 
                eventId=event_id
            ).execute()
            
            # Apply updates
            for key, value in updates.items():
                if key == 'title':
                    event['summary'] = value
                elif key == 'start_time':
                    event['start'] = {
                        'dateTime': value.isoformat() if isinstance(value, datetime) else value,
                        'timeZone': 'America/Paramaribo',
                    }
                elif key == 'end_time':
                    event['end'] = {
                        'dateTime': value.isoformat() if isinstance(value, datetime) else value,
                        'timeZone': 'America/Paramaribo',
                    }
                else:
                    event[key] = value
            
            # Update the event
            updated_event = self.service.events().update(
                calendarId=calendar_id,
                eventId=event_id,
                body=event
            ).execute()
            
            print(f"Event updated: {updated_event.get('htmlLink')}")
            return updated_event
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
    
    def delete_event(
        self, 
        event_id: str,
        calendar_id: str = 'primary'
    ) -> bool:
        """Delete an event.
        
        Args:
            event_id: Event ID to delete
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            True if deleted successfully, False otherwise
        """
        if not self.service:
            if not self.authenticate():
                return False
        
        try:
            self.service.events().delete(
                calendarId=calendar_id,
                eventId=event_id
            ).execute()
            print(f"Event deleted: {event_id}")
            return True
            
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False
    
    def batch_create_events(self, events: List[Dict]) -> Dict[str, Any]:
        """Create multiple events in batch.
        
        Args:
            events: List of event dictionaries with keys: title, start_time, end_time, description, location
        
        Returns:
            Dictionary with 'success' count and 'failed' list
        """
        if not self.service:
            if not self.authenticate():
                return {'success': 0, 'failed': events}
        
        results = {'success': 0, 'failed': []}
        
        for event_data in events:
            event = self.create_event(
                title=event_data.get('title', 'Untitled Event'),
                start_time=event_data.get('start_time'),
                end_time=event_data.get('end_time'),
                description=event_data.get('description', ''),
                location=event_data.get('location', ''),
            )
            
            if event:
                results['success'] += 1
            else:
                results['failed'].append(event_data)
        
        return results


    def sync_events_to_calendar(
        self,
        events: List[Dict[str, Any]],
        calendar_id: str = 'primary'
    ) -> Dict[str, Any]:
        """Sync events from database to Google Calendar with deduplication.
        
        Args:
            events: List of events from database with keys: title, date, description, institution
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            Dictionary with sync statistics: {'created': int, 'skipped': int, 'errors': list}
        """
        if not self.service:
            if not self.authenticate():
                return {'created': 0, 'skipped': 0, 'errors': ['Authentication failed']}
        
        results = {'created': 0, 'skipped': 0, 'errors': []}
        
        # Get existing events from calendar for deduplication
        existing_events = self.get_upcoming_events(max_results=500, days_ahead=365)
        existing_titles = {event['title'].lower() for event in existing_events}
        
        for event_data in events:
            try:
                title = event_data.get('title', 'Untitled Event')
                
                # Skip if already exists (case-insensitive match)
                if title.lower() in existing_titles:
                    results['skipped'] += 1
                    continue
                
                # Parse date
                date_str = event_data.get('date') or event_data.get('start_time')
                if not date_str:
                    results['errors'].append(f"No date for event: {title}")
                    continue
                
                # Handle different date formats
                try:
                    if isinstance(date_str, str):
                        # Try parsing ISO format or other common formats
                        for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']:
                            try:
                                start_time = datetime.strptime(date_str.split('T')[0] if 'T' in date_str else date_str, fmt)
                                break
                            except ValueError:
                                continue
                        else:
                            # If no format matched, use current date + 7 days
                            start_time = datetime.now() + timedelta(days=7)
                    else:
                        start_time = date_str
                except Exception as e:
                    results['errors'].append(f"Invalid date for {title}: {e}")
                    continue
                
                # Set default end time (1 hour after start)
                end_time = start_time + timedelta(hours=1)
                
                # Create event
                description = event_data.get('description', '')
                institution = event_data.get('institution') or event_data.get('institution_id') or ''
                if institution and isinstance(institution, dict):
                    institution = institution.get('name', '')
                
                # Add source information to description
                full_description = description
                if institution:
                    full_description = f"📍 {institution}\n\n{description}"
                if event_data.get('url'):
                    full_description += f"\n\n🔗 {event_data['url']}"
                
                event = self.create_event(
                    title=title,
                    start_time=start_time,
                    end_time=end_time,
                    description=full_description,
                    location=str(institution),
                    calendar_id=calendar_id
                )
                
                if event:
                    results['created'] += 1
                    existing_titles.add(title.lower())  # Add to dedup set
                else:
                    results['errors'].append(f"Failed to create event: {title}")
                    
            except Exception as e:
                results['errors'].append(f"Error processing {event_data.get('title', 'unknown')}: {str(e)}")
        
        return results
    
    def sync_calendar_to_database(
        self,
        database_service,
        calendar_id: str = 'primary'
    ) -> Dict[str, Any]:
        """Sync events from Google Calendar back to database.
        
        Args:
            database_service: Supabase database service instance
            calendar_id: Calendar ID (default: 'primary')
        
        Returns:
            Dictionary with sync statistics
        """
        if not self.service:
            if not self.authenticate():
                return {'saved': 0, 'skipped': 0, 'errors': ['Authentication failed']}
        
        results = {'saved': 0, 'skipped': 0, 'errors': []}
        
        try:
            # Get events from Google Calendar
            calendar_events = self.get_upcoming_events(max_results=500, days_ahead=365, calendar_id=calendar_id)
            
            # Save to database
            for event in calendar_events:
                try:
                    # Check if event already exists in database
                    existing = database_service.client.table('events').select('id').eq(
                        'title', event['title']
                    ).execute()
                    
                    if existing.data:
                        results['skipped'] += 1
                        continue
                    
                    # Prepare event data for database
                    event_data = {
                        'title': event['title'],
                        'description': event.get('description', ''),
                        'date': event.get('start_time'),
                        'end_date': event.get('end_time'),
                        'event_type': 'general',
                        'url': event.get('html_link'),
                        'google_calendar_id': event.get('id'),
                        'synced_from_google': True,
                        'scraped_at': datetime.now().isoformat(),
                        'user_id': self.user_id,  # Add user_id for personal event privacy
                        'is_institutional': False,  # Personal calendar events are not institutional
                    }
                    
                    # Save to database
                    database_service.client.table('events').insert(event_data).execute()
                    results['saved'] += 1
                    
                except Exception as e:
                    results['errors'].append(f"Error saving {event.get('title', 'unknown')}: {str(e)}")
        
        except Exception as e:
            results['errors'].append(f"Error fetching calendar events: {str(e)}")
        
        return results


def get_calendar_service(user_id: Optional[str] = None) -> GoogleCalendarService:
    """Get or create a Google Calendar service instance.
    
    Args:
        user_id: User ID for storing separate credentials per user.
    
    Returns:
        GoogleCalendarService instance
    """
    return GoogleCalendarService(user_id=user_id)
