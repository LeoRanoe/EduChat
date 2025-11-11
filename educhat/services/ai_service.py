"""
AI Service for EduChat - OpenAI Integration

This module provides AI-powered responses with a focus on Surinamese education.
Includes error handling, retry logic, and response validation.
"""

import os
import time
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI, APIError, RateLimitError, APIConnectionError
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not available. Install with: pip install openai")


class AIService:
    """AI service with OpenAI integration for educational queries."""
    
    # Suriname-focused system prompt
    SYSTEM_PROMPT = """Je bent EduChat, een vriendelijke AI-assistent gespecialiseerd in het Surinaams onderwijssysteem.

Je expertisegebieden zijn:
- Surinaamse onderwijsinstellingen (universiteiten, MINOV, middelbare scholen)
- Toelatingsprocedures en vereisten
- Studieprogramma's en curricula
- Deadlines en belangrijke data
- Studiekosten en financieringsmogelijkheden
- Algemeen studieadvies voor Surinaamse studenten

Belangrijk:
1. Geef alleen informatie over Surinaams onderwijs
2. Als een vraag buiten onderwijs valt, verwijs beleefd terug naar onderwijs
3. Wees specifiek, accuraat en behulpzaam
4. Gebruik een vriendelijke, toegankelijke toon
5. Bij twijfel, zeg dat je het niet zeker weet en verwijs naar officiële bronnen
6. Geef stapsgewijze instructies waar mogelijk
7. Pas je formaliteitsniveau aan op basis van de gebruiker

Als je een vraag krijgt die NIET over Surinaams onderwijs gaat:
"Ik ben gespecialiseerd in Surinaams onderwijs en kan je daar graag mee helpen! Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen in Suriname?"
"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """Initialize AI service.
        
        Args:
            api_key: OpenAI API key (defaults to env var)
            model: OpenAI model to use
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        
        # Retry configuration
        self.max_retries = 3
        self.base_delay = 1  # seconds
        self.max_delay = 10  # seconds
    
    def _is_education_related(self, message: str) -> bool:
        """Check if message is related to education.
        
        Args:
            message: User message
            
        Returns:
            True if education-related
        """
        education_keywords = [
            "studie", "opleiding", "universiteit", "school", "minov",
            "inschrijven", "inschrijving", "toelating", "examen", "diploma",
            "vakken", "lessen", "docent", "leraar", "student", "cursus",
            "bachelor", "master", "vmbo", "havo", "vwo", "mbo",
            "deadline", "kosten", "beurs", "financiering"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in education_keywords)
    
    def _get_fallback_response(self, message: str) -> str:
        """Get fallback response for off-topic questions.
        
        Args:
            message: User message
            
        Returns:
            Fallback response
        """
        if not self._is_education_related(message):
            return (
                "Ik ben gespecialiseerd in Surinaams onderwijs en kan je daar graag mee helpen! "
                "Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen in Suriname? "
                "Bijvoorbeeld:\n"
                "- Hoe schrijf ik me in voor een opleiding?\n"
                "- Welke documenten heb ik nodig?\n"
                "- Wat zijn de toelatingseisen?\n"
                "- Vertel me over MINOV opleidingen"
            )
        return None
    
    def _validate_response(self, response: str) -> bool:
        """Validate AI response quality.
        
        Args:
            response: AI response
            
        Returns:
            True if valid
        """
        # Check minimum length
        if len(response.strip()) < 10:
            return False
        
        # Check for placeholder text
        invalid_phrases = [
            "as an ai", "i cannot", "i don't have access",
            "i'm not able to", "i cannot provide"
        ]
        response_lower = response.lower()
        if any(phrase in response_lower for phrase in invalid_phrases):
            return False
        
        return True
    
    def _retry_with_exponential_backoff(self, func, *args, **kwargs) -> Any:
        """Retry function with exponential backoff.
        
        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Last exception if all retries fail
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return func(*args, **kwargs)
            except RateLimitError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    print(f"Rate limit hit, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
            except APIConnectionError as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    print(f"Connection error, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
            except APIError as e:
                last_exception = e
                print(f"API error: {e}")
                break  # Don't retry on general API errors
        
        raise last_exception
    
    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Get AI response for a message.
        
        Args:
            message: User message
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
            context: Additional context (e.g., user preferences from onboarding)
            
        Returns:
            AI response
            
        Raises:
            Exception: If AI call fails after retries
        """
        # Check for off-topic questions
        fallback = self._get_fallback_response(message)
        if fallback:
            return fallback
        
        # Build messages array
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        # Add context if available
        if context:
            context_prompt = self._build_context_prompt(context)
            if context_prompt:
                messages.append({"role": "system", "content": context_prompt})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages for context
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call OpenAI API with retry logic
        try:
            response = self._retry_with_exponential_backoff(
                self._call_openai,
                messages
            )
            
            # Validate response
            if not self._validate_response(response):
                return (
                    "Sorry, ik kon geen goed antwoord genereren. "
                    "Kun je je vraag anders formuleren? "
                    "Ik help je graag met vragen over Surinaams onderwijs!"
                )
            
            return response
            
        except Exception as e:
            print(f"AI service error: {e}")
            return (
                "Er ging iets mis bij het verwerken van je vraag. "
                "Probeer het later nog eens, of stel een andere vraag over Surinaams onderwijs!"
            )
    
    def _call_openai(self, messages: List[Dict[str, str]]) -> str:
        """Call OpenAI API with timeout.
        
        Args:
            messages: Messages array
            
        Returns:
            AI response
            
        Raises:
            TimeoutError: If request exceeds 30s
        """
        response = self.client.chat.completions.create(
            model=self.model,
            timeout=30.0,  # 30 second timeout
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        
        return response.choices[0].message.content.strip()
    
    def _build_context_prompt(self, context: Dict[str, Any]) -> Optional[str]:
        """Build context prompt from user preferences.
        
        Args:
            context: User context (from onboarding)
            
        Returns:
            Context prompt or None
        """
        parts = []
        
        # Education level
        if context.get("education"):
            education = ", ".join(context["education"])
            parts.append(f"De gebruiker volgt: {education}")
        
        # Age
        if context.get("age"):
            parts.append(f"Leeftijd: {context['age']}")
        
        # Favorite subjects
        if context.get("favorite_subjects"):
            subjects = ", ".join(context["favorite_subjects"])
            parts.append(f"Favoriete vakken: {subjects}")
        
        # Future plans
        if context.get("future_plans"):
            parts.append(f"Studieplannen: {context['future_plans']}")
        
        # Formality preference
        if context.get("formality"):
            formality_map = {
                "Heel formeel": "Gebruik een formele, professionele toon.",
                "Gewoon normaal": "Gebruik een vriendelijke, toegankelijke toon.",
                "Heel informeel": "Gebruik een casual, informele toon zoals je met een vriend praat."
            }
            if context["formality"] in formality_map:
                parts.append(formality_map[context["formality"]])
        
        if parts:
            return "Context over de gebruiker:\n" + "\n".join(parts)
        
        return None
    
    async def chat_stream(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Get AI response as a stream (for future streaming implementation).
        
        Args:
            message: User message
            conversation_history: Previous messages
            context: Additional context
            
        Yields:
            Response chunks
        """
        # For now, just return the full response
        # In the future, this can be implemented with OpenAI streaming
        response = self.chat(message, conversation_history, context)
        yield response


# Singleton instance
_ai_service = None


def get_ai_service(api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> AIService:
    """Get or create AI service singleton.
    
    Args:
        api_key: OpenAI API key
        model: Model to use
        
    Returns:
        AIService instance
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService(api_key=api_key, model=model)
    return _ai_service
