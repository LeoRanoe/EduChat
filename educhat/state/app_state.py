"""Main application state for EduChat."""

import reflex as rx
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import asyncio
from educhat.services.ai_service import get_ai_service
from educhat.state.auth_state import AuthState


class AppState(AuthState):
    """The main app state with authentication."""
    
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
    rename_conversation_id: str = ""  # ID of conversation being renamed
    rename_conversation_title: str = ""  # New title being entered
    
    # User context for AI (from onboarding)
    user_context: Optional[Dict] = None
    
    # Performance metrics
    last_response_time: float = 0.0
    
    # Initialization flag  
    _initialized: bool = False
    
    async def initialize_chat(self):
        """Initialize chat state when user first loads the chat page."""
        print(f"[INIT] Starting initialization. Already initialized: {self._initialized}")
        print(f"[INIT] Is guest: {self.is_guest}, Is authenticated: {self.is_authenticated}")
        print(f"[INIT] Current conversations: {len(self.conversations)}")
        print(f"[INIT] Current conversation ID: {self.current_conversation_id}")
        
        # Allow re-initialization if user just logged in or went guest
        # but only if they have no conversations
        if self._initialized and self.conversations:
            print("[INIT] Already initialized with conversations, skipping")
            return
        
        self._initialized = True
        
        # For logged-in users, load conversations from database
        if self.can_access_history():
            print("[INIT] Loading conversations from DB...")
            await self.load_conversations_from_db()
        
        # If no conversations exist (guest or new user), create initial conversation
        if not self.conversations:
            print("[INIT] No conversations found, creating initial conversation...")
            async for _ in self.create_new_conversation():
                pass
        # If conversations exist but no current one is selected, select the first
        elif not self.current_conversation_id:
            print(f"[INIT] Loading first conversation: {self.conversations[0]['id']}")
            async for _ in self.load_conversation(self.conversations[0]["id"]):
                pass
        
        print(f"[INIT] Initialization complete. Total conversations: {len(self.conversations)}, Current ID: {self.current_conversation_id}")
    
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
        
        # Update conversation title and metadata if exists
        if self.current_conversation_id:
            for conv in self.conversations:
                if conv["id"] == self.current_conversation_id:
                    # Auto-generate title from first message if still default
                    if conv.get("title") == "Nieuw gesprek" or not conv.get("title"):
                        conv["title"] = user_input_text[:50] + ("..." if len(user_input_text) > 50 else "")
                    # Update metadata
                    conv["last_updated"] = datetime.now().isoformat()
                    conv["message_count"] = len(self.messages)
                    break
        else:
            # Create new conversation
            async for _ in self.create_new_conversation():
                pass
            if self.conversations:
                # Auto-title from first message
                self.conversations[0]["title"] = user_input_text[:50] + ("..." if len(user_input_text) > 50 else "")
                self.conversations[0]["last_updated"] = datetime.now().isoformat()
                self.conversations[0]["message_count"] = len(self.messages)
        
        # Save conversation to database (for logged-in users)
        if self.can_save_conversations():
            await self.save_conversation_to_db()
    
    def set_user_input(self, value: str):
        """Update user input value."""
        self.user_input = value
    
    async def create_new_conversation(self):
        """Create a new conversation."""
        print(f"[CREATE] Creating new conversation. Current count: {len(self.conversations)}")
        from educhat.services.supabase_client import get_service
        
        # Check conversation limit
        if self.is_at_conversation_limit():
            # For guests, just clear current conversation
            if self.is_guest:
                self.messages = []
                self.current_conversation_id = ""
                return
            else:
                # Logged-in users at limit - shouldn't happen with limit of 100
                return
        
        # Save current conversation messages before creating new one (for guests)
        if self.is_guest and self.current_conversation_id and self.messages:
            # Update current conversation in memory
            for conv in self.conversations:
                if conv["id"] == self.current_conversation_id:
                    conv["messages"] = self.messages.copy()
                    # Update title with first message
                    if self.messages and self.messages[0]["is_user"]:
                        conv["title"] = self.messages[0]["content"][:50] + ("..." if len(self.messages[0]["content"]) > 50 else "")
                    break
        
        # Create conversation locally
        now = datetime.now()
        new_conv = {
            "id": str(uuid.uuid4()),
            "title": "Nieuw gesprek",
            "created_at": now.isoformat(),
            "last_updated": now.isoformat(),
            "message_count": 0,
            "messages": []  # Store messages for guests
        }
        
        # If logged-in user, create in database
        if self.can_save_conversations():
            try:
                db = get_service()
                conv_data = db.create_conversation(
                    user_id=self.user_id,
                    title="Nieuw gesprek"
                )
                new_conv["id"] = conv_data["id"]
            except Exception as e:
                print(f"Error creating conversation in DB: {e}")
        
        self.conversations.insert(0, new_conv)
        self.current_conversation_id = new_conv["id"]
        self.messages = []
        print(f"[CREATE] Created conversation {new_conv['id']}. Total conversations: {len(self.conversations)}")
        yield  # Force UI update
    
    async def load_conversation(self, conversation_id: str):
        """Load a conversation by ID."""
        print(f"[LOAD] Loading conversation: {conversation_id}")
        # Save current conversation messages before switching (for guests)
        if self.is_guest and self.current_conversation_id and self.messages:
            for conv in self.conversations:
                if conv["id"] == self.current_conversation_id:
                    conv["messages"] = self.messages.copy()
                    # Update title with first message if still default
                    if self.messages and self.messages[0]["is_user"]:
                        if conv.get("title") == "Nieuw gesprek" or not conv.get("title"):
                            conv["title"] = self.messages[0]["content"][:50] + ("..." if len(self.messages[0]["content"]) > 50 else "")
                    # Update metadata
                    conv["last_updated"] = datetime.now().isoformat()
                    conv["message_count"] = len(self.messages)
                    break
        
        self.current_conversation_id = conversation_id
        
        # Load messages from database if logged-in user
        if self.can_access_history():
            await self.load_conversation_messages(conversation_id)
        else:
            # Guest users: load from memory
            for conv in self.conversations:
                if conv["id"] == conversation_id:
                    self.messages = conv.get("messages", []).copy()
                    break
            else:
                self.messages = []
        
        print(f"[LOAD] Loaded conversation {conversation_id}. Messages: {len(self.messages)}")
        yield  # Force UI update
    
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
    
    def get_filtered_conversations(self) -> List[Dict]:
        """Get conversations filtered by search query."""
        if not self.search_query or not self.search_query.strip():
            return self.conversations
        
        query_lower = self.search_query.lower().strip()
        return [
            conv for conv in self.conversations
            if query_lower in conv.get("title", "").lower()
        ]
    
    async def rename_conversation(self, conversation_id: str, new_title: str):
        """Rename a conversation.
        
        Args:
            conversation_id: ID of conversation to rename
            new_title: New title for the conversation
        """
        print(f"[RENAME] Renaming conversation {conversation_id} to: {new_title}")
        
        if not new_title or not new_title.strip():
            return
        
        new_title = new_title.strip()
        
        # Update in local state
        for conv in self.conversations:
            if conv["id"] == conversation_id:
                conv["title"] = new_title
                conv["last_updated"] = datetime.now().isoformat()
                break
        
        # Update in database if logged-in user
        if self.can_save_conversations():
            try:
                from educhat.services.supabase_client import get_service
                db = get_service()
                db.update_conversation(conversation_id, title=new_title)
            except Exception as e:
                print(f"Error renaming conversation in DB: {e}")
        
        yield  # Force UI update
    
    def start_rename_conversation(self, conversation_id: str):
        """Start renaming a conversation (open rename UI).
        
        Args:
            conversation_id: ID of conversation to rename
        """
        # Find current title
        for conv in self.conversations:
            if conv["id"] == conversation_id:
                self.rename_conversation_id = conversation_id
                self.rename_conversation_title = conv.get("title", "")
                break
    
    def cancel_rename_conversation(self):
        """Cancel renaming a conversation."""
        self.rename_conversation_id = ""
        self.rename_conversation_title = ""
    
    def set_rename_title(self, title: str):
        """Update the rename title input."""
        self.rename_conversation_title = title
    
    async def confirm_rename_conversation(self):
        """Confirm and save the conversation rename."""
        if not self.rename_conversation_id or not self.rename_conversation_title.strip():
            self.cancel_rename_conversation()
            return
        
        async for _ in self.rename_conversation(self.rename_conversation_id, self.rename_conversation_title.strip()):
            pass
        self.cancel_rename_conversation()
    
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
    
    async def delete_conversation(self, conversation_id: str):
        """Delete a conversation by ID.
        
        Args:
            conversation_id: ID of conversation to delete
        """
        print(f"[DELETE] Deleting conversation: {conversation_id}")
        from educhat.services.supabase_client import get_service
        
        # Delete from database if logged-in user
        if self.can_save_conversations():
            try:
                db = get_service()
                db.delete_conversation(conversation_id)
            except Exception as e:
                print(f"Error deleting conversation from DB: {e}")
        
        # Remove conversation from list
        self.conversations = [conv for conv in self.conversations if conv["id"] != conversation_id]
        
        # If current conversation was deleted, clear messages and load another
        if self.current_conversation_id == conversation_id:
            self.current_conversation_id = ""
            self.messages = []
            
            # Load most recent conversation if any exist
            if self.conversations:
                async for _ in self.load_conversation(self.conversations[0]["id"]):
                    pass
        
        # Force UI update
        yield
    
    async def archive_conversation(self, conversation_id: str):
        """Archive a conversation by ID.
        
        Args:
            conversation_id: ID of conversation to archive
        """
        from educhat.services.supabase_client import get_service
        
        # Update in database if logged-in user
        if self.can_save_conversations():
            try:
                db = get_service()
                db.update_conversation(conversation_id, archived=True)
            except Exception as e:
                print(f"Error archiving conversation in DB: {e}")
        
        # Find and mark conversation as archived
        for conv in self.conversations:
            if conv["id"] == conversation_id:
                conv["archived"] = True
                break
        
        # Filter out archived conversations from visible list
        self.conversations = [conv for conv in self.conversations if not conv.get("archived", False)]
        
        # If current conversation was archived, clear messages and load another
        if self.current_conversation_id == conversation_id:
            self.current_conversation_id = ""
            self.messages = []
            
            # Load most recent conversation if any exist
            if self.conversations:
                async for _ in self.load_conversation(self.conversations[0]["id"]):
                    pass
        
        # Force UI update
        yield
    
    def can_save_conversations(self) -> bool:
        """Check if user can save conversations (only logged-in users)."""
        return self.is_authenticated and not self.is_guest
    
    def can_access_history(self) -> bool:
        """Check if user can access conversation history."""
        return self.is_authenticated and not self.is_guest
    
    def get_max_conversations(self) -> int:
        """Get maximum number of conversations allowed."""
        if self.is_guest:
            return 10  # Guest users can have up to 10 active conversations
        elif self.is_authenticated:
            return 100  # Logged-in users can have up to 100 conversations
        return 0
    
    def is_at_conversation_limit(self) -> bool:
        """Check if user has reached conversation limit."""
        return len(self.conversations) >= self.get_max_conversations()
    
    async def save_conversation_to_db(self):
        """Save current conversation to database (only for logged-in users)."""
        if not self.can_save_conversations():
            return
        
        from educhat.services.supabase_client import get_service
        
        try:
            db = get_service()
            
            # Check if conversation exists in DB
            if self.current_conversation_id:
                existing_conv = db.get_conversation_by_id(self.current_conversation_id)
                
                if not existing_conv:
                    # Create new conversation
                    title = self.messages[0]["content"][:50] if self.messages else "New Conversation"
                    conv_data = db.create_conversation(
                        user_id=self.user_id,
                        title=title + "..." if len(self.messages[0]["content"]) > 50 else title
                    )
                    self.current_conversation_id = conv_data["id"]
                else:
                    # Update conversation title
                    if self.messages:
                        title = self.messages[0]["content"][:50]
                        db.update_conversation(
                            conversation_id=self.current_conversation_id,
                            title=title + "..." if len(self.messages[0]["content"]) > 50 else title
                        )
                
                # Save new messages (check if already saved by checking message count)
                existing_messages = db.get_conversation_messages(self.current_conversation_id)
                messages_to_save = self.messages[len(existing_messages):]
                
                for msg in messages_to_save:
                    db.save_message(
                        conversation_id=self.current_conversation_id,
                        role="user" if msg["is_user"] else "assistant",
                        content=msg["content"],
                        feedback=msg.get("feedback"),
                        is_streaming=msg.get("is_streaming", False),
                        is_error=msg.get("is_error", False)
                    )
        
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    async def load_conversations_from_db(self):
        """Load user's conversation history from database."""
        if not self.can_access_history():
            return
        
        from educhat.services.supabase_client import get_service
        
        try:
            db = get_service()
            conversations_data = db.get_user_conversations(user_id=self.user_id)
            
            # Convert to our conversation format
            self.conversations = [
                {
                    "id": conv["id"],
                    "title": conv["title"],
                    "created_at": conv["created_at"],
                    "archived": conv.get("archived", False)
                }
                for conv in conversations_data
            ]
        
        except Exception as e:
            print(f"Error loading conversations: {e}")
    
    async def load_conversation_messages(self, conversation_id: str):
        """Load messages for a specific conversation from database."""
        if not self.can_access_history():
            return
        
        from educhat.services.supabase_client import get_service
        
        try:
            db = get_service()
            messages_data = db.get_conversation_messages(conversation_id)
            
            # Convert to our message format
            self.messages = [
                {
                    "content": msg["content"],
                    "is_user": msg["role"] == "user",
                    "timestamp": datetime.fromisoformat(msg["timestamp"]).strftime("%H:%M"),
                    "feedback": msg.get("feedback"),
                    "is_streaming": msg.get("is_streaming", False),
                    "is_error": msg.get("is_error", False)
                }
                for msg in messages_data
            ]
        
        except Exception as e:
            print(f"Error loading messages: {e}")

