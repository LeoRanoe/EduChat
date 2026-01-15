"""State management for EduChat."""

from educhat.state.app_state import AppState
from educhat.state.onboarding_state import (
    OnboardingState,
    EDUCATION_LEVELS,
    AGE_GROUPS,
    DISTRICTS,
    SCHOOL_SUBJECTS,
    STUDY_DIRECTIONS,
    IMPROVEMENT_GOALS,
    FORMALITY_OPTIONS,
    FUTURE_PLAN_OPTIONS,
)

__all__ = [
    "AppState",
    "OnboardingState",
    "EDUCATION_LEVELS",
    "AGE_GROUPS",
    "DISTRICTS",
    "SCHOOL_SUBJECTS",
    "STUDY_DIRECTIONS",
    "IMPROVEMENT_GOALS",
    "FORMALITY_OPTIONS",
    "FUTURE_PLAN_OPTIONS",
]

