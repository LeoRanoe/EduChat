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
    signup_name: str = ""
    remember_me: bool = False
    
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
    name_error: str = ""
    
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
    
    # === Reminders ===
    reminders: List[Dict[str, str]] = []
    show_reminder_modal: bool = False
    reminder_title: str = ""
    reminder_date: str = ""
    
    # === Events ===
    upcoming_events: List[Dict[str, str]] = []
    show_events_panel: bool = False
    
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
    
    def set_signup_name(self, value: str):
        """Set signup name."""
        self.signup_name = value
        self.name_error = ""
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
        
        # Validate name
        valid, error = self._validate_name(self.signup_name)
        if not valid:
            self.name_error = error
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
        self.signup_name = ""
        self._clear_errors()
    
    def _clear_errors(self):
        """Clear all error messages."""
        self.auth_error = ""
        self.auth_success = ""
        self.email_error = ""
        self.password_error = ""
        self.confirm_password_error = ""
        self.name_error = ""
    
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
            
            result = await auth_service.signup(
                self.signup_email.strip(),
                self.signup_password,
                self.signup_name.strip()
            )
            
            if result["success"]:
                # Check if email confirmation is required
                if result.get("requires_confirmation"):
                    self.auth_success = result.get("message", "Controleer je e-mail om je account te bevestigen")
                    self.auth_mode = "login"
                    self._clear_form()
                else:
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
                    
                    # Redirect to chat interface
                    yield rx.redirect("/chat")
            else:
                self.auth_error = result.get("error", "Registratie mislukt")
        
        except Exception as e:
            print(f"Signup error: {e}")
            self.auth_error = "Er is een fout opgetreden. Probeer het opnieuw."
        
        finally:
            self.auth_loading = False
    
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
            # Reset initialization flag
            if hasattr(self, '_initialized'):
                self._initialized = False
            # Redirect to landing page
            yield rx.redirect("/")
    
    async def continue_as_guest(self):
        """Continue as guest user."""
        self.is_guest = True
        self.is_authenticated = False
        self.user_id = f"guest_{uuid.uuid4().hex[:8]}"
        self.user_name = "Gast"
        self.show_auth_modal = False
        self._clear_form()
        
        # Reset initialization flag so chat initializes fresh
        if hasattr(self, '_initialized'):
            self._initialized = False
        
        # Show welcome toast
        self.toast_message = "Welkom als gast! Je hebt toegang tot beperkte functies."
        self.toast_type = "info"
        self.show_toast = True
        
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
    # Dark Mode
    # ==========================================================================
    
    def toggle_dark_mode(self):
        """Toggle dark mode."""
        self.dark_mode = not self.dark_mode
    
    # ==========================================================================
    # Events Panel
    # ==========================================================================
    
    def toggle_events_panel(self):
        """Toggle events panel visibility."""
        self.show_events_panel = not self.show_events_panel
    
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
    
    def toggle_reminder_modal(self):
        """Toggle reminder modal."""
        self.show_reminder_modal = not self.show_reminder_modal
        if not self.show_reminder_modal:
            self.reminder_title = ""
            self.reminder_date = ""
    
    def set_reminder_title(self, value: str):
        """Set reminder title."""
        self.reminder_title = value
    
    def set_reminder_date(self, value: str):
        """Set reminder date."""
        self.reminder_date = value
    
    async def create_reminder(self):
        """Create a new reminder."""
        if not self.reminder_title.strip() or not self.reminder_date:
            return
        
        new_reminder = {
            "id": str(uuid.uuid4()),
            "title": self.reminder_title.strip(),
            "date": self.reminder_date,
            "completed": "false",
            "created_at": datetime.now().isoformat()
        }
        
        if self.is_authenticated and self.user_id:
            try:
                from educhat.services.supabase_client import get_service
                db = get_service()
                date_obj = datetime.fromisoformat(self.reminder_date)
                db_reminder = db.create_reminder(
                    user_id=self.user_id,
                    title=self.reminder_title.strip(),
                    date=date_obj
                )
                new_reminder["id"] = str(db_reminder["id"])
            except Exception as e:
                print(f"Error saving reminder: {e}")
        
        self.reminders = [new_reminder] + list(self.reminders)
        self.show_reminder_modal = False
        self.reminder_title = ""
        self.reminder_date = ""
        yield
    
    async def create_reminder_from_event(self, event_id: str):
        """Create reminder from event."""
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
        
        self.reminders = [new_reminder] + list(self.reminders)
        
        # Show success toast
        self.toast_message = "Herinnering aangemaakt"
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
    
    def delete_reminder(self, reminder_id: str):
        """Delete a reminder."""
        self.reminders = [r for r in self.reminders if r["id"] != reminder_id]
    
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
                    "date": str(r.get("date", "")),
                    "completed": "true" if r.get("sent", False) else "false",
                    "created_at": str(r.get("created_at", ""))
                }
                for r in db_reminders
            ]
        except Exception as e:
            print(f"Error loading reminders: {e}")

