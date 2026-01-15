"""State management for onboarding quiz."""
import reflex as rx
from typing import Dict, List, Optional


# =============================================================================
# REAL EDUCATION DATA FOR SURINAME
# =============================================================================

# Education levels in Suriname
EDUCATION_LEVELS = [
    "Gewoon Lager Onderwijs (GLO)",
    "MULO (Meer Uitgebreid Lager Onderwijs)",
    "LBGO (Lager Beroepsgericht Onderwijs)",
    "HAVO (Hoger Algemeen Voortgezet Onderwijs)",
    "VWO (Voorbereidend Wetenschappelijk Onderwijs)",
    "MBO (Middelbaar Beroepsonderwijs)",
    "HBO (Hoger Beroepsonderwijs)",
    "Universiteit (WO)",
]

# Age groups
AGE_GROUPS = [
    "12-15 jaar",
    "16-18 jaar",
    "19-22 jaar",
    "23-30 jaar",
    "31+ jaar",
]

# Districts of Suriname
DISTRICTS = [
    "Paramaribo",
    "Wanica",
    "Nickerie",
    "Commewijne",
    "Saramacca",
    "Para",
    "Brokopondo",
    "Sipaliwini",
    "Coronie",
    "Marowijne",
]

# School subjects in Suriname
SCHOOL_SUBJECTS = [
    "Wiskunde",
    "Nederlands",
    "Engels",
    "Natuurkunde",
    "Scheikunde",
    "Biologie",
    "Aardrijkskunde",
    "Geschiedenis",
    "Economie",
    "Informatica",
    "Spaans",
    "Lichamelijke Opvoeding",
    "Beeldende Vorming",
    "Muziek",
]

# Study directions / Career paths
STUDY_DIRECTIONS = [
    "Techniek & ICT",
    "Gezondheid & Zorg",
    "Economie & Bedrijfskunde",
    "Onderwijs",
    "Rechten",
    "Natuur & Milieu",
    "Kunst & Cultuur",
    "Sociale Wetenschappen",
    "Landbouw & Agribusiness",
    "Toerisme & Horeca",
]

# Improvement goals for EduChat
IMPROVEMENT_GOALS = [
    "Betere cijfers halen",
    "Studiekeuze maken",
    "Informatie over scholen vinden",
    "Leren plannen & studietips",
    "Toelatingseisen begrijpen",
    "Inschrijvingsprocedures leren",
    "Carrièremogelijkheden ontdekken",
    "Beurzen & financiering vinden",
]

# Formality preferences
FORMALITY_OPTIONS = [
    "Informeel & vriendelijk",
    "Normaal",
    "Formeel & zakelijk",
]

# Future study plans
FUTURE_PLAN_OPTIONS = [
    "Ja, ik wil verder studeren",
    "Nee, ik ga werken",
    "Ik weet het nog niet",
    "Ik zoek nog informatie",
]


