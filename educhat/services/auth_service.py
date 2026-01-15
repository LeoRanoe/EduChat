"""
Authentication Service - Clean Implementation
Handles all authentication operations with Supabase Auth.
"""

import re
import asyncio
from typing import Dict, Optional, Tuple
from educhat.services.supabase_client import get_client


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class AuthService:
    """
    Service for handling authentication operations with Supabase.
    All methods return a standardized response dict.
    """
    
    def __init__(self):
        self._client = None
    
    @property
    def client(self):
        """Lazy-load Supabase client."""
        if self._client is None:
            self._client = get_client()
        return self._client
    
    # === Validation Methods ===
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate email format.
        Returns: (is_valid, error_message)
        """
        if not email or not email.strip():
            return False, "E-mailadres is verplicht"
        
        email = email.strip().lower()
        
        # Basic email regex
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Ongeldig e-mailadres formaat"
        
        return True, ""
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        Returns: (is_valid, error_message)
        """
        if not password:
            return False, "Wachtwoord is verplicht"
        
        if len(password) < 8:
            return False, "Wachtwoord moet minimaal 8 karakters bevatten"
        
        # Check for at least one letter and one number
        if not re.search(r'[a-zA-Z]', password):
            return False, "Wachtwoord moet minimaal één letter bevatten"
        
        if not re.search(r'[0-9]', password):
            return False, "Wachtwoord moet minimaal één cijfer bevatten"
        
        return True, ""
    
    def validate_name(self, name: str) -> Tuple[bool, str]:
        """
        Validate user name.
        Returns: (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Naam is verplicht"
        
        name = name.strip()
        
        if len(name) < 2:
            return False, "Naam moet minimaal 2 karakters bevatten"
        
        if len(name) > 50:
            return False, "Naam mag maximaal 50 karakters bevatten"
        
        return True, ""
    
    def validate_passwords_match(self, password: str, confirm: str) -> Tuple[bool, str]:
        """
        Validate that passwords match.
        Returns: (is_valid, error_message)
        """
        if password != confirm:
            return False, "Wachtwoorden komen niet overeen"
        return True, ""
    
    # === Core Auth Methods ===
    
    async def signup(self, email: str, password: str, name: str) -> Dict:
        """
        Register a new user with Supabase Auth.
        
        Args:
            email: User's email address
            password: User's password
            name: User's display name
            
        Returns:
            Dict with success status, user data, session, or error
        """
        try:
            # Validate inputs
            valid, error = self.validate_email(email)
            if not valid:
                return {"success": False, "error": error}
            
            valid, error = self.validate_password(password)
            if not valid:
                return {"success": False, "error": error}
            
            valid, error = self.validate_name(name)
            if not valid:
                return {"success": False, "error": error}
            
            # Clean inputs
            email = email.strip().lower()
            name = name.strip()
            
            # Sign up with Supabase Auth
            response = await asyncio.to_thread(
                lambda: self.client.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "name": name,
                            "display_name": name
                        }
                    }
                })
            )
            
            if response.user:
                # Check if email confirmation is required
                if response.user.email_confirmed_at is None and response.session is None:
                    return {
                        "success": True,
                        "requires_confirmation": True,
                        "message": "Controleer je e-mail om je account te bevestigen",
                        "user": {
                            "id": response.user.id,
                            "email": response.user.email,
                            "name": name
                        }
                    }
                
                return {
                    "success": True,
                    "requires_confirmation": False,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": name
                    },
                    "session": {
                        "access_token": response.session.access_token if response.session else None,
                        "refresh_token": response.session.refresh_token if response.session else None,
                        "expires_at": response.session.expires_at if response.session else None
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Account aanmaken mislukt. Probeer het opnieuw."
                }
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Parse common Supabase errors
            if "user already registered" in error_msg:
                return {"success": False, "error": "Dit e-mailadres is al geregistreerd"}
            elif "invalid email" in error_msg:
                return {"success": False, "error": "Ongeldig e-mailadres"}
            elif "password" in error_msg and "weak" in error_msg:
                return {"success": False, "error": "Wachtwoord is te zwak"}
            elif "rate limit" in error_msg or "too many" in error_msg:
                return {"success": False, "error": "Te veel pogingen. Wacht even en probeer opnieuw."}
            else:
                print(f"Signup error: {e}")
                return {"success": False, "error": "Er is een fout opgetreden. Probeer het opnieuw."}
    
    async def login(self, email: str, password: str) -> Dict:
        """
        Log in an existing user.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dict with success status, user data, session, or error
        """
        try:
            # Basic validation
            if not email or not email.strip():
                return {"success": False, "error": "E-mailadres is verplicht"}
            
            if not password:
                return {"success": False, "error": "Wachtwoord is verplicht"}
            
            # Clean email
            email = email.strip().lower()
            
            # Sign in with Supabase Auth
            response = await asyncio.to_thread(
                lambda: self.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
            )
            
            if response.user and response.session:
                # Get user metadata
                user_metadata = response.user.user_metadata or {}
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": user_metadata.get("name") or user_metadata.get("display_name") or email.split("@")[0]
                    },
                    "session": {
                        "access_token": response.session.access_token,
                        "refresh_token": response.session.refresh_token,
                        "expires_at": response.session.expires_at
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Ongeldig e-mailadres of wachtwoord"
                }
        
        except Exception as e:
            error_msg = str(e).lower()
            
            # Parse common errors
            if "invalid login credentials" in error_msg:
                return {"success": False, "error": "Ongeldig e-mailadres of wachtwoord"}
            elif "email not confirmed" in error_msg:
                return {"success": False, "error": "Je e-mailadres is nog niet bevestigd. Check je inbox en spam folder voor de bevestigingsmail, of klik hieronder om een nieuwe mail te ontvangen."}
            elif "rate limit" in error_msg or "too many" in error_msg:
                return {"success": False, "error": "Te veel inlogpogingen. Wacht even."}
            else:
                print(f"Login error: {e}")
                return {"success": False, "error": "Inloggen mislukt. Probeer het opnieuw."}
    
    async def logout(self) -> Dict:
        """
        Log out the current user.
        
        Returns:
            Dict with success status
        """
        try:
            await asyncio.to_thread(
                lambda: self.client.auth.sign_out()
            )
            return {"success": True}
        except Exception as e:
            print(f"Logout error: {e}")
            # Return success anyway - user should be logged out locally
            return {"success": True}
    
    async def get_current_user(self) -> Dict:
        """
        Get the currently authenticated user.
        
        Returns:
            Dict with success status and user data
        """
        try:
            response = await asyncio.to_thread(
                lambda: self.client.auth.get_user()
            )
            
            if response and response.user:
                user_metadata = response.user.user_metadata or {}
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": user_metadata.get("name") or user_metadata.get("display_name") or "User"
                    }
                }
            return {"success": False, "error": "No user session"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_session(self) -> Dict:
        """
        Get the current session.
        
        Returns:
            Dict with success status and session data
        """
        try:
            response = await asyncio.to_thread(
                lambda: self.client.auth.get_session()
            )
            
            if response:
                return {
                    "success": True,
                    "session": {
                        "access_token": response.access_token,
                        "refresh_token": response.refresh_token,
                        "expires_at": response.expires_at
                    }
                }
            return {"success": False, "error": "No active session"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def refresh_session(self, refresh_token: str) -> Dict:
        """
        Refresh the session using refresh token.
        
        Args:
            refresh_token: The refresh token
            
        Returns:
            Dict with success status and new session data
        """
        try:
            response = await asyncio.to_thread(
                lambda: self.client.auth.refresh_session(refresh_token)
            )
            
            if response.session:
                user_metadata = response.user.user_metadata or {} if response.user else {}
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id if response.user else None,
                        "email": response.user.email if response.user else None,
                        "name": user_metadata.get("name") or "User"
                    },
                    "session": {
                        "access_token": response.session.access_token,
                        "refresh_token": response.session.refresh_token,
                        "expires_at": response.session.expires_at
                    }
                }
            return {"success": False, "error": "Failed to refresh session"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def reset_password(self, email: str) -> Dict:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with success status
        """
        try:
            # Validate email
            valid, error = self.validate_email(email)
            if not valid:
                return {"success": False, "error": error}
            
            email = email.strip().lower()
            
            await asyncio.to_thread(
                lambda: self.client.auth.reset_password_email(email)
            )
            
            return {
                "success": True,
                "message": "Als dit e-mailadres bij ons bekend is, ontvang je een reset link."
            }
        except Exception as e:
            # Always return success to prevent email enumeration
            return {
                "success": True,
                "message": "Als dit e-mailadres bij ons bekend is, ontvang je een reset link."
            }
    
    async def resend_confirmation(self, email: str) -> Dict:
        """
        Resend confirmation email to user.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with success status
        """
        try:
            # Validate email
            valid, error = self.validate_email(email)
            if not valid:
                return {"success": False, "error": error}
            
            email = email.strip().lower()
            
            # Resend confirmation email using Supabase
            await asyncio.to_thread(
                lambda: self.client.auth.resend(
                    type="signup",
                    email=email
                )
            )
            
            return {
                "success": True,
                "message": "Bevestigingsmail opnieuw verzonden. Check je inbox en spam folder."
            }
        except Exception as e:
            error_msg = str(e).lower()
            print(f"Resend confirmation error: {e}")
            
            # Even on error, return success to avoid email enumeration
            return {
                "success": True,
                "message": "Als dit e-mailadres bij ons bekend is, ontvang je een bevestigingsmail."
            }


# Singleton instance
_auth_service: Optional[AuthService] = None


def get_auth_service() -> AuthService:
    """Get the singleton AuthService instance."""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service


# Legacy alias for backwards compatibility
auth_service = get_auth_service()

