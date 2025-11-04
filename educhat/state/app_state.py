"""Main application state for EduChat."""

import reflex as rx
from typing import List, Dict


class AppState(rx.State):
    """The main app state."""
    
    # Chat state
    messages: List[Dict] = []
    current_conversation_id: str = ""
    conversations: List[Dict] = []
    user_input: str = ""
    is_loading: bool = False
    
    def send_message(self):
        """Handle sending a message (to be implemented)."""
        pass
    
    def create_new_conversation(self):
        """Create a new conversation (to be implemented)."""
        pass
    
    def load_conversation(self, conversation_id: str):
        """Load a conversation by ID (to be implemented)."""
        pass
