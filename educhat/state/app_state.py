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
    
    # Pagination state
    messages_page_size: int = 30
    messages_current_page: int = 1
    has_more_messages: bool = False
    
    # UI state
    sidebar_open: bool = False  # For mobile sidebar toggle
    sidebar_collapsed: bool = False  # For desktop sidebar collapse
    
    # User context for AI (from onboarding)
    user_context: Optional[Dict] = None
    
    # Performance metrics
    last_response_time: float = 0.0
    
    async def send_message(self):
        """Handle sending a message with AI integration."""
        if not self.user_input.strip():
            return
        
        # Start performance tracking
        import time
        start_time = time.time()
        
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
            
            # Call AI service with context (run in executor to avoid blocking)
            loop = asyncio.get_event_loop()
            ai_response = await loop.run_in_executor(
                None,
                lambda: ai_service.chat(
                    message=user_input_text,
                    conversation_history=conversation_history,
                    context=self.user_context
                )
            )
            
            # Track response time
            self.last_response_time = time.time() - start_time
            
            # Add AI response
            bot_message = {
                "content": ai_response,
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
            }
            self.messages.append(bot_message)
            
        except TimeoutError:
            # Handle timeout specifically
            error_message = {
                "content": "Het antwoord duurt te lang. Probeer je vraag opnieuw te stellen of maak deze korter.",
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
                "is_error": True,
            }
            self.messages.append(error_message)
        except Exception as e:
            # Handle errors gracefully
            error_message = {
                "content": "Sorry, er is iets misgegaan. Probeer het opnieuw of stel een andere vraag.",
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
    
    def toggle_sidebar_collapse(self):
        """Toggle sidebar collapse (for desktop)."""
        self.sidebar_collapsed = not self.sidebar_collapsed
    
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
    
    async def send_quick_action(self, prompt: str):
        """Handle quick action button click.
        
        Args:
            prompt: Pre-defined prompt text
        """
        self.user_input = prompt
        # send_message is an async generator, so we need to iterate through it
        async for _ in self.send_message():
            pass
    
    async def handle_message_feedback(self, message_index: int, feedback_type: str):
        """Handle user feedback on a message (like/dislike).
        
        Args:
            message_index: Index of the message in messages list
            feedback_type: 'like' or 'dislike'
        """
        if 0 <= message_index < len(self.messages):
            # Update message with feedback
            self.messages[message_index]["feedback"] = feedback_type
            self.messages[message_index]["feedback_timestamp"] = datetime.now().isoformat()
            
            # TODO: Store feedback in database for analytics
            # await self.supabase_client.store_feedback(
            #     conversation_id=self.current_conversation_id,
            #     message_index=message_index,
            #     feedback_type=feedback_type
            # )
            
            # Visual confirmation
            yield
    
    async def copy_message(self, message_index: int):
        """Copy message content to clipboard.
        
        Args:
            message_index: Index of the message to copy
        """
        if 0 <= message_index < len(self.messages):
            # Note: Actual clipboard copy handled by browser
            pass
    
    async def regenerate_response(self, message_index: int):
        """Regenerate AI response for the last user message.
        
        Args:
            message_index: Index of the bot message to regenerate
        """
        if message_index > 0 and message_index < len(self.messages):
            # Find the previous user message
            user_msg_idx = message_index - 1
            if user_msg_idx >= 0 and self.messages[user_msg_idx]["is_user"]:
                # Remove the old bot response
                self.messages.pop(message_index)
                
                # Re-send the user message
                self.user_input = self.messages[user_msg_idx]["content"]
                # Use return to chain to send_message generator
                return self.send_message()
    
    async def load_more_messages(self):
        """Load older messages (pagination)."""
        if not self.has_more_messages:
            return
        
        self.messages_current_page += 1
        
        # TODO: Load messages from database with pagination
        # offset = (self.messages_current_page - 1) * self.messages_page_size
        # older_messages = await self.database.get_messages(
        #     conversation_id=self.current_conversation_id,
        #     limit=self.messages_page_size,
        #     offset=offset
        # )
        # self.messages = older_messages + self.messages
        # self.has_more_messages = len(older_messages) == self.messages_page_size
        
        yield
    
    def get_visible_messages(self) -> List[Dict]:
        """Get paginated visible messages.
        
        Returns:
            List of messages for current page
        """
        # For now, return all messages (pagination disabled until DB integration)
        return self.messages
    
    def delete_conversation(self, conversation_id: str):
        """Delete a conversation by ID.
        
        Args:
            conversation_id: ID of conversation to delete
        """
        # Remove conversation from list
        self.conversations = [conv for conv in self.conversations if conv["id"] != conversation_id]
        
        # If current conversation was deleted, clear messages
        if self.current_conversation_id == conversation_id:
            self.current_conversation_id = ""
            self.messages = []
            
            # Load most recent conversation if any exist
            if self.conversations:
                self.load_conversation(self.conversations[0]["id"])
        
        # TODO: Delete from database when integrated
        # await self.database.delete_conversation(conversation_id)
    
    def archive_conversation(self, conversation_id: str):
        """Archive a conversation by ID.
        
        Args:
            conversation_id: ID of conversation to archive
        """
        # Find and mark conversation as archived
        for conv in self.conversations:
            if conv["id"] == conversation_id:
                conv["archived"] = True
                break
        
        # Filter out archived conversations from visible list
        self.conversations = [conv for conv in self.conversations if not conv.get("archived", False)]
        
        # If current conversation was archived, clear messages
        if self.current_conversation_id == conversation_id:
            self.current_conversation_id = ""
            self.messages = []
            
            # Load most recent conversation if any exist
            if self.conversations:
                self.load_conversation(self.conversations[0]["id"])
        
        # TODO: Update database when integrated
        # await self.database.update_conversation(conversation_id, archived=True)
