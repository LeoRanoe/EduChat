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
    search_query: str = ""  # Search query for filtering conversations
    search_expanded: bool = False  # Whether search bar is expanded
    
    # User context for AI (from onboarding)
    user_context: Optional[Dict] = None
    
    # Performance metrics
    last_response_time: float = 0.0
    
    async def send_message(self):
        """Handle sending a message with AI integration and streaming response."""
        if not self.user_input.strip():
            return
        
        # Start performance tracking
        import time
        start_time = time.time()
        
        # Store input first
        user_input_text = self.user_input
        
        # Add user message
        user_message = {
            "content": user_input_text,
            "is_user": True,
            "timestamp": datetime.now().strftime("%H:%M"),
        }
        self.messages.append(user_message)
        
        # Clear input box immediately
        self.user_input = ""
        
        # Add temporary thinking message bubble
        thinking_message = {
            "content": "",
            "is_user": False,
            "timestamp": datetime.now().strftime("%H:%M"),
            "is_streaming": True,
        }
        self.messages.append(thinking_message)
        bot_message_idx = len(self.messages) - 1
        
        # Set loading state and update UI
        self.is_loading = True
        yield
        
        try:
            # Get AI service
            ai_service = get_ai_service()
            
            # Build conversation history (last 10 messages, excluding the new empty one)
            conversation_history = []
            for msg in self.messages[:-1][-10:]:
                role = "user" if msg["is_user"] else "assistant"
                conversation_history.append({
                    "role": role,
                    "content": msg["content"]
                })
            
            # Stream AI response with typing animation
            full_response = ""
            loop = asyncio.get_event_loop()
            
            # Run streaming in executor
            stream_generator = await loop.run_in_executor(
                None,
                lambda: ai_service.chat_stream(
                    message=user_input_text,
                    conversation_history=conversation_history,
                    context=self.user_context
                )
            )
            
            # Stream each chunk with smooth updates
            for chunk in stream_generator:
                full_response += chunk
                self.messages[bot_message_idx]["content"] = full_response
                yield
                # Small delay for natural typing effect (adjust as needed)
                await asyncio.sleep(0.03)  # 30ms between updates for smooth animation
            
            # Track response time
            self.last_response_time = time.time() - start_time
            
            # Mark streaming as complete
            self.messages[bot_message_idx]["is_streaming"] = False
            
        except TimeoutError:
            # Replace with timeout error
            self.messages[bot_message_idx] = {
                "content": "Het antwoord duurt te lang. Probeer je vraag opnieuw te stellen of maak deze korter.",
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
                "is_error": True,
            }
        except Exception as e:
            # Replace with error message
            self.messages[bot_message_idx] = {
                "content": "Sorry, er is iets misgegaan. Probeer het opnieuw of stel een andere vraag.",
                "is_user": False,
                "timestamp": datetime.now().strftime("%H:%M"),
                "is_error": True,
            }
        
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
        # Close search when collapsing sidebar
        if self.sidebar_collapsed:
            self.search_expanded = False
            self.search_query = ""
    
    def toggle_search(self):
        """Toggle search bar expansion."""
        self.search_expanded = not self.search_expanded
        if not self.search_expanded:
            self.search_query = ""
    
    def set_search_query(self, query: str):
        """Update search query."""
        self.search_query = query
    
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
        # Yield immediately to show the chat interface with the user message
        yield
        # Then send the message (this will handle the AI response)
        async for _ in self.send_message():
            yield
    
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
                # Store the user message content
                user_message_content = self.messages[user_msg_idx]["content"]
                
                # Replace the old bot response with streaming placeholder
                self.messages[message_index] = {
                    "content": "",
                    "is_user": False,
                    "timestamp": datetime.now().strftime("%H:%M"),
                    "is_streaming": True,
                }
                
                # Set loading state
                self.is_loading = True
                yield
                
                try:
                    # Get AI service
                    ai_service = get_ai_service()
                    
                    # Build conversation history (excluding the message being regenerated)
                    conversation_history = []
                    for i, msg in enumerate(self.messages[:message_index]):
                        role = "user" if msg["is_user"] else "assistant"
                        conversation_history.append({
                            "role": role,
                            "content": msg["content"]
                        })
                    
                    # Stream AI response
                    full_response = ""
                    loop = asyncio.get_event_loop()
                    
                    stream_generator = await loop.run_in_executor(
                        None,
                        lambda: ai_service.chat_stream(
                            message=user_message_content,
                            conversation_history=conversation_history[-10:],
                            context=self.user_context
                        )
                    )
                    
                    # Stream each chunk with smooth updates
                    for chunk in stream_generator:
                        full_response += chunk
                        self.messages[message_index]["content"] = full_response
                        yield
                        # Small delay for natural typing effect
                        await asyncio.sleep(0.03)  # 30ms between updates
                    
                    # Mark streaming as complete
                    self.messages[message_index]["is_streaming"] = False
                    
                except Exception as e:
                    self.messages[message_index] = {
                        "content": "Sorry, er is iets misgegaan bij het opnieuw genereren. Probeer het nog eens.",
                        "is_user": False,
                        "timestamp": datetime.now().strftime("%H:%M"),
                        "is_error": True,
                    }
                
                finally:
                    self.is_loading = False
    
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
