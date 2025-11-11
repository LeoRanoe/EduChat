"""Main application state for EduChat."""

import reflex as rx
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import asyncio
from educhat.services.ai_service import get_ai_service


class AppState(rx.State):
    """The main app state."""
    
    # Chat state
    messages: List[Dict] = []
    current_conversation_id: str = ""
    conversations: List[Dict] = []
    user_input: str = ""
    is_loading: bool = False
    
    # UI state
    sidebar_open: bool = False  # For mobile sidebar toggle
    
    # User context for AI (from onboarding)
    user_context: Optional[Dict] = None
    
    async def send_message(self):
        """Handle sending a message with AI integration."""
        if not self.user_input.strip():
            return
        
        # Add user message
        user_message = {
            "content": self.user_input,
            "is_user": True,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        self.messages.append(user_message)
        
        # Store input and clear
        user_input_text = self.user_input
        self.user_input = ""
        
        # Set loading state
        self.is_loading = True
        yield
        
        try:
            # Get AI service
            ai_service = get_ai_service()
            
            # Build conversation history (last 10 messages)
            conversation_history = []
            for msg in self.messages[-10:]:
                role = "user" if msg["is_user"] else "assistant"
                conversation_history.append({
                    "role": role,
                    "content": msg["content"]
                })
            
            # Call AI service with context
            ai_response = await ai_service.chat(
                message=user_input_text,
                conversation_history=conversation_history,
                context=self.user_context
            )
            
            # Add AI response
            bot_message = {
                "content": ai_response,
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
            self.messages.append(bot_message)
            
        except Exception as e:
            # Handle errors gracefully
            error_message = {
                "content": f"Sorry, er is iets misgegaan. Probeer het opnieuw. (Error: {str(e)})",
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
            self.messages.append(error_message)
        
        finally:
            self.is_loading = False
        
        # Update conversation title if exists
        if self.current_conversation_id:
            for conv in self.conversations:
                if conv["id"] == self.current_conversation_id:
                    conv["title"] = user_input_text[:50] + "..." if len(user_input_text) > 50 else user_input_text
                    break
        else:
            # Create new conversation
            self.create_new_conversation()
            if self.conversations:
                self.conversations[0]["title"] = user_input_text[:50] + "..." if len(user_input_text) > 50 else user_input_text
    
    def set_user_input(self, value: str):
        """Update user input value."""
        self.user_input = value
    
    def create_new_conversation(self):
        """Create a new conversation."""
        new_conv = {
            "id": str(uuid.uuid4()),
            "title": "Nieuw gesprek",
            "created_at": datetime.now().isoformat(),
        }
        self.conversations.insert(0, new_conv)
        self.current_conversation_id = new_conv["id"]
        self.messages = []
    
    def load_conversation(self, conversation_id: str):
        """Load a conversation by ID."""
        self.current_conversation_id = conversation_id
    
    def toggle_sidebar(self):
        """Toggle sidebar visibility (for mobile)."""
        self.sidebar_open = not self.sidebar_open
    
    def close_sidebar(self):
        """Close sidebar (for mobile)."""
        self.sidebar_open = False
    
    def set_user_context(self, context: Dict):
        """Set user context from onboarding data.
        
        Args:
            context: Dictionary containing onboarding data like:
                - education_level
                - age
                - favorite_subjects
                - future_plans
                - formality_preference
        """
        self.user_context = context
        # TODO: Load messages from database
        self.messages = []
