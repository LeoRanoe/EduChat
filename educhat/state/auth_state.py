"""Authentication state management for EduChat."""

import reflex as rx
from typing import Optional, Dict
from datetime import datetime
import uuid


class AuthState(rx.State):
    """Authentication state for managing user sessions."""
    
    # User authentication
    is_authenticated: bool = False
    is_guest: bool = False
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    session_token: Optional[str] = None
    
    # Auth UI state
    show_auth_modal: bool = False
    auth_mode: str = "login"  # "login" or "signup"
    auth_error: str = ""
    auth_loading: bool = False
    guest_banner_dismissed: bool = False
    
    # Toast notifications
    show_toast: bool = False
    toast_message: str = ""
    toast_type: str = "success"  # "success", "error", "info", "warning"
    
    # Form fields
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    name: str = ""
    
    # Remember session
    remember_me: bool = False
    
    def toggle_auth_modal(self):
        """Toggle authentication modal visibility."""
        self.show_auth_modal = not self.show_auth_modal
        if not self.show_auth_modal:
            self.clear_auth_form()
    
    def set_auth_mode(self, mode: str):
        """Switch between login and signup modes."""
        self.auth_mode = mode
        self.auth_error = ""
        self.clear_auth_form()
    
    def clear_auth_form(self):
        """Clear all form fields."""
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.name = ""
        self.auth_error = ""
    
    def set_email(self, value: str):
        """Set email field."""
        self.email = value
        self.auth_error = ""
    
    def set_password(self, value: str):
        """Set password field."""
        self.password = value
        self.auth_error = ""
    
    def set_confirm_password(self, value: str):
        """Set confirm password field."""
        self.confirm_password = value
        self.auth_error = ""
    
    def set_name(self, value: str):
        """Set name field."""
        self.name = value
        self.auth_error = ""
    
    def toggle_remember_me(self):
        """Toggle remember me checkbox."""
        self.remember_me = not self.remember_me
    
    def dismiss_guest_banner(self):
        """Dismiss the guest banner."""
        self.guest_banner_dismissed = True
    
    async def show_toast_notification(self, message: str, toast_type: str = "success"):
        """Show a toast notification that auto-dismisses after 3 seconds."""
        import asyncio
        
        self.toast_message = message
        self.toast_type = toast_type
        self.show_toast = True
        yield
        
        # Auto-dismiss after 3 seconds
        await asyncio.sleep(3)
        self.show_toast = False
        yield
    
    def hide_toast(self):
        """Hide the toast notification."""
        self.show_toast = False
    
    def continue_as_guest(self):
        """Continue using the app as a guest user."""
        self.is_guest = True
        self.is_authenticated = False
        self.user_id = f"guest_{uuid.uuid4().hex[:8]}"
        self.user_name = "Guest User"
        self.show_auth_modal = False
        # Navigate to chat
        return rx.redirect("/chat")
    
    async def login(self):
        """Handle user login."""
        from educhat.services.auth_service import auth_service
        
        # Validate inputs
        if not self.email or not self.password:
            self.auth_error = "Please fill in all fields"
            return
        
        self.auth_loading = True
        self.auth_error = ""
        yield
        
        try:
            # Attempt login
            result = await auth_service.login(self.email, self.password)
            
            if result["success"]:
                # Set authenticated user
                self.is_authenticated = True
                self.is_guest = False
                self.user_id = result["user"]["id"]
                self.user_email = result["user"]["email"]
                self.user_name = result["user"].get("name", result["user"]["email"].split("@")[0])
                self.session_token = result["session"]["access_token"]
                
                # Show success toast
                self.show_toast_notification(f"Welcome back, {self.user_name}!", "success")
                
                # Close modal
                self.show_auth_modal = False
                self.clear_auth_form()
                
                # Store session if remember me is checked
                if self.remember_me:
                    self._store_session()
                
                # Load user's conversations (only for AppState)
                if hasattr(self, 'load_conversations_from_db'):
                    await self.load_conversations_from_db()
                
                # Navigate to chat - yield instead of return in async generator
                yield rx.redirect("/chat")
                return
            else:
                self.auth_error = result.get("error", "Login failed. Please check your credentials.")
        
        except Exception as e:
            self.auth_error = "An error occurred during login. Please try again."
        
        finally:
            self.auth_loading = False
    
    async def signup(self):
        """Handle user signup."""
        from educhat.services.auth_service import auth_service
        
        # Validate inputs
        if not self.email or not self.password or not self.name:
            self.auth_error = "Please fill in all fields"
            return
        
        if self.password != self.confirm_password:
            self.auth_error = "Passwords do not match"
            return
        
        if len(self.password) < 8:
            self.auth_error = "Password must be at least 8 characters"
            return
        
        self.auth_loading = True
        self.auth_error = ""
        yield
        
        try:
            # Attempt signup
            result = await auth_service.signup(self.email, self.password, self.name)
            
            if result["success"]:
                # Set authenticated user
                self.is_authenticated = True
                self.is_guest = False
                self.user_id = result["user"]["id"]
                self.user_email = result["user"]["email"]
                self.user_name = result["user"].get("name", self.name)
                self.session_token = result["session"]["access_token"]
                
                # Show success toast
                self.show_toast_notification(f"Account created successfully! Welcome, {self.user_name}!", "success")
                
                # Close modal
                self.show_auth_modal = False
                self.clear_auth_form()
                
                # Store session
                if self.remember_me:
                    self._store_session()
                
                # Load user's conversations (only for AppState, will be empty for new users)
                if hasattr(self, 'load_conversations_from_db'):
                    await self.load_conversations_from_db()
                
                # Navigate to chat - yield instead of return in async generator
                yield rx.redirect("/chat")
                return
            else:
                self.auth_error = result.get("error", "Signup failed. Please try again.")
        
        except Exception as e:
            self.auth_error = "An error occurred during signup. Please try again."
        
        finally:
            self.auth_loading = False
    
    async def logout(self):
        """Handle user logout."""
        from educhat.services.auth_service import auth_service
        
        try:
            # Clear session on server
            if self.session_token:
                await auth_service.logout(self.session_token)
            
            # Clear local state
            self.is_authenticated = False
            self.is_guest = False
            self.user_id = None
            self.user_email = None
            self.user_name = None
            self.session_token = None
            
            # Clear stored session
            self._clear_session()
            
            # Redirect to landing
            yield rx.redirect("/")
            return
        
        except Exception as e:
            # Force logout even on error
            self.is_authenticated = False
            self.is_guest = False
            self.user_id = None
            self.user_email = None
            self.user_name = None
            self.session_token = None
    
    def _store_session(self):
        """Store session in browser storage (simplified)."""
        # In a real implementation, you'd use rx.LocalStorage or cookies
        # For now, we'll use rx state vars that persist
        pass
    
    def _clear_session(self):
        """Clear stored session."""
        pass
    
    async def restore_session(self):
        """Restore user session from stored token."""
        from educhat.services.auth_service import auth_service
        
        # Check for stored session
        # In real implementation, retrieve from localStorage/cookies
        stored_token = None  # Placeholder
        
        if stored_token:
            try:
                result = await auth_service.validate_session(stored_token)
                
                if result["success"]:
                    self.is_authenticated = True
                    self.is_guest = False
                    self.user_id = result["user"]["id"]
                    self.user_email = result["user"]["email"]
                    self.user_name = result["user"].get("name", "User")
                    self.session_token = stored_token
                    return
            
            except Exception:
                pass
        
        # No valid session, show auth modal
        self.show_auth_modal = True

