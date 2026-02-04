"""
Authentication State Management - Clean Implementation
Handles all authentication state for EduChat.
"""

import reflex as rx
from typing import Optional, Dict, List
from datetime import datetime
import uuid
import re


class AuthState(rx.State):
    """
    Authentication state for managing user sessions.
    Clean implementation with proper validation and session handling.
    """
    
    # === Core Auth State ===
    is_authenticated: bool = False
    is_guest: bool = False
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    
    # Session tokens (stored in state, can be persisted to localStorage via JS)
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    
    # === Language Settings ===
    language: str = "nl"  # "nl" for Dutch, "en" for English
    
    # === UI State ===
    show_auth_modal: bool = False
    auth_mode: str = "login"  # "login" or "signup"
    auth_loading: bool = False
    guest_banner_dismissed: bool = False
    
    # === Form Fields ===
    login_email: str = ""
    login_password: str = ""
    signup_email: str = ""
    signup_password: str = ""
    signup_confirm_password: str = ""
    signup_firstname: str = ""
    signup_lastname: str = ""
    remember_me: bool = False
    
    # === Google OAuth ===
    google_auth_loading: bool = False
    
    # Password visibility toggles
    show_login_password: bool = False
    show_signup_password: bool = False
    show_confirm_password: bool = False
    
    # === Error/Success Messages ===
    auth_error: str = ""
    auth_success: str = ""
    
    # Field-specific errors for better UX
    email_error: str = ""
    password_error: str = ""
    confirm_password_error: str = ""
    firstname_error: str = ""
    lastname_error: str = ""
    
    # === Email Confirmation ===
    email_needs_confirmation: bool = False
    pending_confirmation_email: str = ""
    resending_confirmation: bool = False
    
    # === Toast Notifications ===
    show_toast: bool = False
    toast_message: str = ""
    toast_type: str = "success"  # "success", "error", "info", "warning"
    
    # === User Settings ===
    dark_mode: bool = False
    show_settings_modal: bool = False
    
    # === Reminders ===
    reminders: List[Dict[str, str]] = []
    show_reminder_modal: bool = False
    reminder_title: str = ""
    reminder_date: str = ""
    reminder_time: str = "09:00"  # Default to 9 AM
    reminder_description: str = ""
    reminder_location: str = ""
    reminders_loaded: bool = False
    
    # === Events ===
    upcoming_events: List[Dict[str, str]] = []
    show_events_panel: bool = False
    events_was_open_before_calendar: bool = False
    
    # === Calendar ===
    show_calendar_view: bool = False
    calendar_view: str = "month"  # "month", "week", "day"
    calendar_year: int = datetime.now().year
    google_calendar_connected: bool = False  # Connection status indicator
    is_manual_syncing: bool = False  # Manual sync loading state
    calendar_month: int = datetime.now().month
    calendar_day: int = datetime.now().day
    calendar_events: List[Dict] = []
    selected_day_events: List[Dict] = []
    is_syncing_calendar: bool = False
    last_calendar_sync: str = ""
    is_loading: bool = False  # General loading state for various operations
    
    # === Google Calendar Sync ===
    show_google_events_modal: bool = False
    new_google_events: List[Dict] = []
    selected_google_events: List[str] = []  # List of event IDs
    all_google_events_selected: bool = False
    is_creating_reminders: bool = False
    sync_in_progress: bool = False
    sync_progress_current: int = 0
    sync_progress_total: int = 0
    
    # ==========================================================================
    # Language Methods
    # ==========================================================================
    
    def toggle_language(self):
        """Toggle between Dutch and English."""
        self.language = "en" if self.language == "nl" else "nl"
    
    def set_language(self, lang: str):
        """Set language directly."""
        if lang in ["nl", "en"]:
            self.language = lang
    
    @rx.var
    def is_dutch(self) -> bool:
        """Check if current language is Dutch."""
        return self.language == "nl"
    
    @rx.var
    def is_english(self) -> bool:
        """Check if current language is English."""
        return self.language == "en"
    
    @rx.var
    def current_calendar_month_year(self) -> str:
        """Get formatted month and year for calendar header."""
        months = ["Januari", "Februari", "Maart", "April", "Mei", "Juni",
                  "Juli", "Augustus", "September", "Oktober", "November", "December"]
        return f"{months[self.calendar_month - 1]} {self.calendar_year}"
    
    @rx.var
    def selected_day_formatted(self) -> str:
        """Get formatted selected day."""
        months = ["januari", "februari", "maart", "april", "mei", "juni",
                  "juli", "augustus", "september", "oktober", "november", "december"]
        return f"{self.calendar_day} {months[self.calendar_month - 1]} {self.calendar_year}"
    
    @rx.var
    def current_week_range(self) -> str:
        """Get formatted week range."""
        from datetime import timedelta
        selected_date = datetime(self.calendar_year, self.calendar_month, self.calendar_day)
        start_of_week = selected_date - timedelta(days=selected_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return f"{start_of_week.day} {start_of_week.strftime('%b')} - {end_of_week.day} {end_of_week.strftime('%b %Y')}"
    
    @rx.var
    def week_time_slots(self) -> List[Dict]:
        """Generate time slots for week view."""
        slots = []
        for hour in range(8, 20):  # 8 AM to 8 PM
            time_str = f"{hour:02d}:00"
            # Check if any event exists at this time
            has_event = False
            event_title = ""
            for event in self.selected_day_events:
                event_time = event.get("start_time", "")
                if event_time and event_time.startswith(f"{hour:02d}:"):
                    has_event = True
                    event_title = event.get("title", "")
                    break
            slots.append({
                "time": time_str,
                "has_event": has_event,
                "event_title": event_title
            })
        return slots
    
    @rx.var
    def calendar_days(self) -> List[Dict]:
        """Generate calendar days for current month."""
        from calendar import monthrange
        
        # Get number of days in current month
        _, num_days = monthrange(self.calendar_year, self.calendar_month)
        
        # Get first day of month (0 = Monday, 6 = Sunday)
        first_day = datetime(self.calendar_year, self.calendar_month, 1).weekday()
        
        # Get previous month days to fill
        if self.calendar_month == 1:
            prev_month = 12
            prev_year = self.calendar_year - 1
        else:
            prev_month = self.calendar_month - 1
            prev_year = self.calendar_year
        
        _, prev_month_days = monthrange(prev_year, prev_month)
        
        days = []
        
        # Add previous month days
        for i in range(first_day):
            day = prev_month_days - first_day + i + 1
            days.append({
                "day": day,
                "is_current_month": False,
                "is_today": False,
                "events_count": 0
            })
        
        # Add current month days
        today = datetime.now()
        for day in range(1, num_days + 1):
            is_today = (day == today.day and 
                       self.calendar_month == today.month and 
                       self.calendar_year == today.year)
            
            # Count events for this day
            events_count = sum(1 for event in self.calendar_events
                             if event.get("date", "").startswith(
                                 f"{self.calendar_year}-{self.calendar_month:02d}-{day:02d}"))
            
            days.append({
                "day": day,
                "is_current_month": True,
                "is_today": is_today,
                "events_count": events_count
            })
        
        # Add next month days to fill grid (usually 35 or 42 days)
        remaining = 35 - len(days)
        if remaining < 0:
            remaining = 42 - len(days)
        
        for day in range(1, remaining + 1):
            days.append({
                "day": day,
                "is_current_month": False,
                "is_today": False,
                "events_count": 0
            })
        
        return days
    
    # ==========================================================================
    # Form Input Handlers
    # ==========================================================================
    
    def set_login_email(self, value: str):
        """Set login email with validation."""
        self.login_email = value
        self.email_error = ""
        self.auth_error = ""
    
    def set_login_password(self, value: str):
        """Set login password."""
        self.login_password = value
        self.password_error = ""
        self.auth_error = ""
    
    def set_signup_email(self, value: str):
        """Set signup email with validation."""
        self.signup_email = value
        self.email_error = ""
        self.auth_error = ""
    
    def set_signup_password(self, value: str):
        """Set signup password with validation."""
        self.signup_password = value
        self.password_error = ""
        self.auth_error = ""
        # Clear confirm error if passwords now match
    
    def toggle_login_password(self):
        """Toggle login password visibility."""
        self.show_login_password = not self.show_login_password
    
    def toggle_signup_password(self):
        """Toggle signup password visibility."""
        self.show_signup_password = not self.show_signup_password
    
    def toggle_confirm_password(self):
        """Toggle confirm password visibility."""
        self.show_confirm_password = not self.show_confirm_password
    
    def set_signup_confirm_password(self, value: str):
        """Set signup confirm password with validation."""
        self.signup_confirm_password = value
        self.confirm_password_error = ""
        self.auth_error = ""
        # Clear confirm error if passwords now match
        if self.signup_password and value == self.signup_password:
            self.confirm_password_error = ""
    
    def set_signup_firstname(self, value: str):
        """Set signup firstname."""
        self.signup_firstname = value
        self.firstname_error = ""
        self.auth_error = ""
    
    def set_signup_lastname(self, value: str):
        """Set signup lastname."""
        self.signup_lastname = value
        self.lastname_error = ""
        self.auth_error = ""
    
    def toggle_remember_me(self):
        """Toggle remember me checkbox."""
        self.remember_me = not self.remember_me
    
    # ==========================================================================
    # Modal Control
    # ==========================================================================
    
    def open_auth_modal(self):
        """Open authentication modal."""
        self.show_auth_modal = True
        self.auth_mode = "login"
    
    def set_show_auth_modal(self, value: bool):
        """Set show auth modal state."""
        self.show_auth_modal = value
    
    def close_auth_modal(self):
        """Close authentication modal."""
        self.show_auth_modal = False
        self._clear_errors()
    
    # ==========================================================================
    # Validation Methods
    # ==========================================================================
    
    def _validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format."""
        if not email or not email.strip():
            return False, "E-mailadres is verplicht"
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email.strip()):
            return False, "Ongeldig e-mailadres"
        
        return True, ""
    
    def _validate_password(self, password: str) -> tuple[bool, str]:
        """Validate password strength."""
        if not password:
            return False, "Wachtwoord is verplicht"
        
        if len(password) < 8:
            return False, "Minimaal 8 karakters"
        
        return True, ""
    
    def _validate_name(self, name: str) -> tuple[bool, str]:
        """Validate user name."""
        if not name or not name.strip():
            return False, "Naam is verplicht"
        
        if len(name.strip()) < 2:
            return False, "Minimaal 2 karakters"
        
        return True, ""
    
    def _validate_login_form(self) -> bool:
        """Validate login form fields. Returns True if valid."""
        is_valid = True
        
        valid, error = self._validate_email(self.login_email)
        if not valid:
            self.email_error = error
            is_valid = False
        
        if not self.login_password:
            self.password_error = "Wachtwoord is verplicht"
            is_valid = False
        
        return is_valid
    
    def _validate_signup_form(self) -> bool:
        """Validate signup form fields. Returns True if valid."""
        is_valid = True
        
        # Validate email
        valid, error = self._validate_email(self.signup_email)
        if not valid:
            self.email_error = error
            is_valid = False
        
        # Validate firstname
        valid, error = self._validate_name(self.signup_firstname)
        if not valid:
            self.firstname_error = error if error != "Naam is verplicht" else "Voornaam is verplicht"
            is_valid = False
        
        # Validate lastname
        valid, error = self._validate_name(self.signup_lastname)
        if not valid:
            self.lastname_error = error if error != "Naam is verplicht" else "Achternaam is verplicht"
            is_valid = False
        
        # Validate password
        valid, error = self._validate_password(self.signup_password)
        if not valid:
            self.password_error = error
            is_valid = False
        
        # Validate password confirmation
        if not self.signup_confirm_password:
            self.confirm_password_error = "Bevestig je wachtwoord"
            is_valid = False
        elif self.signup_password != self.signup_confirm_password:
            self.confirm_password_error = "Wachtwoorden komen niet overeen"
            is_valid = False
        
        return is_valid
    
    # ==========================================================================
    # Modal Controls
    # ==========================================================================
    
    def open_auth_modal(self):
        """Open the auth modal."""
        self.show_auth_modal = True
        self.auth_mode = "login"
        self._clear_form()
    
    def close_auth_modal(self):
        """Close the auth modal."""
        self.show_auth_modal = False
        self._clear_form()
    
    def toggle_auth_modal(self):
        """Toggle auth modal visibility."""
        if self.show_auth_modal:
            self.close_auth_modal()
        else:
            self.open_auth_modal()
    
    def set_auth_mode(self, mode: str):
        """Switch between login and signup modes."""
        self.auth_mode = mode
        self._clear_errors()
    
    def _clear_form(self):
        """Clear all form fields and errors."""
        self.login_email = ""
        self.login_password = ""
        self.signup_email = ""
        self.signup_password = ""
        self.signup_confirm_password = ""
        self.signup_firstname = ""
        self.signup_lastname = ""
        self._clear_errors()
    
    def _clear_errors(self):
        """Clear all error messages."""
        self.auth_error = ""
        self.auth_success = ""
        self.email_error = ""
        self.password_error = ""
        self.confirm_password_error = ""
        self.firstname_error = ""
        self.lastname_error = ""
    
    # ==========================================================================
    # Authentication Actions
    # ==========================================================================
    
    async def login(self):
        """Handle user login."""
        # Clear previous errors
        self._clear_errors()
        
        # Validate form
        if not self._validate_login_form():
            return
        
        # Set loading state
        self.auth_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.login(
                self.login_email.strip(),
                self.login_password
            )
            
            if result["success"]:
                # Set authenticated state
                self.is_authenticated = True
                self.is_guest = False
                self.user_id = result["user"]["id"]
                self.user_email = result["user"]["email"]
                self.user_name = result["user"]["name"]
                self.access_token = result["session"]["access_token"]
                self.refresh_token = result["session"]["refresh_token"]
                
                # Clear any previous session data (e.g., guest conversations)
                if hasattr(self, 'conversations'):
                    self.conversations = []
                if hasattr(self, 'messages'):
                    self.messages = []
                if hasattr(self, 'current_conversation_id'):
                    self.current_conversation_id = ""
                if hasattr(self, '_conversations_loaded_for_user'):
                    self._conversations_loaded_for_user = ""
                
                # Close modal and clear form
                self.show_auth_modal = False
                self._clear_form()
                
                # Show success toast
                self.toast_message = f"Welkom terug, {self.user_name}!"
                self.toast_type = "success"
                self.show_toast = True
                
                # Reset initialization flag so chat reinitializes
                if hasattr(self, '_initialized'):
                    self._initialized = False
                
                # Load user data
                await self._load_user_data()
                
                # Yield state update before redirect
                yield
                
                # Redirect to chat interface
                yield rx.redirect("/chat")
            else:
                error_msg = result.get("error", "Inloggen mislukt")
                self.auth_error = error_msg
                
                # Check if email confirmation is needed
                if "e-mailadres" in error_msg.lower() or "bevestig" in error_msg.lower():
                    self.email_needs_confirmation = True
                    self.pending_confirmation_email = self.login_email.strip()
                else:
                    self.email_needs_confirmation = False
                    self.pending_confirmation_email = ""
        
        except Exception as e:
            print(f"Login error: {e}")
            self.auth_error = "Er is een fout opgetreden. Probeer het opnieuw."
        
        finally:
            self.auth_loading = False
    
    async def signup(self):
        """Handle user signup."""
        # Clear previous errors
        self._clear_errors()
        
        # Validate form
        if not self._validate_signup_form():
            return
        
        # Set loading state
        self.auth_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            # Combine firstname and lastname
            full_name = f"{self.signup_firstname.strip()} {self.signup_lastname.strip()}"
            
            result = await auth_service.signup(
                self.signup_email.strip(),
                self.signup_password,
                full_name,
                firstname=self.signup_firstname.strip(),
                lastname=self.signup_lastname.strip()
            )
            
            if result["success"]:
                # Check if email confirmation is required
                if result.get("requires_confirmation"):
                    self.auth_success = result.get("message", "Controleer je e-mail om je account te bevestigen")
                    self.auth_mode = "login"
                    self._clear_form()
                else:
                    # SECURITY: Reset chat state FIRST to prevent conversation leakage
                    if hasattr(self, '_reset_chat_state_for_user_switch'):
                        self._reset_chat_state_for_user_switch()
                    
                    # Set authenticated state
                    self.is_authenticated = True
                    self.is_guest = False
                    self.user_id = result["user"]["id"]
                    self.user_email = result["user"]["email"]
                    self.user_name = result["user"]["name"]
                    self.access_token = result["session"]["access_token"] if result.get("session") else None
                    self.refresh_token = result["session"]["refresh_token"] if result.get("session") else None
                    
                    # Close modal and clear form
                    self.show_auth_modal = False
                    self._clear_form()
                    
                    # Show success toast
                    self.toast_message = f"Account aangemaakt! Welkom, {self.user_name}!"
                    self.toast_type = "success"
                    self.show_toast = True
                    
                    # Redirect to onboarding for new users
                    yield rx.redirect("/onboarding")
            else:
                self.auth_error = result.get("error", "Registratie mislukt")
        
        except Exception as e:
            print(f"Signup error: {e}")
            self.auth_error = "Er is een fout opgetreden. Probeer het opnieuw."
        
        finally:
            self.auth_loading = False
    
    async def google_signin(self):
        """Handle Google OAuth sign-in."""
        self.google_auth_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.google_signin()
            
            if result["success"] and result.get("url"):
                # Redirect to Google OAuth URL (use window.open for external redirect)
                yield rx.redirect(result["url"])
            else:
                self.auth_error = result.get("error", "Google inloggen mislukt")
                self.google_auth_loading = False
        except Exception as e:
            print(f"Google sign-in error: {e}")
            self.auth_error = "Er is een fout opgetreden met Google inloggen"
            self.google_auth_loading = False
    
    async def handle_oauth_callback(self, code: str):
        """Handle OAuth callback from Google."""
        print(f"[OAuth Callback] Received code: {code[:20] if code else 'None'}...")
        
        # Validate code
        if not code or not isinstance(code, str):
            print(f"[OAuth Callback] Invalid code received: {type(code)}")
            self.auth_error = "Ongeldige authenticatie code"
            yield rx.redirect("/")
            return
            
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.handle_oauth_callback(code)
            print(f"[OAuth Callback] Result: {result.get('success') if isinstance(result, dict) else 'Invalid result'}")
            
            if isinstance(result, dict) and result.get("success") and result.get("user"):
                user = result["user"]
                session = result.get("session", {})
                
                # Set authenticated state
                self.is_authenticated = True
                self.is_guest = False
                self.user_id = user["id"]
                self.user_email = user["email"]
                self.user_name = user["name"]
                self.access_token = session.get("access_token")
                self.refresh_token = session.get("refresh_token")
                
                # Close modal
                self.show_auth_modal = False
                
                # Show success toast
                self.toast_message = f"Ingelogd met Google! Welkom, {self.user_name}!"
                self.toast_type = "success"
                self.show_toast = True
                
                # Load user data
                await self._load_user_data()
                
                # Redirect to chat
                yield rx.redirect("/chat")
            else:
                error_msg = result.get("error", "Google authenticatie mislukt") if isinstance(result, dict) else "Onverwachte fout"
                self.auth_error = error_msg
                yield rx.redirect("/")
        except Exception as e:
            print(f"OAuth callback error: {e}")
            import traceback
            traceback.print_exc()
            self.auth_error = "Er is een fout opgetreden met Google authenticatie"
            yield rx.redirect("/")
    
    async def logout(self):
        """Handle user logout."""
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            await auth_service.logout()
        except Exception as e:
            print(f"Logout error: {e}")
        finally:
            # Always clear local state
            self._clear_auth_state()
            # Reset loading state
            self.is_loading = False
            # Also reset is_guest
            self.is_guest = False
            # Clear auth modal
            self.show_auth_modal = False
            # Clear any errors
            self._clear_errors()
            # SECURITY: Reset chat state to prevent conversation leakage
            if hasattr(self, '_reset_chat_state_for_user_switch'):
                self._reset_chat_state_for_user_switch()
            # Clear conversations and messages to prevent data leak
            if hasattr(self, 'messages'):
                self.messages = []
            if hasattr(self, 'conversations'):
                self.conversations = []
            if hasattr(self, 'current_conversation_id'):
                self.current_conversation_id = ""
            # Yield state updates before redirect
            yield
            # Force full page reload with JavaScript to clear all client state
            yield rx.call_script("window.location.href = window.location.origin + '/'")
    
    async def continue_as_guest(self):
        """Continue as guest user."""
        # SECURITY: Reset chat state FIRST to prevent conversation leakage
        if hasattr(self, '_reset_chat_state_for_user_switch'):
            self._reset_chat_state_for_user_switch()
        
        self.is_guest = True
        self.is_authenticated = False
        self.user_id = f"guest_{uuid.uuid4().hex[:8]}"
        self.user_name = "Gast"
        self.show_auth_modal = False
        self._clear_form()
        
        # Reset initialization flag so chat initializes fresh
        if hasattr(self, '_initialized'):
            self._initialized = False
        
        # Don't show toast - guest banner will appear on chat page instead
        self.show_toast = False
        
        # Yield state update before redirect
        yield
        
        # Redirect to chat interface
        yield rx.redirect("/chat")
    
    def _clear_auth_state(self):
        """Clear all authentication state."""
        self.is_authenticated = False
        self.is_guest = False
        self.user_id = None
        self.user_email = None
        self.user_name = None
        self.access_token = None
        self.refresh_token = None
    
    async def _load_user_data(self):
        """Load user-specific data after login."""
        try:
            await self.load_reminders_from_db()
            await self.load_upcoming_events()
            # Check Google Calendar connection
            await self.check_google_calendar_connection()
            # Auto-sync with Google Calendar in background
            await self.auto_sync_google_calendar()
            # Load onboarding preferences (handled by AppState)
            if hasattr(self, 'load_onboarding_preferences'):
                await self.load_onboarding_preferences()
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    async def check_session(self):
        """Check if there's an existing session on app load."""
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.get_current_user()
            
            if result["success"]:
                self.is_authenticated = True
                self.is_guest = False
                self.user_id = result["user"]["id"]
                self.user_email = result["user"]["email"]
                self.user_name = result["user"]["name"]
                
                # Load user data
                await self._load_user_data()
        except Exception as e:
            print(f"Session check error: {e}")
    
    # ==========================================================================
    # Email Confirmation
    # ==========================================================================
    
    async def resend_confirmation_email(self):
        """Resend confirmation email to user."""
        if not self.pending_confirmation_email:
            return
        
        self.resending_confirmation = True
        self._clear_errors()
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.resend_confirmation(self.pending_confirmation_email)
            
            if result["success"]:
                self.auth_success = "Bevestigingsmail opnieuw verzonden. Check je inbox en spam folder."
                self.email_needs_confirmation = True
            else:
                self.auth_error = result.get("error", "Kon bevestigingsmail niet verzenden")
        except Exception as e:
            print(f"Resend confirmation error: {e}")
            self.auth_error = "Er is een fout opgetreden. Probeer het later opnieuw."
        finally:
            self.resending_confirmation = False
    
    # ==========================================================================
    # Password Reset
    # ==========================================================================
    
    async def request_password_reset(self):
        """Request password reset email."""
        email = self.login_email.strip() if self.auth_mode == "login" else self.signup_email.strip()
        
        if not email:
            self.email_error = "Voer je e-mailadres in"
            return
        
        self.auth_loading = True
        yield
        
        try:
            from educhat.services.auth_service import get_auth_service
            auth_service = get_auth_service()
            
            result = await auth_service.reset_password(email)
            
            self.auth_success = result.get("message", "Check je e-mail voor reset instructies")
        except Exception as e:
            print(f"Password reset error: {e}")
            self.auth_success = "Check je e-mail voor reset instructies"
        finally:
            self.auth_loading = False
    
    # ==========================================================================
    # Toast Notifications
    # ==========================================================================
    
    async def show_toast_notification(self, message: str, toast_type: str = "success"):
        """Show toast notification with auto-dismiss."""
        import asyncio
        
        self.toast_message = message
        self.toast_type = toast_type
        self.show_toast = True
        yield
        
        await asyncio.sleep(3)
        self.show_toast = False
        yield
    
    def hide_toast(self):
        """Hide toast notification."""
        self.show_toast = False
    
    def dismiss_guest_banner(self):
        """Dismiss the guest banner."""
        self.guest_banner_dismissed = True
    
    # ==========================================================================
    # Dark Mode - Uses Reflex's built-in color mode system
    # ==========================================================================
    
    # Note: dark_mode state var is kept for backward compatibility but the actual
    # theming is handled by Reflex's rx.toggle_color_mode which uses next-themes.
    # To toggle dark mode, use rx.toggle_color_mode event directly in on_click handlers.
    
    def toggle_settings_modal(self):
        """Toggle settings modal."""
        self.show_settings_modal = not self.show_settings_modal
    
    # ==========================================================================
    # Events Panel
    # ==========================================================================
    
    async def toggle_events_panel(self):
        """Toggle events panel visibility."""
        self.show_events_panel = not self.show_events_panel
        # Close calendar when opening events panel
        if self.show_events_panel:
            self.show_calendar_view = False
            if len(self.upcoming_events) == 0:
                await self.load_upcoming_events()
    
    async def load_upcoming_events(self):
        """Load upcoming events."""
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            events = db.get_upcoming_events(limit=10)
            
            self.upcoming_events = [
                {
                    "id": str(e.get("id", "")),
                    "title": e.get("title", "Evenement"),
                    "description": e.get("description", ""),
                    "date": str(e.get("date", "")),
                    "type": e.get("event_type", "general"),
                    "institution": e.get("institutions", {}).get("name", "") if e.get("institutions") else "",
                }
                for e in events
            ]
        except Exception as e:
            print(f"Error loading events: {e}")
            self._load_events_from_local()
    
    def _load_events_from_local(self):
        """Load events from local education data as fallback."""
        try:
            from educhat.services.education_service import EducationDataService
            edu_service = EducationDataService()
            dates = edu_service.get_important_dates()
            
            events = []
            now = datetime.now()
            current_year = now.year
            
            if "school_year" in dates:
                sy = dates["school_year"]
                events.append({
                    "id": "local-school-start",
                    "title": "Start Schooljaar",
                    "description": "Begin van het nieuwe schooljaar",
                    "date": f"{current_year}-10-01",
                    "type": "school_year",
                    "institution": "",
                })
            
            if "application_periods" in dates:
                for inst_type, period in dates["application_periods"].items():
                    events.append({
                        "id": f"local-inschrijving-{inst_type}",
                        "title": f"Inschrijvingen {inst_type.upper()}",
                        "description": f"Inschrijvingsperiode: {period}",
                        "date": f"{current_year}-04-01",
                        "type": "application",
                        "institution": "",
                    })
            
            self.upcoming_events = events[:10]
        except Exception as e:
            print(f"Error loading local events: {e}")
            self.upcoming_events = []
    
    # ==========================================================================
    # Reminders
    # ==========================================================================
    
    async def toggle_reminder_modal(self):
        """Toggle reminder modal."""
        self.show_reminder_modal = not self.show_reminder_modal
        if self.show_reminder_modal and not self.reminders_loaded:
            await self.load_reminders_from_db()
            self.reminders_loaded = True
        if not self.show_reminder_modal:
            self.reminder_title = ""
            self.reminder_date = ""
    
    def set_reminder_title(self, value: str):
        """Set reminder title."""
        self.reminder_title = value
    
    def set_reminder_date(self, value: str):
        """Set reminder date."""
        self.reminder_date = value
    
    def set_reminder_time(self, value: str):
        """Set reminder time."""
        self.reminder_time = value
    
    def set_reminder_description(self, value: str):
        """Set reminder description."""
        self.reminder_description = value
    
    def set_reminder_location(self, value: str):
        """Set reminder location."""
        self.reminder_location = value
    
    async def create_reminder(self):
        """Create a new reminder and sync to Google Calendar with real-time updates."""
        # Validate required fields
        if not self.reminder_title.strip():
            self.toast_message = "⚠ Titel is verplicht"
            self.toast_type = "error"
            self.show_toast = True
            return
        
        if not self.reminder_date or not self.reminder_date.strip():
            self.toast_message = "⚠ Datum is verplicht"
            self.toast_type = "error"
            self.show_toast = True
            return
        
        # Combine date and time
        datetime_str = f"{self.reminder_date}T{self.reminder_time}:00"
        
        temp_id = str(uuid.uuid4())
        new_reminder = {
            "id": temp_id,
            "title": self.reminder_title.strip(),
            "date": self.reminder_date,
            "time": self.reminder_time,
            "datetime": datetime_str,
            "description": self.reminder_description.strip(),
            "location": self.reminder_location.strip(),
            "completed": "false",
            "created_at": datetime.now().isoformat(),
            "sync_status": "pending",
            "google_calendar_event_id": "",
            "google_link": ""
        }
        
        # Add to UI immediately with pending status
        self.reminders = [new_reminder] + list(self.reminders)
        self.reminder_title = ""
        self.reminder_date = ""
        self.reminder_time = "09:00"
        self.reminder_description = ""
        self.reminder_location = ""
        self.show_reminder_modal = False
        yield
        
        # Save to database if authenticated
        db_id = temp_id
        if self.is_authenticated and self.user_id:
            try:
                from educhat.services.supabase_client import get_service
                db = get_service()
                # Parse datetime with time
                date_obj = datetime.fromisoformat(new_reminder["datetime"])
                db_reminder = db.create_reminder(
                    user_id=self.user_id,
                    title=new_reminder["title"],
                    date=date_obj,
                    description=new_reminder.get("description", ""),
                    location=new_reminder.get("location", "")
                )
                db_id = str(db_reminder["id"])
                
                # Update local reminder with real DB ID
                for i, r in enumerate(self.reminders):
                    if r["id"] == temp_id:
                        self.reminders[i]["id"] = db_id
                        break
                yield
                
            except Exception as e:
                print(f"Error saving reminder to database: {e}")
                # Show error but continue with sync attempt
        
        # Sync to Google Calendar with real-time status updates
        if self.is_authenticated and self.user_id:
            try:
                from educhat.services.sync_manager import get_sync_manager
                
                # Update status to syncing
                for i, r in enumerate(self.reminders):
                    if r["id"] == db_id:
                        self.reminders[i]["sync_status"] = "syncing"
                        break
                yield
                
                # Authenticate and sync
                sync_manager = get_sync_manager(self.user_id)
                if sync_manager.authenticate():
                    # Prepare reminder data for sync
                    reminder_data = {
                        "id": db_id,
                        "title": new_reminder["title"],
                        "date": self.reminder_date,
                        "time": new_reminder["time"],
                        "datetime": new_reminder["datetime"],
                        "description": new_reminder["description"] or "Herinnering aangemaakt via EduChat",
                        "location": new_reminder["location"]
                    }
                    
                    # Sync to Google Calendar
                    result = await sync_manager.sync_reminder_to_google(reminder_data)
                    
                    if result.success:
                        # Update database with Google Calendar event ID
                        from educhat.services.supabase_client import get_service
                        db = get_service()
                        db.client.table('reminders').update({
                            'google_calendar_event_id': result.google_event_id,
                            'sync_status': 'synced',
                            'last_sync_at': datetime.now().isoformat(),
                            'last_sync_direction': 'local_to_google'
                        }).eq('id', db_id).execute()
                        
                        # Update local state with success
                        sync_time = datetime.now().strftime("%H:%M")
                        for i, r in enumerate(self.reminders):
                            if r["id"] == db_id:
                                self.reminders[i]["sync_status"] = "synced"
                                self.reminders[i]["google_calendar_event_id"] = result.google_event_id
                                self.reminders[i]["last_sync_time"] = sync_time
                                # Get Google Calendar link
                                self.reminders[i]["google_link"] = f"https://calendar.google.com/calendar/event?eid={result.google_event_id}"
                                break
                        
                        # Show success toast
                        self.toast_message = f"✓ Herinnering aangemaakt en gesynchroniseerd ({sync_time})"
                        self.toast_type = "success"
                        self.show_toast = True
                    else:
                        # Update with error status
                        for i, r in enumerate(self.reminders):
                            if r["id"] == db_id:
                                self.reminders[i]["sync_status"] = "error"
                                self.reminders[i]["sync_error"] = result.error or "Unknown error"
                                break
                        
                        self.toast_message = f"✗ Sync mislukt: {result.error[:50] if result.error else 'Unknown error'}"
                        self.toast_type = "error"
                        self.show_toast = True
                else:
                    # Authentication failed
                    for i, r in enumerate(self.reminders):
                        if r["id"] == db_id:
                            self.reminders[i]["sync_status"] = "error"
                            self.reminders[i]["sync_error"] = "Google Calendar authenticatie mislukt"
                            break
                    
                    self.toast_message = "✗ Google Calendar authenticatie mislukt"
                    self.toast_type = "error"
                    self.show_toast = True
                    
            except Exception as e:
                print(f"Error syncing reminder to Google Calendar: {e}")
                import traceback
                traceback.print_exc()
                
                # Update with error status
                for i, r in enumerate(self.reminders):
                    if r["id"] == db_id:
                        self.reminders[i]["sync_status"] = "error"
                        self.reminders[i]["sync_error"] = str(e)
                        break
                
                self.toast_message = f"✗ Sync fout: {str(e)[:50]}"
                self.toast_type = "error"
                self.show_toast = True
        
        # Refresh calendar events to show the new reminder
        if self.show_calendar_view:
            await self.load_calendar_events()
        
        yield
    
    async def create_reminder_from_event(self, event_id: str):
        """Create reminder from event and sync to Google Calendar."""
        event = None
        for e in self.upcoming_events:
            if e["id"] == event_id:
                event = e
                break
        
        if not event:
            return
        
        new_reminder = {
            "id": str(uuid.uuid4()),
            "title": f"Herinnering: {event['title']}",
            "date": event.get("date", datetime.now().isoformat()[:10]),
            "completed": "false",
            "created_at": datetime.now().isoformat()
        }
        
        # Save to database if authenticated
        if self.is_authenticated and self.user_id:
            try:
                from educhat.services.supabase_client import get_service
                db = get_service()
                date_str = event.get("date", "")
                date_obj = datetime.fromisoformat(date_str.split("T")[0]) if date_str else datetime.now()
                db_reminder = db.create_reminder(
                    user_id=self.user_id,
                    title=new_reminder["title"],
                    date=date_obj
                )
                new_reminder["id"] = str(db_reminder["id"])
            except Exception as e:
                print(f"Error saving reminder: {e}")
        
        # Sync to Google Calendar if authenticated
        if self.is_authenticated:
            try:
                from educhat.services.google_calendar_service import get_calendar_service
                
                calendar_service = get_calendar_service(user_id=self.user_id)
                if calendar_service.authenticate():
                    date_str = event.get("date", "")
                    date_obj = datetime.fromisoformat(date_str.split("T")[0]) if date_str else datetime.now()
                    event_time = date_obj.replace(hour=9, minute=0, second=0)
                    
                    calendar_event = calendar_service.create_event(
                        title=f"🔔 {new_reminder['title']}",
                        start_time=event_time,
                        end_time=event_time + timedelta(hours=1),
                        description=f"Herinnering voor evenement: {event['title']}\n\n{event.get('description', '')}",
                        location=event.get('location', ''),
                        reminders={
                            'useDefault': False,
                            'overrides': [
                                {'method': 'popup', 'minutes': 24 * 60},
                                {'method': 'popup', 'minutes': 60},
                            ],
                        }
                    )
                    
                    if calendar_event:
                        new_reminder["calendar_event_id"] = calendar_event['id']
            except Exception as e:
                print(f"Error syncing reminder to Google Calendar: {e}")
        
        self.reminders = [new_reminder] + list(self.reminders)
        
        # Refresh calendar events to show the new reminder
        if self.show_calendar_view:
            await self.load_calendar_events()
        
        # Show success toast
        self.toast_message = "Herinnering aangemaakt en gesynchroniseerd"
        self.toast_type = "success"
        self.show_toast = True
        yield
    
    def toggle_reminder_complete(self, reminder_id: str):
        """Toggle reminder completion."""
        updated = []
        for r in self.reminders:
            if r["id"] == reminder_id:
                r["completed"] = "false" if r.get("completed") == "true" else "true"
            updated.append(r)
        self.reminders = updated
    
    async def delete_reminder(self, reminder_id: str):
        """Delete a reminder from database and Google Calendar with real-time updates."""
        # Find the reminder to get google_calendar_event_id
        reminder_to_delete = None
        for r in self.reminders:
            if r["id"] == reminder_id:
                reminder_to_delete = r
                break
        
        if not reminder_to_delete:
            return
        
        google_event_id = reminder_to_delete.get("google_calendar_event_id") or reminder_to_delete.get("calendar_event_id")
        
        # Delete from Google Calendar FIRST (if synced)
        google_delete_success = True
        if google_event_id and self.is_authenticated:
            try:
                from educhat.services.sync_manager import get_sync_manager
                
                sync_manager = get_sync_manager(self.user_id)
                if sync_manager.authenticate():
                    result = await sync_manager.delete_google_event(google_event_id)
                    
                    if result.success:
                        print(f"✓ Deleted reminder from Google Calendar: {google_event_id}")
                    else:
                        print(f"✗ Error deleting from Google Calendar: {result.error}")
                        google_delete_success = False
            except Exception as e:
                print(f"Error deleting reminder from Google Calendar: {e}")
                google_delete_success = False
        
        # Delete from database if authenticated
        if self.is_authenticated and self.user_id:
            try:
                from educhat.services.database import get_client
                db = get_client()
                db.table('reminders').delete().eq('id', reminder_id).execute()
                print(f"✓ Deleted reminder from database: {reminder_id}")
            except Exception as e:
                print(f"Error deleting reminder from database: {e}")
                import traceback
                traceback.print_exc()
        
        # Remove from local state
        self.reminders = [r for r in self.reminders if r["id"] != reminder_id]
        
        # Show success/warning toast
        if google_event_id:
            if google_delete_success:
                self.toast_message = "✓ Reminder verwijderd (inclusief Google Calendar)"
                self.toast_type = "success"
            else:
                self.toast_message = "⚠ Reminder verwijderd van app, maar niet van Google Calendar"
                self.toast_type = "warning"
        else:
            self.toast_message = "✓ Reminder verwijderd"
            self.toast_type = "success"
        self.show_toast = True
        
        # Refresh calendar events if calendar is open
        if self.show_calendar_view:
            await self.load_calendar_events()
        
        yield
    
    async def load_reminders_from_db(self):
        """Load reminders from database."""
        if not self.is_authenticated or not self.user_id:
            return
        
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            db_reminders = db.get_user_reminders(self.user_id)
            
            self.reminders = [
                {
                    "id": str(r["id"]),
                    "title": r["title"],
                    "date": str(r.get("date", "")).split('T')[0] if 'T' in str(r.get("date", "")) else str(r.get("date", "")),  # Extract date part
                    "time": str(r.get("date", "")).split('T')[1][:5] if 'T' in str(r.get("date", "")) else "09:00",  # Extract time part
                    "datetime": str(r.get("date", "")),  # Full timestamp
                    "description": r.get("description", ""),
                    "location": r.get("location", ""),
                    "completed": "true" if r.get("sent", False) else "false",
                    "created_at": str(r.get("created_at", "")),
                    "google_calendar_event_id": r.get("google_calendar_event_id", ""),
                    "sync_status": r.get("sync_status", "pending"),
                    "last_sync_at": str(r.get("last_sync_at", ""))[:16] if r.get("last_sync_at") else "",  # Format: YYYY-MM-DD HH:MM
                    "sync_error": r.get("sync_error", ""),
                    "google_link": f"https://calendar.google.com/calendar/event?eid={r.get('google_calendar_event_id', '')}" if r.get("google_calendar_event_id") else ""
                }
                for r in db_reminders
            ]
        except Exception as e:
            print(f"Error loading reminders: {e}")
    
    # ==========================================================================
    # Calendar Management
    # ==========================================================================
    
    def toggle_calendar_view(self):
        """Toggle calendar view visibility."""
        # If opening calendar, remember if events panel was open and close it
        if not self.show_calendar_view:
            self.events_was_open_before_calendar = self.show_events_panel
            self.show_events_panel = False
        # If closing calendar, reopen events panel if it was open before
        else:
            if self.events_was_open_before_calendar:
                self.show_events_panel = True
                self.events_was_open_before_calendar = False
        
        self.show_calendar_view = not self.show_calendar_view
    
    def set_calendar_view(self, view: str):
        """Set calendar view type (month/week/day)."""
        self.calendar_view = view
    
    def previous_month(self):
        """Navigate to previous month."""
        if self.calendar_month == 1:
            self.calendar_month = 12
            self.calendar_year -= 1
        else:
            self.calendar_month -= 1
    
    def next_month(self):
        """Navigate to next month."""
        if self.calendar_month == 12:
            self.calendar_month = 1
            self.calendar_year += 1
        else:
            self.calendar_month += 1
    
    def go_to_today(self):
        """Navigate to current month."""
        now = datetime.now()
        self.calendar_year = now.year
        self.calendar_month = now.month
        self.calendar_day = now.day
        self._update_selected_day_events()
    
    def previous_week(self):
        """Navigate to previous week."""
        from datetime import timedelta
        current = datetime(self.calendar_year, self.calendar_month, self.calendar_day)
        previous = current - timedelta(days=7)
        self.calendar_year = previous.year
        self.calendar_month = previous.month
        self.calendar_day = previous.day
        self._update_selected_day_events()
    
    def next_week(self):
        """Navigate to next week."""
        from datetime import timedelta
        current = datetime(self.calendar_year, self.calendar_month, self.calendar_day)
        next_date = current + timedelta(days=7)
        self.calendar_year = next_date.year
        self.calendar_month = next_date.month
        self.calendar_day = next_date.day
        self._update_selected_day_events()
    
    def previous_day(self):
        """Navigate to previous day."""
        from datetime import timedelta
        current = datetime(self.calendar_year, self.calendar_month, self.calendar_day)
        previous = current - timedelta(days=1)
        self.calendar_year = previous.year
        self.calendar_month = previous.month
        self.calendar_day = previous.day
        self._update_selected_day_events()
    
    def next_day(self):
        """Navigate to next day."""
        from datetime import timedelta
        current = datetime(self.calendar_year, self.calendar_month, self.calendar_day)
        next_date = current + timedelta(days=1)
        self.calendar_year = next_date.year
        self.calendar_month = next_date.month
        self.calendar_day = next_date.day
        self._update_selected_day_events()
    
    def select_calendar_day(self, day: int):
        """Select a day in the calendar."""
        self.calendar_day = day
        self._update_selected_day_events()
    
    def _update_selected_day_events(self):
        """Update events for selected day."""
        date_str = f"{self.calendar_year}-{self.calendar_month:02d}-{self.calendar_day:02d}"
        self.selected_day_events = [
            event for event in self.calendar_events
            if event.get("date", "").startswith(date_str)
        ]
    
    async def sync_calendar_events(self):
        """Bidirectional sync: Database ↔ Google Calendar.
        
        This method:
        1. Syncs EduChat database events TO Google Calendar
        2. Syncs Google Calendar events BACK to database
        3. Optionally scrapes new events from websites
        """
        if self.is_syncing_calendar:
            return
        
        self.is_syncing_calendar = True
        
        try:
            from educhat.services.google_calendar_service import get_calendar_service
            from educhat.services.supabase_client import get_service
            from educhat.services.event_scraper_service import scrape_and_sync_events
            from educhat.services.ai_service import get_ai_service
            import asyncio
            
            # Get event loop
            loop = asyncio.get_event_loop()
            
            # Get services
            calendar_service = get_calendar_service(user_id=self.user_id)
            db_service = get_service()
            
            # Authenticate with Google Calendar
            if not calendar_service.authenticate():
                self.toast_message = "Google Calendar authenticatie mislukt"
                self.toast_type = "error"
                self.show_toast = True
                return
            
            total_synced = 0
            total_scraped = 0
            
            # STEP 1: Sync DATABASE events TO Google Calendar
            print("[CALENDAR SYNC] Step 1: Syncing database events to Google Calendar...")
            db_events = db_service.get_upcoming_events(limit=100)
            if db_events:
                sync_to_calendar_result = await loop.run_in_executor(
                    None,
                    lambda: calendar_service.sync_events_to_calendar(db_events)
                )
                total_synced += sync_to_calendar_result['created']
                print(f"[CALENDAR SYNC] ✓ Created {sync_to_calendar_result['created']} events in Google Calendar")
                print(f"[CALENDAR SYNC] ⊘ Skipped {sync_to_calendar_result['skipped']} duplicate events")
                if sync_to_calendar_result['errors']:
                    print(f"[CALENDAR SYNC] ✗ Errors: {sync_to_calendar_result['errors'][:3]}")
            
            # STEP 2: Sync Google Calendar events BACK to database
            print("[CALENDAR SYNC] Step 2: Syncing Google Calendar events to database...")
            sync_to_db_result = await loop.run_in_executor(
                None,
                lambda: calendar_service.sync_calendar_to_database(db_service)
            )
            print(f"[CALENDAR SYNC] ✓ Saved {sync_to_db_result['saved']} events to database")
            print(f"[CALENDAR SYNC] ⊘ Skipped {sync_to_db_result['skipped']} existing events")
            
            # STEP 2.5: Sync deletions from Google Calendar
            print("[CALENDAR SYNC] Step 2.5: Checking for deleted events in Google Calendar...")
            await self.sync_deleted_events_from_google()
            
            # STEP 3 (Optional): Scrape new events from websites
            # Only do this if user explicitly requests it or on periodic basis
            # Commenting out to avoid slow sync times on every click
            # 
            # ai_service = get_ai_service()
            # scrape_result = await scrape_and_sync_events(
            #     ai_service=ai_service,
            #     calendar_service=calendar_service,
            #     user_institutions=None
            # )
            # total_scraped = scrape_result['scraped']
            # total_synced += scrape_result['synced']
            
            # Load all events from Google Calendar for display
            events = calendar_service.get_upcoming_events(max_results=100)
            
            # Update state
            self.calendar_events = events
            self.upcoming_events = events[:10]  # Top 10 for events panel
            self.last_calendar_sync = datetime.now().strftime("%H:%M")
            
            # Update selected day events
            self._update_selected_day_events()
            
            # Show success message
            message_parts = []
            if sync_to_calendar_result['created'] > 0:
                message_parts.append(f"{sync_to_calendar_result['created']} naar Google")
            if sync_to_db_result['saved'] > 0:
                message_parts.append(f"{sync_to_db_result['saved']} naar database")
            if total_scraped > 0:
                message_parts.append(f"{total_scraped} gescraped")
            
            if message_parts:
                self.toast_message = f"✓ Gesynchroniseerd: {', '.join(message_parts)}"
            else:
                self.toast_message = "✓ Kalender is up-to-date (geen nieuwe evenementen)"
            
            self.toast_type = "success"
            self.show_toast = True
            
        except Exception as e:
            print(f"[CALENDAR SYNC] Error: {e}")
            import traceback
            traceback.print_exc()
            self.toast_message = f"Fout bij synchroniseren: {str(e)[:100]}"
            self.toast_type = "error"
            self.show_toast = True
        finally:
            self.is_syncing_calendar = False
    
    async def sync_deleted_events_from_google(self):
        """Check for events deleted in Google Calendar and remove them from database."""
        if not self.is_authenticated or not self.user_id:
            return
        
        try:
            from educhat.services.google_calendar_service import get_calendar_service
            from educhat.services.database import get_client
            
            # Get all Google Calendar events
            calendar_service = get_calendar_service(user_id=self.user_id)
            if not calendar_service.authenticate():
                return
            
            google_events = calendar_service.get_upcoming_events(max_results=500)
            google_event_ids = {event.get('id') for event in google_events if event.get('id')}
            
            # Get all synced reminders from database
            db = get_client()
            reminders = db.table('reminders')\
                .select('id, google_calendar_event_id')\
                .eq('user_id', self.user_id)\
                .not_.is_('google_calendar_event_id', 'null')\
                .execute()
            
            # Check for deleted events
            deleted_count = 0
            if hasattr(reminders, 'data') and reminders.data:
                for reminder in reminders.data:
                    google_id = reminder.get('google_calendar_event_id')
                    if google_id and google_id not in google_event_ids:
                        # Event was deleted in Google Calendar
                        reminder_id = reminder['id']
                        db.table('reminders').delete().eq('id', reminder_id).execute()
                        
                        # Remove from local state
                        self.reminders = [r for r in self.reminders if r['id'] != str(reminder_id)]
                        deleted_count += 1
                        print(f"✓ Removed reminder {reminder_id} (deleted in Google Calendar)")
            
            if deleted_count > 0:
                print(f"✓ Synced {deleted_count} deletions from Google Calendar")
                
        except Exception as e:
            print(f"Error syncing deleted events from Google: {e}")
            import traceback
            traceback.print_exc()
    
    async def load_calendar_events(self):
        """Load events from Google Calendar and local reminders."""
        try:
            all_events = []
            
            # Load from Google Calendar
            from educhat.services.google_calendar_service import get_calendar_service
            calendar_service = get_calendar_service(user_id=self.user_id)
            
            if calendar_service.authenticate():
                google_events = calendar_service.get_upcoming_events(max_results=100)
                all_events.extend(google_events)
            
            # Load local reminders and add to calendar
            from educhat.services.database import get_client
            db = get_client()
            
            reminders = db.table("reminders")\
                .select("*")\
                .eq("user_id", self.user_id)\
                .execute()
            
            if hasattr(reminders, 'data') and reminders.data:
                for reminder in reminders.data:
                    # Extract date from timestamp for calendar display
                    date_value = reminder.get('date', '')
                    if 'T' in date_value:
                        # Extract YYYY-MM-DD from YYYY-MM-DDTHH:MM:SS
                        display_date = date_value.split('T')[0]
                        # Extract time HH:MM
                        start_time = date_value.split('T')[1][:5]
                    else:
                        display_date = date_value
                        start_time = "09:00"
                    
                    # Format last_sync_at for display
                    last_sync_display = ""
                    if reminder.get('last_sync_at'):
                        try:
                            sync_time = str(reminder.get('last_sync_at', ''))
                            # Extract time HH:MM from timestamp
                            if 'T' in sync_time:
                                last_sync_display = sync_time.split('T')[1][:5]
                            elif ' ' in sync_time:
                                last_sync_display = sync_time.split(' ')[1][:5]
                        except:
                            last_sync_display = ""
                    
                    # Convert reminder to calendar event format
                    reminder_event = {
                        "id": f"reminder_{reminder['id']}",
                        "title": f"🔔 {reminder['title']}",
                        "date": display_date,  # Use clean date for calendar matching
                        "datetime": date_value,  # Keep full timestamp
                        "start_time": start_time,  # Add start_time for display
                        "description": reminder.get('description', ''),
                        "location": reminder.get('location', ''),
                        "type": "reminder",
                        "sync_status": reminder.get('sync_status', 'pending'),
                        "google_calendar_event_id": reminder.get('google_calendar_event_id', ''),
                        "last_sync_at": last_sync_display
                    }
                    all_events.append(reminder_event)
            
            self.calendar_events = all_events
            self.upcoming_events = all_events[:10]
            self._update_selected_day_events()
            
            # Also check for deletions from Google Calendar
            await self.sync_deleted_events_from_google()
            
        except Exception as e:
            print(f"Error loading calendar events: {e}")
            import traceback
            traceback.print_exc()
    
    def show_event_details(self, event_id: str):
        """Show event details (to be implemented)."""
        pass
    
    # ==========================================================================
    # Google Calendar Import
    # ==========================================================================
    
    def toggle_google_event_selection(self, event_id: str):
        """Toggle selection of a Google Calendar event.
        
        Args:
            event_id: Google Calendar event ID
        """
        if event_id in self.selected_google_events:
            self.selected_google_events = [
                eid for eid in self.selected_google_events if eid != event_id
            ]
        else:
            self.selected_google_events = list(self.selected_google_events) + [event_id]
        
        # Update all selected state
        self.all_google_events_selected = (
            len(self.selected_google_events) == len(self.new_google_events)
            and len(self.new_google_events) > 0
        )
    
    def toggle_all_google_events(self, checked: bool):
        """Toggle selection of all Google Calendar events.
        
        Args:
            checked: Whether to select all
        """
        if checked:
            self.selected_google_events = [e["id"] for e in self.new_google_events]
            self.all_google_events_selected = True
        else:
            self.selected_google_events = []
            self.all_google_events_selected = False
    
    def close_google_events_modal(self):
        """Close Google events import modal."""
        self.show_google_events_modal = False
        self.selected_google_events = []
        self.all_google_events_selected = False
    
    async def create_reminders_from_google_events(self):
        """Create reminders from selected Google Calendar events."""
        if not self.selected_google_events:
            return
        
        self.is_creating_reminders = True
        self.sync_progress_current = 0
        self.sync_progress_total = len(self.selected_google_events)
        yield
        
        try:
            from educhat.services.supabase_client import get_service
            
            db = get_service()
            created_count = 0
            
            for event_id in self.selected_google_events:
                # Find the event
                event = None
                for e in self.new_google_events:
                    if e["id"] == event_id:
                        event = e
                        break
                
                if not event:
                    continue
                
                # Create reminder in database
                try:
                    date_str = event.get("date", event.get("start_time", ""))
                    if "T" in date_str:
                        date_obj = datetime.fromisoformat(date_str.replace("Z", ""))
                    else:
                        date_obj = datetime.fromisoformat(date_str)
                    
                    db_reminder = db.create_reminder(
                        user_id=self.user_id,
                        title=event.get("title", "Reminder"),
                        date=date_obj
                    )
                    
                    # Update reminder with Google Calendar event ID
                    db.client.table('reminders').update({
                        'google_calendar_event_id': event_id,
                        'sync_status': 'synced',
                        'last_sync_at': datetime.now().isoformat(),
                        'last_sync_direction': 'google_to_local'
                    }).eq('id', db_reminder["id"]).execute()
                    
                    # Add to local state
                    new_reminder = {
                        "id": str(db_reminder["id"]),
                        "title": event.get("title", "Reminder"),
                        "date": date_str,
                        "completed": "false",
                        "created_at": datetime.now().isoformat(),
                        "google_calendar_event_id": event_id,
                        "sync_status": "synced",
                        "google_link": event.get("html_link", "")
                    }
                    self.reminders = [new_reminder] + list(self.reminders)
                    created_count += 1
                    self.sync_progress_current += 1
                    yield
                    
                except Exception as e:
                    print(f"Error creating reminder from Google event: {e}")
                    continue
            
            # Close modal and show success
            self.show_google_events_modal = False
            self.selected_google_events = []
            self.all_google_events_selected = False
            
            # Refresh calendar if open
            if self.show_calendar_view:
                await self.load_calendar_events()
            
            # Show toast
            self.toast_message = f"✓ {created_count} herinneringen aangemaakt"
            self.toast_type = "success"
            self.show_toast = True
            
        except Exception as e:
            print(f"Error creating reminders from Google events: {e}")
            self.toast_message = f"Fout bij aanmaken herinneringen: {str(e)[:50]}"
            self.toast_type = "error"
            self.show_toast = True
        finally:
            self.is_creating_reminders = False
            self.sync_progress_current = 0
            self.sync_progress_total = 0
            yield
    
    async def check_google_calendar_connection(self):
        """Check if Google Calendar is connected and authenticated."""
        if not self.is_authenticated or not self.user_id:
            self.google_calendar_connected = False
            return
        
        try:
            from educhat.services.google_calendar_service import get_calendar_service
            
            calendar_service = get_calendar_service(user_id=self.user_id)
            self.google_calendar_connected = calendar_service.authenticate()
            
            if self.google_calendar_connected:
                print("[GOOGLE CALENDAR] ✓ Connected and authenticated")
            else:
                print("[GOOGLE CALENDAR] ✗ Not connected or authentication failed")
                
        except Exception as e:
            print(f"[GOOGLE CALENDAR] Connection check error: {e}")
            self.google_calendar_connected = False
    
    async def manual_sync_calendar(self):
        """Manual sync triggered by user button click."""
        if not self.is_authenticated or not self.user_id:
            self.toast_message = "Log in om te synchroniseren met Google Calendar"
            self.toast_type = "warning"
            self.show_toast = True
            return
        
        if self.is_manual_syncing:
            return
        
        self.is_manual_syncing = True
        yield
        
        try:
            # Check connection first
            await self.check_google_calendar_connection()
            
            if not self.google_calendar_connected:
                self.toast_message = "Google Calendar niet verbonden. Configureer eerst je credentials."
                self.toast_type = "error"
                self.show_toast = True
                return
            
            # Perform full bidirectional sync
            await self.sync_calendar_events()
            
        except Exception as e:
            print(f"[MANUAL SYNC] Error: {e}")
            self.toast_message = f"Synchronisatie mislukt: {str(e)[:80]}"
            self.toast_type = "error"
            self.show_toast = True
        finally:
            self.is_manual_syncing = False
            yield
    
    async def auto_sync_google_calendar(self):
        """Auto-sync with Google Calendar on app launch (background, non-blocking)."""
        if not self.is_authenticated or not self.user_id:
            return
        
        try:
            from educhat.services.sync_manager import get_sync_manager
            from educhat.services.supabase_client import get_service
            
            sync_manager = get_sync_manager(self.user_id)
            
            # Authenticate silently
            if not sync_manager.authenticate():
                print("[AUTO-SYNC] Google Calendar authentication not configured or failed")
                self.google_calendar_connected = False
                return
            
            self.google_calendar_connected = True
            
            print("[AUTO-SYNC] Starting background sync with Google Calendar...")
            
            # Fetch events from Google Calendar
            google_events, error = await sync_manager.fetch_google_events(days_ahead=90)
            
            if error:
                print(f"[AUTO-SYNC] Error fetching Google events: {error}")
                return
            
            # Get local data
            db = get_service()
            local_events = db.get_upcoming_events(limit=200)
            
            # Compare and find new events
            comparison = sync_manager.compare_with_local(
                google_events,
                list(self.reminders),
                local_events
            )
            
            new_events = comparison['new_in_google']
            
            if new_events:
                print(f"[AUTO-SYNC] Found {len(new_events)} new events in Google Calendar")
                
                # Store new events for user to review
                self.new_google_events = new_events
                
                # Show modal asking user which to import
                self.show_google_events_modal = True
                self.last_calendar_sync = datetime.now().strftime("%H:%M")
            else:
                print("[AUTO-SYNC] No new events found. Calendar is up to date.")
                self.last_calendar_sync = datetime.now().strftime("%H:%M")
                
        except Exception as e:
            print(f"[AUTO-SYNC] Error during auto-sync: {e}")
            import traceback
            traceback.print_exc()

