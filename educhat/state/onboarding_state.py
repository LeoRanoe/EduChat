"""State management for onboarding quiz."""
import reflex as rx
from typing import Dict, List


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
    
    def complete_quiz(self):
        """Mark quiz as completed and save preferences."""
        self.quiz_completed = True
        # TODO: Save to database
        # In a real app, you would save these preferences to the database
        # and use them to personalize the chat experience
    
    def get_progress_percentage(self) -> int:
        """Calculate the current progress percentage."""
        return int((self.current_step / self.total_steps) * 100)
