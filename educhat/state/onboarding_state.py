"""State management for onboarding quiz."""
import reflex as rx
from typing import Dict, List, Optional


class OnboardingState(rx.State):
    """State for managing the onboarding quiz flow."""
    
    # Current step in the quiz (0-7)
    current_step: int = 0
    
    # User answers
    education: List[str] = []
    age: str = ""
    district: str = ""
    favorite_subjects: List[str] = []
    future_plans: str = ""
    improvement_areas: List[str] = []
    formality: str = "Normaal"
    expectations: str = ""
    
    # Quiz completed flag
    quiz_completed: bool = False
    
    # Total number of steps
    total_steps: int = 8
    
    # Database tracking
    onboarding_id: Optional[str] = None
    saving_to_db: bool = False
    
    def next_step(self):
        """Move to the next step in the quiz."""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
    
    def previous_step(self):
        """Move to the previous step in the quiz."""
        if self.current_step > 0:
            self.current_step -= 1
    
    def skip_step(self):
        """Skip the current step."""
        self.next_step()
    
    def toggle_education(self, value: str):
        """Toggle education selection."""
        if value in self.education:
            self.education.remove(value)
        else:
            self.education.append(value)
    
    def set_age(self, value: str):
        """Set age selection."""
        self.age = value
    
    def set_district(self, value: str):
        """Set district selection."""
        self.district = value
    
    def toggle_subject(self, value: str):
        """Toggle favorite subject selection."""
        if value in self.favorite_subjects:
            self.favorite_subjects.remove(value)
        else:
            self.favorite_subjects.append(value)
    
    def set_future_plans(self, value: str):
        """Set future plans."""
        self.future_plans = value
    
    def toggle_improvement_area(self, value: str):
        """Toggle improvement area selection."""
        if value in self.improvement_areas:
            self.improvement_areas.remove(value)
        else:
            self.improvement_areas.append(value)
    
    def set_formality(self, value: str):
        """Set formality preference."""
        self.formality = value
    
    def set_expectations(self, value: str):
        """Set user expectations."""
        self.expectations = value
    
    async def complete_quiz(self):
        """Mark quiz as completed and save preferences to database."""
        self.quiz_completed = True
        self.saving_to_db = True
        yield
        
        # Get user info from parent state if available
        user_id = None
        session_id = None
        
        try:
            # Try to get user_id from parent AuthState
            if hasattr(self, 'user_id'):
                user_id = self.user_id
        except:
            pass
        
        # Save to database
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            
            # Create onboarding record
            import uuid
            session_id = str(uuid.uuid4())  # Generate session ID for anonymous users
            
            onboarding_data = db.create_onboarding(
                session_id=session_id,
                user_id=user_id
            )
            self.onboarding_id = onboarding_data.get("id")
            
            # Save all answers
            answers_data = {
                "education": ",".join(self.education) if self.education else "",
                "age": self.age,
                "district": self.district,
                "favorite_subjects": ",".join(self.favorite_subjects) if self.favorite_subjects else "",
                "future_plans": self.future_plans,
                "improvement_areas": ",".join(self.improvement_areas) if self.improvement_areas else "",
                "formality": self.formality,
                "expectations": self.expectations,
            }
            
            # Update onboarding record with answers (stored as JSON in metadata)
            db.update_onboarding(
                onboarding_id=self.onboarding_id,
                data={"answers": answers_data, "completed": True}
            )
            
            print(f"Onboarding saved to DB: {self.onboarding_id}")
            
        except Exception as e:
            print(f"Error saving onboarding to DB: {e}")
            # Continue anyway - quiz is marked as completed locally
        
        finally:
            self.saving_to_db = False
    
    async def load_user_preferences(self, user_id: str):
        """Load user's onboarding preferences from database.
        
        Args:
            user_id: User's UUID to look up preferences.
        """
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            
            # Get user's most recent onboarding record
            # Query by user_id to get their preferences
            response = db.client.table('onboarding').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
            
            if response.data:
                onboarding = response.data[0]
                answers = onboarding.get("answers", {})
                
                if answers:
                    # Restore answers from database
                    self.education = answers.get("education", "").split(",") if answers.get("education") else []
                    self.age = answers.get("age", "")
                    self.district = answers.get("district", "")
                    self.favorite_subjects = answers.get("favorite_subjects", "").split(",") if answers.get("favorite_subjects") else []
                    self.future_plans = answers.get("future_plans", "")
                    self.improvement_areas = answers.get("improvement_areas", "").split(",") if answers.get("improvement_areas") else []
                    self.formality = answers.get("formality", "Normaal")
                    self.expectations = answers.get("expectations", "")
                    self.quiz_completed = onboarding.get("completed", False)
                    self.onboarding_id = onboarding.get("id")
                    
                    print(f"Loaded onboarding preferences for user {user_id}")
                    
        except Exception as e:
            print(f"Error loading onboarding preferences: {e}")
    
    def get_user_context(self) -> Dict:
        """Get user context for AI personalization.
        
        Returns:
            Dictionary with user preferences for AI context.
        """
        if not self.quiz_completed:
            return {}
        
        return {
            "education_level": self.education,
            "age_group": self.age,
            "district": self.district,
            "favorite_subjects": self.favorite_subjects,
            "future_plans": self.future_plans,
            "improvement_areas": self.improvement_areas,
            "formality_preference": self.formality,
            "expectations": self.expectations,
        }
    
    def get_progress_percentage(self) -> int:
        """Calculate the current progress percentage."""
        return int((self.current_step / self.total_steps) * 100)