class OnboardingState(rx.State):
    """State for managing the onboarding quiz flow."""
    
    # Current step in the quiz (0-7)
    current_step: int = 0
    
    # User answers
    education_level: str = ""  # Current education level
    study_direction: List[str] = []  # Interested study directions
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
    user_id_linked: Optional[str] = None
    saving_to_db: bool = False
    loading_from_db: bool = False
    
    # Edit mode (for returning users)
    is_edit_mode: bool = False
    
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
    
    def set_education_level(self, value: str):
        """Set education level selection."""
        self.education_level = value
    
    def toggle_study_direction(self, value: str):
        """Toggle study direction selection."""
        if value in self.study_direction:
            self.study_direction.remove(value)
        else:
            self.study_direction.append(value)
    
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
    
    def reset_onboarding(self):
        """Reset onboarding state for new session or edit."""
        self.current_step = 0
        self.education_level = ""
        self.study_direction = []
        self.age = ""
        self.district = ""
        self.favorite_subjects = []
        self.future_plans = ""
        self.improvement_areas = []
        self.formality = "Normaal"
        self.expectations = ""
        self.quiz_completed = False
        self.is_edit_mode = False
    
    def start_edit_mode(self):
        """Start editing existing onboarding answers."""
        self.is_edit_mode = True
        self.current_step = 0
    
    async def complete_quiz(self):
        """Mark quiz as completed and save preferences to database."""
        self.quiz_completed = True
        self.saving_to_db = True
        yield
        
        # Get user info from parent state if available
        user_id = None
        
        try:
            # Try to get user_id from parent AuthState
            from educhat.state.auth_state import AuthState
            auth_state = await self.get_state(AuthState)
            if auth_state and hasattr(auth_state, 'user_id') and auth_state.user_id:
                user_id = auth_state.user_id
                self.user_id_linked = user_id
        except Exception as e:
            print(f"Could not get user_id: {e}")
        
        # Save to database
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            
            # Prepare answers data
            answers_data = {
                "education_level": self.education_level,
                "study_direction": ",".join(self.study_direction) if self.study_direction else "",
                "age": self.age,
                "district": self.district,
                "favorite_subjects": ",".join(self.favorite_subjects) if self.favorite_subjects else "",
                "future_plans": self.future_plans,
                "improvement_areas": ",".join(self.improvement_areas) if self.improvement_areas else "",
                "formality": self.formality,
                "expectations": self.expectations,
            }
            
            if self.is_edit_mode and self.onboarding_id:
                # Update existing onboarding record
                db.update_onboarding(
                    onboarding_id=self.onboarding_id,
                    data={"answers": answers_data, "completed": True}
                )
                print(f"Onboarding updated in DB: {self.onboarding_id}")
            else:
                # Create new onboarding record
                import uuid
                session_id = str(uuid.uuid4())
                
                onboarding_data = db.create_onboarding(
                    session_id=session_id,
                    user_id=user_id
                )
                self.onboarding_id = onboarding_data.get("id")
                
                # Update onboarding record with answers
                db.update_onboarding(
                    onboarding_id=self.onboarding_id,
                    data={"answers": answers_data, "completed": True}
                )
                print(f"Onboarding saved to DB: {self.onboarding_id}")
            
            self.is_edit_mode = False
            
        except Exception as e:
            print(f"Error saving onboarding to DB: {e}")
            # Continue anyway - quiz is marked as completed locally
        
        finally:
            self.saving_to_db = False
        
        # Redirect to chat after completion
        yield rx.redirect("/chat")
    
    async def load_user_preferences(self, user_id: str):
        """Load user's onboarding preferences from database.
        
        Args:
            user_id: User's UUID to look up preferences.
            
        Returns:
            True if preferences were loaded, False otherwise.
        """
        self.loading_from_db = True
        
        try:
            from educhat.services.supabase_client import get_service
            db = get_service()
            
            # Get user's most recent onboarding record
            response = db.client.table('onboarding').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
            
            if response.data:
                onboarding = response.data[0]
                answers = onboarding.get("answers", {})
                
                if answers:
                    # Restore answers from database
                    self.education_level = answers.get("education_level", "")
                    self.study_direction = answers.get("study_direction", "").split(",") if answers.get("study_direction") else []
                    self.age = answers.get("age", "")
                    self.district = answers.get("district", "")
                    self.favorite_subjects = answers.get("favorite_subjects", "").split(",") if answers.get("favorite_subjects") else []
                    self.future_plans = answers.get("future_plans", "")
                    self.improvement_areas = answers.get("improvement_areas", "").split(",") if answers.get("improvement_areas") else []
                    self.formality = answers.get("formality", "Normaal")
                    self.expectations = answers.get("expectations", "")
                    self.quiz_completed = onboarding.get("completed", False)
                    self.onboarding_id = onboarding.get("id")
                    self.user_id_linked = user_id
                    
                    print(f"Loaded onboarding preferences for user {user_id}")
                    self.loading_from_db = False
                    return True
            
            self.loading_from_db = False
            return False
            
        except Exception as e:
            print(f"Error loading onboarding preferences: {e}")
            self.loading_from_db = False
            return False
    
    def has_completed_onboarding(self) -> bool:
        """Check if user has completed onboarding."""
        return self.quiz_completed and self.onboarding_id is not None
    
    def get_user_context(self) -> Dict:
        """Get user context for AI personalization.
        
        Returns:
            Dictionary with user preferences for AI context.
        """
        if not self.quiz_completed:
            return {}
        
        # Build a rich context for AI personalization
        context = {
            "education_level": self.education_level,
            "study_directions": self.study_direction,
            "age_group": self.age,
            "district": self.district,
            "favorite_subjects": self.favorite_subjects,
            "future_plans": self.future_plans,
            "improvement_areas": self.improvement_areas,
            "formality_preference": self.formality,
            "expectations": self.expectations,
        }
        
        # Add derived context for better AI responses
        if self.formality == "Informeel & vriendelijk":
            context["tone"] = "casual, friendly, use informal language"
        elif self.formality == "Formeel & zakelijk":
            context["tone"] = "professional, formal, respectful"
        else:
            context["tone"] = "balanced, clear, helpful"
        
        # Add age-appropriate context
        if self.age in ["12-15 jaar", "16-18 jaar"]:
            context["audience"] = "young student, explain concepts simply"
        elif self.age in ["19-22 jaar"]:
            context["audience"] = "young adult, university level"
        else:
            context["audience"] = "adult learner, professional context"
        
        return context
    
    def get_context_summary(self) -> str:
        """Get a human-readable summary of user context for AI prompts.
        
        Returns:
            String summary of user preferences.
        """
        if not self.quiz_completed:
            return ""
        
        parts = []
        
        if self.education_level:
            parts.append(f"Opleiding: {self.education_level}")
        
        if self.age:
            parts.append(f"Leeftijd: {self.age}")
        
        if self.district:
            parts.append(f"District: {self.district}")
        
        if self.study_direction:
            parts.append(f"Interessegebieden: {', '.join(self.study_direction)}")
        
        if self.favorite_subjects:
            parts.append(f"Favoriete vakken: {', '.join(self.favorite_subjects)}")
        
        if self.improvement_areas:
            parts.append(f"Wil hulp bij: {', '.join(self.improvement_areas)}")
        
        if self.future_plans:
            parts.append(f"Toekomstplannen: {self.future_plans}")
        
        return "; ".join(parts) if parts else ""
    
    def get_progress_percentage(self) -> int:
        """Calculate the current progress percentage."""
        return int((self.current_step / self.total_steps) * 100)

