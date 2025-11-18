"""Authentication service using Supabase Auth."""

from typing import Dict, Optional
from educhat.services.supabase_client import get_client
import asyncio


class AuthService:
    """Service for handling authentication operations with Supabase."""
    
    def __init__(self):
        self.client = get_client()
    
    async def signup(self, email: str, password: str, name: str) -> Dict:
        """
        Sign up a new user.
        
        Args:
            email: User's email address
            password: User's password
            name: User's display name
            
        Returns:
            Dict with success status, user data, and session
        """
        try:
            # Sign up with Supabase Auth
            response = await asyncio.to_thread(
                lambda: self.client.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data": {
                            "name": name,
                            "created_at": str(asyncio.get_event_loop().time())
                        }
                    }
                })
            )
            
            if response.user:
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": name
                    },
                    "session": {
                        "access_token": response.session.access_token if response.session else None,
                        "refresh_token": response.session.refresh_token if response.session else None
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to create account"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def login(self, email: str, password: str) -> Dict:
        """
        Log in an existing user.
        
        Args:
            email: User's email address
            password: User's password
            
        Returns:
            Dict with success status, user data, and session
        """
        try:
            # Sign in with Supabase Auth
            response = await asyncio.to_thread(
                lambda: self.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
            )
            
            if response.user:
                # Get user metadata
                user_metadata = response.user.user_metadata or {}
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": user_metadata.get("name", email.split("@")[0])
                    },
                    "session": {
                        "access_token": response.session.access_token,
                        "refresh_token": response.session.refresh_token
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
        
        except Exception as e:
            error_message = str(e)
            if "Invalid login credentials" in error_message:
                return {
                    "success": False,
                    "error": "Invalid email or password"
                }
            return {
                "success": False,
                "error": "Login failed. Please try again."
            }
    
    async def logout(self, session_token: str) -> Dict:
        """
        Log out the current user.
        
        Args:
            session_token: Current session token
            
        Returns:
            Dict with success status
        """
        try:
            await asyncio.to_thread(
                lambda: self.client.auth.sign_out()
            )
            
            return {
                "success": True
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def validate_session(self, session_token: str) -> Dict:
        """
        Validate and restore a session from token.
        
        Args:
            session_token: Session access token
            
        Returns:
            Dict with success status and user data
        """
        try:
            # Get current user with token
            response = await asyncio.to_thread(
                lambda: self.client.auth.get_user(session_token)
            )
            
            if response.user:
                user_metadata = response.user.user_metadata or {}
                
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": user_metadata.get("name", "User")
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Invalid session"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def reset_password(self, email: str) -> Dict:
        """
        Send password reset email.
        
        Args:
            email: User's email address
            
        Returns:
            Dict with success status
        """
        try:
            await asyncio.to_thread(
                lambda: self.client.auth.reset_password_email(email)
            )
            
            return {
                "success": True,
                "message": "Password reset email sent"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_user(self, user_id: str, data: Dict) -> Dict:
        """
        Update user profile.
        
        Args:
            user_id: User's ID
            data: Data to update (name, email, etc.)
            
        Returns:
            Dict with success status
        """
        try:
            response = await asyncio.to_thread(
                lambda: self.client.auth.update_user({
                    "data": data
                })
            )
            
            if response.user:
                return {
                    "success": True,
                    "user": {
                        "id": response.user.id,
                        "email": response.user.email,
                        "name": data.get("name", "User")
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update user"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Global auth service instance
auth_service = AuthService()

