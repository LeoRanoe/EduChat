"""Database service for EduChat - Supabase/Postgres integration via Prisma.

This module provides a comprehensive interface to Supabase Postgres for all database operations.
It implements connection pooling (via Prisma), CRUD operations, and query methods for all tables.

Tables:
- institutions: Educational institutions in Suriname
- studies: Programs and courses offered
- events: Important dates, deadlines, open days
- users: User accounts
- sessions: Chat sessions
- messages: Individual chat messages
- onboarding: User onboarding progress
- onboarding_questions: Quiz questions
- onboarding_answers: User's quiz responses
- reminders: Deadline and event reminders

Note: This service wraps the Prisma Python client for type-safe database access.
For direct access, you can use: from prisma import Prisma
"""

import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Prisma will be used for database operations
# Import will be added after prisma generate is run
try:
    from prisma import Prisma
    PRISMA_AVAILABLE = True
except ImportError:
    PRISMA_AVAILABLE = False
    print("Warning: Prisma client not available. Run 'prisma generate' first.")


class DatabaseService:
    """Supabase/Postgres database service with Prisma ORM for connection pooling and CRUD operations."""
    
    def __init__(
        self,
        connection_string: Optional[str] = None
    ):
        """Initialize database connection via Prisma.
        
        Args:
            connection_string: Postgres connection URI (defaults to env var DATABASE_URL)
        """
        self.connection_string = connection_string or os.getenv(
            "DATABASE_URL",
            os.getenv("SUPABASE_URL", "")
        )
        
        if not PRISMA_AVAILABLE:
            raise ImportError(
                "Prisma client not available. Install with: pip install prisma && prisma generate"
            )
        
        # Initialize Prisma client (connection pooling handled automatically)
        self.client = Prisma()
        self._connected = False
    
    async def connect(self):
        """Connect to the database (async operation)."""
        if not self._connected:
            await self.client.connect()
            self._connected = True
    
    async def disconnect(self):
        """Disconnect from the database."""
        if self._connected:
            await self.client.disconnect()
            self._connected = False
    
    async def test_connection(self) -> bool:
        """Test database connection.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            await self.connect()
            # Simple query to test connection
            await self.client.query_raw("SELECT 1")
            return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
    
    def close(self):
        """Close database connection (sync wrapper for backward compatibility)."""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is running, schedule disconnect
                asyncio.create_task(self.disconnect())
            else:
                # Run in new event loop
                asyncio.run(self.disconnect())
        except Exception as e:
            print(f"Error closing database connection: {e}")
    
    # ==================== INSTITUTIONS ====================
    
    def create_institution(self, institution_data: Dict[str, Any]) -> str:
        """Create a new educational institution.
        
        Args:
            institution_data: Institution details
            
        Returns:
            Inserted institution ID as string
        """
        # Work on a copy to avoid mutating the caller's dict (tests pass the
        # same dict instance multiple times). This prevents duplicate _id
        # issues where PyMongo may add `_id` to the original document.
        doc = dict(institution_data)
        doc["last_updated"] = datetime.now(timezone.utc)
        result = self.institutions.insert_one(doc)
        return str(result.inserted_id)
    
    def get_institution(self, institution_id: str) -> Optional[Dict]:
        """Get institution by ID.
        
        Args:
            institution_id: Institution ID
            
        Returns:
            Institution document or None
        """
        return self.institutions.find_one({"_id": ObjectId(institution_id)})
    
    def get_all_institutions(
        self,
        location: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Get all institutions with optional filtering.
        
        Args:
            location: Filter by location
            limit: Maximum number of results
            
        Returns:
            List of institution documents
        """
        query = {}
        if location:
            query["location"] = location
        
        return list(self.institutions.find(query).limit(limit))
    
    def search_institutions(
        self,
        search_text: str,
        limit: int = 10
    ) -> List[Dict]:
        """Search institutions by text.
        
        Args:
            search_text: Search query
            limit: Maximum results
            
        Returns:
            List of matching institutions
        """
        return list(
            self.institutions.find(
                {"$text": {"$search": search_text}}
            ).limit(limit)
        )
    
    def update_institution(
        self,
        institution_id: str,
        update_data: Dict[str, Any]
    ) -> bool:
        """Update institution details.
        
        Args:
            institution_id: Institution ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        update_data["last_updated"] = datetime.now(timezone.utc)
        result = self.institutions.update_one(
            {"_id": ObjectId(institution_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_institution(self, institution_id: str) -> bool:
        """Delete institution.
        
        Args:
            institution_id: Institution ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.institutions.delete_one({"_id": ObjectId(institution_id)})
        return result.deleted_count > 0
    
    # ==================== STUDIES ====================
    
    def create_study(self, study_data: Dict[str, Any]) -> str:
        """Create a new study program.
        
        Args:
            study_data: Study program details
            
        Returns:
            Inserted study ID as string
        """
        # Copy input to avoid mutating caller-provided dicts (prevents
        # duplicate _id when the same dict is reused in tests).
        doc = dict(study_data)
        doc["last_updated"] = datetime.now(timezone.utc)
        result = self.studies.insert_one(doc)
        return str(result.inserted_id)
    
    def get_study(self, study_id: str) -> Optional[Dict]:
        """Get study by ID.
        
        Args:
            study_id: Study ID
            
        Returns:
            Study document or None
        """
        return self.studies.find_one({"_id": ObjectId(study_id)})
    
    def get_studies_by_institution(
        self,
        institution_id: str,
        study_type: Optional[str] = None
    ) -> List[Dict]:
        """Get all studies for an institution.
        
        Args:
            institution_id: Institution ID
            study_type: Filter by type (Bachelor, MBO, Master, etc.)
            
        Returns:
            List of study programs
        """
        query = {"institution_id": institution_id}
        if study_type:
            query["type"] = study_type
        
        return list(self.studies.find(query))
    
    def search_studies(
        self,
        search_text: str,
        study_type: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """Search studies by text.
        
        Args:
            search_text: Search query
            study_type: Filter by type
            limit: Maximum results
            
        Returns:
            List of matching studies
        """
        query = {"$text": {"$search": search_text}}
        if study_type:
            query["type"] = study_type
        
        return list(self.studies.find(query).limit(limit))
    
    def update_study(self, study_id: str, update_data: Dict[str, Any]) -> bool:
        """Update study program.
        
        Args:
            study_id: Study ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        update_data["last_updated"] = datetime.now(timezone.utc)
        result = self.studies.update_one(
            {"_id": ObjectId(study_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_study(self, study_id: str) -> bool:
        """Delete study program.
        
        Args:
            study_id: Study ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.studies.delete_one({"_id": ObjectId(study_id)})
        return result.deleted_count > 0
    
    # ==================== EVENTS ====================
    
    def create_event(self, event_data: Dict[str, Any]) -> str:
        """Create a new event.
        
        Args:
            event_data: Event details
            
        Returns:
            Inserted event ID as string
        """
        # Copy input to avoid mutating caller-provided dicts
        doc = dict(event_data)
        doc["last_updated"] = datetime.now(timezone.utc)
        result = self.events.insert_one(doc)
        return str(result.inserted_id)
    
    def get_event(self, event_id: str) -> Optional[Dict]:
        """Get event by ID.
        
        Args:
            event_id: Event ID
            
        Returns:
            Event document or None
        """
        return self.events.find_one({"_id": ObjectId(event_id)})
    
    def get_upcoming_events(
        self,
        institution_id: Optional[str] = None,
        event_type: Optional[str] = None,
        days_ahead: int = 30
    ) -> List[Dict]:
        """Get upcoming events.
        
        Args:
            institution_id: Filter by institution
            event_type: Filter by type (open_day, deadline, etc.)
            days_ahead: Number of days to look ahead
            
        Returns:
            List of upcoming events
        """
        query = {
            "date": {
                "$gte": datetime.now(timezone.utc),
                "$lte": datetime.now(timezone.utc) + timedelta(days=days_ahead)
            }
        }
        
        if institution_id:
            query["institution_id"] = institution_id
        if event_type:
            query["type"] = event_type
        
        return list(
            self.events.find(query).sort("date", ASCENDING)
        )
    
    def update_event(self, event_id: str, update_data: Dict[str, Any]) -> bool:
        """Update event.
        
        Args:
            event_id: Event ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        update_data["last_updated"] = datetime.now(timezone.utc)
        result = self.events.update_one(
            {"_id": ObjectId(event_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_event(self, event_id: str) -> bool:
        """Delete event.
        
        Args:
            event_id: Event ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.events.delete_one({"_id": ObjectId(event_id)})
        return result.deleted_count > 0
    
    # ==================== USERS ====================
    
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user account.
        
        Args:
            user_data: User details (email, password, etc.)
            
        Returns:
            Inserted user ID as string
        """
        # Copy input to avoid mutating caller-provided dicts
        doc = dict(user_data)
        doc["created_at"] = datetime.now(timezone.utc)
        result = self.users.insert_one(doc)
        return str(result.inserted_id)
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User document or None
        """
        return self.users.find_one({"_id": ObjectId(user_id)})
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User document or None
        """
        return self.users.find_one({"email": email})
    
    def update_user(self, user_id: str, update_data: Dict[str, Any]) -> bool:
        """Update user details.
        
        Args:
            user_id: User ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        result = self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_user(self, user_id: str) -> bool:
        """Delete user account.
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.users.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    
    # ==================== SESSIONS ====================
    
    def create_session(
        self,
        user_id: Optional[str] = None,
        anonymous_id: Optional[str] = None
    ) -> str:
        """Create a new chat session.
        
        Args:
            user_id: User ID (for authenticated users)
            anonymous_id: Anonymous session ID (for guest users)
            
        Returns:
            Inserted session ID as string
        """
        session_data = {
            "user_id": user_id,
            "anonymous_id": anonymous_id,
            "created_at": datetime.utcnow(),
            "last_active": datetime.utcnow(),
            "summary": ""
        }
        result = self.sessions.insert_one(session_data)
        return str(result.inserted_id)
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session document or None
        """
        return self.sessions.find_one({"_id": ObjectId(session_id)})
    
    def get_user_sessions(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[Dict]:
        """Get all sessions for a user.
        
        Args:
            user_id: User ID
            limit: Maximum number of sessions
            
        Returns:
            List of session documents
        """
        return list(
            self.sessions.find({"user_id": user_id})
            .sort("last_active", DESCENDING)
            .limit(limit)
        )
    
    def update_session_activity(self, session_id: str, summary: Optional[str] = None) -> bool:
        """Update session last_active timestamp.
        
        Args:
            session_id: Session ID
            summary: Optional summary of conversation
            
        Returns:
            True if updated, False otherwise
        """
        update_data = {"last_active": datetime.utcnow()}
        if summary:
            update_data["summary"] = summary
        
        result = self.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete_session(self, session_id: str) -> bool:
        """Delete session and all its messages.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if deleted, False otherwise
        """
        # Delete all messages in session
        self.messages.delete_many({"session_id": session_id})
        
        # Delete session
        result = self.sessions.delete_one({"_id": ObjectId(session_id)})
        return result.deleted_count > 0
    
    # ==================== MESSAGES ====================
    
    def create_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """Create a new message in a session.
        
        Args:
            session_id: Session ID
            role: Message role ('user' or 'assistant')
            content: Message content
            metadata: Optional metadata (response_time, etc.)
            
        Returns:
            Inserted message ID as string
        """
        message_data = {
            "session_id": session_id,
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "feedback": None,
            "metadata": metadata or {}
        }
        result = self.messages.insert_one(message_data)
        
        # Update session activity
        self.update_session_activity(session_id)
        
        return str(result.inserted_id)
    
    def get_message(self, message_id: str) -> Optional[Dict]:
        """Get message by ID.
        
        Args:
            message_id: Message ID
            
        Returns:
            Message document or None
        """
        return self.messages.find_one({"_id": ObjectId(message_id)})
    
    def get_session_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """Get all messages in a session.
        
        Args:
            session_id: Session ID
            limit: Maximum number of messages (None for all)
            
        Returns:
            List of message documents
        """
        query = self.messages.find({"session_id": session_id}).sort("timestamp", ASCENDING)
        
        if limit:
            query = query.limit(limit)
        
        return list(query)
    
    def add_message_feedback(
        self,
        message_id: str,
        rating: str,
        comment: Optional[str] = None
    ) -> bool:
        """Add feedback to a message.
        
        Args:
            message_id: Message ID
            rating: Rating ('thumbs_up' or 'thumbs_down')
            comment: Optional feedback comment
            
        Returns:
            True if updated, False otherwise
        """
        feedback = {
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.utcnow()
        }
        
        result = self.messages.update_one(
            {"_id": ObjectId(message_id)},
            {"$set": {"feedback": feedback}}
        )
        return result.modified_count > 0
    
    def delete_message(self, message_id: str) -> bool:
        """Delete a message.
        
        Args:
            message_id: Message ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.messages.delete_one({"_id": ObjectId(message_id)})
        return result.deleted_count > 0
    
    # ==================== ONBOARDING ====================
    
    def create_onboarding(
        self,
        session_id: str,
        user_id: Optional[str] = None
    ) -> str:
        """Create onboarding record for a session.
        
        Args:
            session_id: Session ID
            user_id: Optional user ID
            
        Returns:
            Inserted onboarding ID as string
        """
        onboarding_data = {
            "session_id": session_id,
            "user_id": user_id,
            "completed": False,
            "completed_at": None,
            "current_step": 0,
            "interests": [],
            "skills": [],
            "goals": [],
            "personality": None,
            "quiz_results": {},
            "suggested_paths": [],
            "feedback": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        result = self.onboarding.insert_one(onboarding_data)
        return str(result.inserted_id)
    
    def get_onboarding(self, onboarding_id: str) -> Optional[Dict]:
        """Get onboarding by ID.
        
        Args:
            onboarding_id: Onboarding ID
            
        Returns:
            Onboarding document or None
        """
        return self.onboarding.find_one({"_id": ObjectId(onboarding_id)})
    
    def get_onboarding_by_session(self, session_id: str) -> Optional[Dict]:
        """Get onboarding for a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Onboarding document or None
        """
        return self.onboarding.find_one({"session_id": session_id})
    
    def update_onboarding_progress(
        self,
        onboarding_id: str,
        current_step: int,
        quiz_results: Optional[Dict] = None
    ) -> bool:
        """Update onboarding progress.
        
        Args:
            onboarding_id: Onboarding ID
            current_step: Current step number
            quiz_results: Optional quiz answers
            
        Returns:
            True if updated, False otherwise
        """
        update_data = {
            "current_step": current_step,
            "updated_at": datetime.utcnow()
        }
        
        if quiz_results:
            update_data["quiz_results"] = quiz_results
        
        result = self.onboarding.update_one(
            {"_id": ObjectId(onboarding_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def complete_onboarding(
        self,
        onboarding_id: str,
        interests: List[str],
        skills: List[str],
        goals: List[str],
        personality: str,
        suggested_paths: List[str]
    ) -> bool:
        """Mark onboarding as completed with results.
        
        Args:
            onboarding_id: Onboarding ID
            interests: User interests
            skills: User skills
            goals: User goals
            personality: User personality type
            suggested_paths: Recommended study paths
            
        Returns:
            True if updated, False otherwise
        """
        update_data = {
            "completed": True,
            "completed_at": datetime.utcnow(),
            "interests": interests,
            "skills": skills,
            "goals": goals,
            "personality": personality,
            "suggested_paths": suggested_paths,
            "updated_at": datetime.utcnow()
        }
        
        result = self.onboarding.update_one(
            {"_id": ObjectId(onboarding_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    # ==================== ONBOARDING QUESTIONS ====================
    
    def create_onboarding_question(self, question_data: Dict[str, Any]) -> str:
        """Create onboarding question.
        
        Args:
            question_data: Question details
            
        Returns:
            Inserted question ID as string
        """
        result = self.onboarding_questions.insert_one(question_data)
        return str(result.inserted_id)
    
    def get_onboarding_questions(
        self,
        category: Optional[str] = None,
        active_only: bool = True
    ) -> List[Dict]:
        """Get all onboarding questions.
        
        Args:
            category: Filter by category
            active_only: Only return active questions
            
        Returns:
            List of question documents
        """
        query = {}
        if category:
            query["category"] = category
        if active_only:
            query["active"] = True
        
        return list(
            self.onboarding_questions.find(query).sort("order_num", ASCENDING)
        )
    
    def update_onboarding_question(
        self,
        question_id: str,
        update_data: Dict[str, Any]
    ) -> bool:
        """Update onboarding question.
        
        Args:
            question_id: Question ID
            update_data: Fields to update
            
        Returns:
            True if updated, False otherwise
        """
        result = self.onboarding_questions.update_one(
            {"_id": ObjectId(question_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    # ==================== ONBOARDING ANSWERS ====================
    
    def save_onboarding_answer(
        self,
        onboarding_id: str,
        question_id: str,
        selected_option: str
    ) -> str:
        """Save user's answer to onboarding question.
        
        Args:
            onboarding_id: Onboarding ID
            question_id: Question ID
            selected_option: Selected answer
            
        Returns:
            Inserted answer ID as string
        """
        answer_data = {
            "onboarding_id": onboarding_id,
            "question_id": question_id,
            "selected_option": selected_option,
            "created_at": datetime.utcnow()
        }
        result = self.onboarding_answers.insert_one(answer_data)
        return str(result.inserted_id)
    
    def get_onboarding_answers(self, onboarding_id: str) -> List[Dict]:
        """Get all answers for an onboarding session.
        
        Args:
            onboarding_id: Onboarding ID
            
        Returns:
            List of answer documents
        """
        return list(
            self.onboarding_answers.find({"onboarding_id": onboarding_id})
        )
    
    # ==================== REMINDERS ====================
    
    def create_reminder(
        self,
        user_id: str,
        title: str,
        date: datetime,
        event_id: Optional[str] = None
    ) -> str:
        """Create a reminder for a user.
        
        Args:
            user_id: User ID
            title: Reminder title
            date: Reminder date
            event_id: Optional associated event ID
            
        Returns:
            Inserted reminder ID as string
        """
        reminder_data = {
            "user_id": user_id,
            "event_id": event_id,
            "title": title,
            "date": date,
            "sent": False,
            "created_at": datetime.utcnow()
        }
        result = self.reminders.insert_one(reminder_data)
        return str(result.inserted_id)
    
    def get_reminder(self, reminder_id: str) -> Optional[Dict]:
        """Get reminder by ID.
        
        Args:
            reminder_id: Reminder ID
            
        Returns:
            Reminder document or None
        """
        return self.reminders.find_one({"_id": ObjectId(reminder_id)})
    
    def get_user_reminders(
        self,
        user_id: str,
        include_sent: bool = False
    ) -> List[Dict]:
        """Get all reminders for a user.
        
        Args:
            user_id: User ID
            include_sent: Include already sent reminders
            
        Returns:
            List of reminder documents
        """
        query = {"user_id": user_id}
        if not include_sent:
            query["sent"] = False
        
        return list(
            self.reminders.find(query).sort("date", ASCENDING)
        )
    
    def get_pending_reminders(self, hours_ahead: int = 24) -> List[Dict]:
        """Get reminders that need to be sent.
        
        Args:
            hours_ahead: Look ahead this many hours
            
        Returns:
            List of pending reminders
        """
        return list(
            self.reminders.find({
                "sent": False,
                "date": {
                    "$lte": datetime.utcnow() + timedelta(hours=hours_ahead)
                }
            }).sort("date", ASCENDING)
        )
    
    def mark_reminder_sent(self, reminder_id: str) -> bool:
        """Mark reminder as sent.
        
        Args:
            reminder_id: Reminder ID
            
        Returns:
            True if updated, False otherwise
        """
        result = self.reminders.update_one(
            {"_id": ObjectId(reminder_id)},
            {"$set": {"sent": True}}
        )
        return result.modified_count > 0
    
    def delete_reminder(self, reminder_id: str) -> bool:
        """Delete reminder.
        
        Args:
            reminder_id: Reminder ID
            
        Returns:
            True if deleted, False otherwise
        """
        result = self.reminders.delete_one({"_id": ObjectId(reminder_id)})
        return result.deleted_count > 0
    
    # ==================== ANALYTICS ====================
    
    def get_message_stats(
        self,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get message statistics.
        
        Args:
            days: Number of days to look back
            
        Returns:
            Dictionary with statistics
        """
        start_date = datetime.utcnow() - timedelta(days=days)
        
        total_messages = self.messages.count_documents({
            "timestamp": {"$gte": start_date}
        })
        
        user_messages = self.messages.count_documents({
            "timestamp": {"$gte": start_date},
            "role": "user"
        })
        
        assistant_messages = self.messages.count_documents({
            "timestamp": {"$gte": start_date},
            "role": "assistant"
        })
        
        feedback_stats = list(self.messages.aggregate([
            {"$match": {"timestamp": {"$gte": start_date}, "feedback": {"$ne": None}}},
            {"$group": {
                "_id": "$feedback.rating",
                "count": {"$sum": 1}
            }}
        ]))
        
        return {
            "total_messages": total_messages,
            "user_messages": user_messages,
            "assistant_messages": assistant_messages,
            "feedback": feedback_stats,
            "period_days": days
        }
    
    def get_popular_institutions(self, limit: int = 10) -> List[Dict]:
        """Get most asked about institutions (placeholder for analytics).
        
        Args:
            limit: Number of results
            
        Returns:
            List of institutions with query counts
        """
        # This would require implementing query tracking
        # For now, return most recently updated
        return list(
            self.institutions.find()
            .sort("last_updated", DESCENDING)
            .limit(limit)
        )


# ==================== HELPER FUNCTIONS ====================

def convert_objectid_to_str(document: Optional[Dict]) -> Optional[Dict]:
    """Convert ObjectId fields to strings for JSON serialization.
    
    Args:
        document: MongoDB document
        
    Returns:
        Document with string IDs
    """
    if document is None:
        return None
    
    if "_id" in document:
        document["_id"] = str(document["_id"])
    
    return document


def convert_objectids_in_list(documents: List[Dict]) -> List[Dict]:
    """Convert ObjectId fields in list of documents.
    
    Args:
        documents: List of MongoDB documents
        
    Returns:
        List with string IDs
    """
    return [convert_objectid_to_str(doc) for doc in documents]
