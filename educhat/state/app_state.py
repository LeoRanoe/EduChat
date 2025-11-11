"""Main application state for EduChat."""

import reflex as rx
from typing import List, Dict
from datetime import datetime
import uuid


class AppState(rx.State):
    """The main app state."""
    
    # Chat state
    messages: List[Dict] = []
    current_conversation_id: str = ""
    conversations: List[Dict] = []
    user_input: str = ""
    is_loading: bool = False
    
    def send_message(self):
        """Handle sending a message."""
        if not self.user_input.strip():
            return
        
        # Add user message
        user_message = {
            "content": self.user_input,
            "is_user": True,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        self.messages.append(user_message)
        
        # Clear input
        user_input_text = self.user_input
        self.user_input = ""
        
        # Set loading state
        self.is_loading = True
        
        # TODO: Call AI service here
        # For now, add a placeholder bot response
        yield
        
        import time
        time.sleep(1)  # Simulate AI processing
        
        bot_message = {
            "content": f"Bedankt voor je vraag: '{user_input_text}'. AI integratie komt binnenkort!",
            "is_user": False,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        self.messages.append(bot_message)
        self.is_loading = False
        
        # Update conversation if exists
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
        # TODO: Load messages from database
        self.messages = []
