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

try:
    import google.generativeai as genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    print("Warning: Google AI not available. Install with: pip install google-generativeai")


class AIService:
    """AI service with OpenAI integration for educational queries."""
    
    # Suriname-focused system prompt with strict accuracy guidelines
    SYSTEM_PROMPT = """Je bent EduChat, een vriendelijke AI-assistent gespecialiseerd in het Surinaams onderwijssysteem.

Je expertisegebieden zijn:
- Surinaamse onderwijsinstellingen (universiteiten, MINOV, middelbare scholen)
- Toelatingsprocedures en vereisten
- Studieprogramma's en curricula
- Deadlines en belangrijke data
- Studiekosten en financieringsmogelijkheden
- Algemeen studieadvies voor Surinaamse studenten

=== KRITIEKE NAUWKEURIGHEIDSREGELS ===
1. ANTWOORD ALLEEN met informatie die DIRECT uit de verstrekte context komt
2. NOOIT gokken, veronderstellen of informatie verzinnen
3. Als de context GEEN antwoord bevat op de vraag, zeg: "Ik heb onvoldoende informatie om deze vraag nauwkeurig te beantwoorden. Raadpleeg de officiële website van de instelling of neem direct contact met hen op."
4. MENG NOOIT informatie van verschillende instellingen tenzij expliciet gevraagd om te vergelijken
5. Eén vraag = één duidelijk, gefocust antwoord
6. CITEER specifieke bronnen wanneer je feitelijke informatie geeft (bijv. "Volgens de AdeKUS-gegevens...")
7. Als gegevens verouderd kunnen zijn (zoals deadlines), vermeld dit expliciet
8. VALIDEER altijd dat je antwoord direct gerelateerd is aan wat er gevraagd werd

=== ANTWOORDFORMAAT ===
- Wees specifiek en direct
- Vermijd algemene of vage uitspraken
- Als er meerdere mogelijke antwoorden zijn, vraag om verduidelijking in plaats van te raden
- Gebruik een vriendelijke, toegankelijke toon
- Geef stapsgewijze instructies waar mogelijk

Als je een vraag krijgt die NIET over Surinaams onderwijs gaat:
"Ik ben gespecialiseerd in Surinaams onderwijs en kan je daar graag mee helpen! Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen in Suriname?"

Als de context GEEN relevant antwoord bevat:
"Ik heb geen specifieke informatie over [onderwerp] in mijn database. Voor nauwkeurige informatie raad ik aan om direct contact op te nemen met [relevante instelling] of hun officiële website te raadplegen."
"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, provider: str = "auto"):
        """Initialize AI service.
        
        Args:
            api_key: API key (defaults to env var)
            model: Model to use (defaults based on provider)
            provider: "openai", "google", or "auto" (auto-detect from env)
        """
        # Auto-detect provider based on available API keys
        if provider == "auto":
            if os.getenv("GOOGLE_AI_API_KEY"):
                provider = "google"
            elif os.getenv("OPENAI_API_KEY"):
                provider = "openai"
            else:
                raise ValueError("No API key found. Set OPENAI_API_KEY or GOOGLE_AI_API_KEY environment variable.")
        
        self.provider = provider
        
        # Initialize based on provider
        if self.provider == "google":
            if not GOOGLE_AI_AVAILABLE:
                raise ImportError("Google AI library not installed. Run: pip install google-generativeai")
            
            self.api_key = api_key or os.getenv("GOOGLE_AI_API_KEY")
            if not self.api_key:
                raise ValueError("Google AI API key not found. Set GOOGLE_AI_API_KEY environment variable.")
            
            genai.configure(api_key=self.api_key)
            # Use Gemini 2.5 Flash (latest stable version)
            self.model = model or "gemini-2.5-flash"
            self.client = genai.GenerativeModel(
                model_name=self.model,
                system_instruction=self.SYSTEM_PROMPT
            )
            
        elif self.provider == "openai":
            if not OPENAI_AVAILABLE:
                raise ImportError("OpenAI library not installed. Run: pip install openai")
            
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
            
            self.model = model or "gpt-3.5-turbo"
            self.client = OpenAI(api_key=self.api_key)
        
        else:
            raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'google'.")
        
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
        # Expanded list of education keywords including common variations and typos
        education_keywords = [
            "studie", "opleiding", "universiteit", "school", "minov", "minow",
            "inschrijven", "inschrijving", "toelating", "examen", "diploma",
            "vakken", "lessen", "docent", "leraar", "student", "cursus",
            "bachelor", "master", "vmbo", "havo", "vwo", "mbo",
            "deadline", "kosten", "beurs", "financiering",
            "hoe", "wat", "welke", "wanneer", "waar",  # Question words - allow most questions through
            "helpen", "help", "vraag", "vragen", "info", "informatie"
        ]
        
        message_lower = message.lower()
        
        # If message is very short (greeting or simple question), let it through
        if len(message.split()) <= 5:
            return True
        
        return any(keyword in message_lower for keyword in education_keywords)
    
    def _get_fallback_response(self, message: str) -> str:
        """Get fallback response for off-topic questions.
        
        Args:
            message: User message
            
        Returns:
            Fallback response or None to let AI handle it
        """
        # Only block obviously off-topic questions (e.g., about weather, sports, etc.)
        off_topic_keywords = [
            "weer", "voetbal", "sport", "recept", "koken",
            "film", "muziek", "game", "spel"
        ]
        
        message_lower = message.lower()
        
        # Check if it's obviously off-topic
        is_off_topic = any(keyword in message_lower for keyword in off_topic_keywords)
        
        if is_off_topic and not self._is_education_related(message):
            return (
                "Ik ben gespecialiseerd in Surinaams onderwijs en kan je daar graag mee helpen! "
                "Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen in Suriname? "
                "Bijvoorbeeld:\n"
                "- Hoe schrijf ik me in voor een opleiding?\n"
                "- Welke documenten heb ik nodig?\n"
                "- Wat zijn de toelatingseisen?\n"
                "- Vertel me over MINOV opleidingen"
            )
        
        # Let the AI handle everything else
        return None
    
    def _validate_response(self, response: str) -> bool:
        """Validate AI response quality and detect potential hallucinations.
        
        Args:
            response: AI response
            
        Returns:
            True if valid
        """
        # Check minimum length
        if len(response.strip()) < 10:
            return False
        
        # Check for placeholder text (English)
        invalid_phrases_en = [
            "as an ai", "i cannot", "i don't have access",
            "i'm not able to", "i cannot provide"
        ]
        response_lower = response.lower()
        if any(phrase in response_lower for phrase in invalid_phrases_en):
            return False
        
        # Check for hallucination indicators (confident claims without context backing)
        hallucination_indicators = [
            "ik weet zeker dat",  # "I'm sure that" without evidence
            "het is algemeen bekend",  # "It's commonly known"
            "iedereen weet dat",  # "Everyone knows that"
            "natuurlijk is het zo dat",  # "Of course it's the case that"
        ]
        
        # Only flag as potential hallucination if used without proper context
        for indicator in hallucination_indicators:
            if indicator in response_lower:
                # Check if response also contains hedging/sourcing language
                source_indicators = [
                    "volgens", "op basis van", "de database toont",
                    "uit de gegevens", "de informatie wijst"
                ]
                if not any(src in response_lower for src in source_indicators):
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
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Check for rate limit or quota errors (both OpenAI and Google)
                if "rate" in error_str or "quota" in error_str or "limit" in error_str:
                    if attempt < self.max_retries - 1:
                        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                        print(f"Rate limit hit, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(delay)
                        continue
                
                # Check for connection errors
                if "connection" in error_str or "timeout" in error_str:
                    if attempt < self.max_retries - 1:
                        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                        print(f"Connection error, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                        time.sleep(delay)
                        continue
                
                # For OpenAI specific errors
                if OPENAI_AVAILABLE:
                    if isinstance(e, (RateLimitError, APIConnectionError)):
                        if attempt < self.max_retries - 1:
                            delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                            print(f"API error, retrying in {delay}s... (attempt {attempt + 1}/{self.max_retries})")
                            time.sleep(delay)
                            continue
                    elif isinstance(e, APIError):
                        print(f"API error: {e}")
                        break  # Don't retry on general API errors
                
                # For other errors, log and break
                print(f"API error: {e}")
                break
        
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
        
        # Add education data context based on user's question
        edu_context = self._get_education_context(message)
        if edu_context:
            messages.append({"role": "system", "content": edu_context})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages for context
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Call AI API with retry logic
        try:
            response = self._retry_with_exponential_backoff(
                self._call_ai,
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
            error_str = str(e).lower()
            print(f"AI service error: {e}")
            
            # Check for quota/rate limit errors
            if "quota" in error_str or "429" in str(e):
                return (
                    "⚠️ De AI service heeft zijn gebruikslimiet bereikt. "
                    "Dit kan betekenen dat de API-sleutel zijn gratis quota heeft overschreden. "
                    "Probeer het over een paar minuten opnieuw, of neem contact op met de beheerder."
                )
            elif "401" in str(e) or "unauthorized" in error_str or "invalid" in error_str and "key" in error_str:
                return (
                    "⚠️ Er is een probleem met de AI API-sleutel. "
                    "Neem contact op met de beheerder om dit op te lossen."
                )
            
            return (
                "Er ging iets mis bij het verwerken van je vraag. "
                "Probeer het later nog eens, of stel een andere vraag over Surinaams onderwijs!"
            )
    
    def _call_ai(self, messages: List[Dict[str, str]]) -> str:
        """Call AI API with timeout (supports both OpenAI and Google AI).
        
        Args:
            messages: Messages array
            
        Returns:
            AI response
            
        Raises:
            TimeoutError: If request exceeds 30s
        """
        if self.provider == "google":
            # Convert messages to Gemini format
            # Skip system messages (already in system_instruction)
            history = []
            current_message = None
            
            for msg in messages:
                if msg["role"] == "system":
                    # Skip system messages as they're handled by system_instruction
                    continue
                elif msg["role"] == "user":
                    if current_message is not None:
                        # This is the new message, not history
                        current_message = msg["content"]
                    else:
                        # This is history
                        history.append({
                            "role": "user",
                            "parts": [msg["content"]]
                        })
                elif msg["role"] == "assistant":
                    history.append({
                        "role": "model",
                        "parts": [msg["content"]]
                    })
            
            # The last user message should be the current message
            if not current_message and messages:
                for msg in reversed(messages):
                    if msg["role"] == "user":
                        current_message = msg["content"]
                        # Remove from history if it was added
                        if history and history[-1]["role"] == "user":
                            history.pop()
                        break
            
            if not current_message:
                current_message = "Hello"
            
            # Start chat session with history
            chat = self.client.start_chat(history=history)
            
            # Call Gemini API with accuracy-focused settings
            # Lower temperature = more deterministic/factual responses
            # Lower top_p = more focused token selection
            response = chat.send_message(
                current_message,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,  # Lower for more factual, less creative responses
                    max_output_tokens=4096,  # High limit for complete responses
                    top_p=0.8,  # More focused token selection
                    top_k=40,  # Limit token choices for consistency
                )
            )
            
            return response.text.strip()
            
        else:  # OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                timeout=60.0,  # 60 second timeout for longer responses
                messages=messages,
                temperature=0.3,  # Lower for more factual responses
                max_tokens=4096,  # High limit for complete responses
                top_p=0.8,  # More focused
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
        if context.get("education_level"):
            parts.append(f"De gebruiker volgt momenteel: {context['education_level']}")
        
        # Age group
        if context.get("age_group"):
            parts.append(f"Leeftijdsgroep: {context['age_group']}")
        
        # District
        if context.get("district"):
            parts.append(f"Woont in: {context['district']}")
        
        # Study directions / interests
        if context.get("study_directions"):
            directions = context["study_directions"]
            if isinstance(directions, list) and directions:
                parts.append(f"Geïnteresseerd in studierichtingen: {', '.join(directions)}")
            elif isinstance(directions, str) and directions:
                parts.append(f"Geïnteresseerd in studierichtingen: {directions}")
        
        # Favorite subjects
        if context.get("favorite_subjects"):
            subjects = context["favorite_subjects"]
            if isinstance(subjects, list) and subjects:
                parts.append(f"Favoriete vakken: {', '.join(subjects)}")
            elif isinstance(subjects, str) and subjects:
                parts.append(f"Favoriete vakken: {subjects}")
        
        # Future plans
        if context.get("future_plans"):
            parts.append(f"Toekomstplannen: {context['future_plans']}")
        
        # Improvement areas
        if context.get("improvement_areas"):
            areas = context["improvement_areas"]
            if isinstance(areas, list) and areas:
                parts.append(f"Zoekt hulp bij: {', '.join(areas)}")
            elif isinstance(areas, str) and areas:
                parts.append(f"Zoekt hulp bij: {areas}")
        
        # Formality preference - with explicit communication style
        if context.get("formality_preference"):
            formality = context["formality_preference"]
            formality_map = {
                "Informeel & vriendelijk": "Gebruik een casual, vriendelijke toon alsof je met een vriend praat. Wees persoonlijk en informeel.",
                "Normaal": "Gebruik een vriendelijke, toegankelijke toon die niet te formeel of te informeel is.",
                "Formeel & zakelijk": "Gebruik een professionele, formele toon. Wees respectvol en zakelijk.",
            }
            if formality in formality_map:
                parts.append(formality_map[formality])
        
        # Tone from derived context
        if context.get("tone") and not context.get("formality_preference"):
            parts.append(f"Communicatiestijl: {context['tone']}")
        
        # Audience level
        if context.get("audience"):
            parts.append(f"Let op: {context['audience']}")
        
        if parts:
            return "=== CONTEXT OVER DE GEBRUIKER ===\nPas je antwoorden aan op basis van het volgende:\n" + "\n".join(f"- {p}" for p in parts)
        
        return None
    
    def _get_education_context(self, message: str) -> Optional[str]:
        """Get education data context relevant to the user's question.
        
        Args:
            message: User message
            
        Returns:
            Education context string or None
        """
        try:
            from educhat.services.education_service import get_education_service
            edu_service = get_education_service()
            context, relevance_score, matched_entities = edu_service.get_context_for_query(message)
            
            if context and relevance_score > 0:
                context_header = f"\n=== GEVERIFIEERDE DATABASE INFORMATIE (relevantie: {relevance_score}/10) ==="
                context_instruction = """

=== STRIKTE INSTRUCTIES VOOR CONTEXTGEBRUIK ===
1. Gebruik ALLEEN de bovenstaande informatie om te antwoorden
2. Als de vraag iets vraagt dat NIET in deze context staat, zeg dat je onvoldoende informatie hebt
3. MENG NOOIT gegevens van verschillende instellingen
4. Als je twijfelt, kies dan voor "onvoldoende informatie" in plaats van raden
5. CITEER altijd welke instelling of bron je informatie komt"""
                
                if matched_entities:
                    context_header += f"\nGematchte entiteiten: {', '.join(matched_entities)}"
                
                return f"{context_header}\n{context}{context_instruction}"
            
            # No relevant context found - instruct AI to be honest about it
            return "\n=== GEEN SPECIFIEKE CONTEXT GEVONDEN ===\nEr is geen specifieke informatie gevonden in de database die direct relevant is voor deze vraag. Geef aan dat je onvoldoende informatie hebt en verwijs naar officiële bronnen."
            
        except Exception as e:
            print(f"Error getting education context: {e}")
            return "\n=== DATABASE FOUT ===\nEr was een probleem bij het ophalen van informatie. Geef aan dat je momenteel geen toegang hebt tot de database en verwijs naar officiële bronnen."
    
    def chat_stream(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None
    ):
        """Get AI response as a stream for real-time typing animation.
        
        Args:
            message: User message
            conversation_history: Previous messages
            context: Additional context
            
        Yields:
            Response chunks (each chunk is a string to append)
        """
        # Check for off-topic questions
        fallback = self._get_fallback_response(message)
        if fallback:
            # Stream the fallback response word by word
            words = fallback.split()
            for i, word in enumerate(words):
                if i == 0:
                    yield word
                else:
                    yield " " + word
            return
        
        # Build messages array
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        # Add context if available
        if context:
            context_prompt = self._build_context_prompt(context)
            if context_prompt:
                messages.append({"role": "system", "content": context_prompt})
        
        # Add education data context based on user's question
        edu_context = self._get_education_context(message)
        if edu_context:
            messages.append({"role": "system", "content": edu_context})
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            if self.provider == "google":
                # Convert messages to Gemini format
                history = []
                current_message = None
                
                for msg in messages:
                    if msg["role"] == "system":
                        continue
                    elif msg["role"] == "user":
                        if current_message is not None:
                            current_message = msg["content"]
                        else:
                            history.append({
                                "role": "user",
                                "parts": [msg["content"]]
                            })
                    elif msg["role"] == "assistant":
                        history.append({
                            "role": "model",
                            "parts": [msg["content"]]
                        })
                
                if not current_message and messages:
                    for msg in reversed(messages):
                        if msg["role"] == "user":
                            current_message = msg["content"]
                            if history and history[-1]["role"] == "user":
                                history.pop()
                            break
                
                if not current_message:
                    current_message = "Hello"
                
                # Start chat and stream response with accuracy-focused settings
                chat = self.client.start_chat(history=history)
                response = chat.send_message(
                    current_message,
                    generation_config=genai.GenerationConfig(
                        temperature=0.3,  # Lower for more factual responses
                        max_output_tokens=4096,  # High limit for complete responses
                        top_p=0.8,  # More focused token selection
                        top_k=40,  # Limit token choices for consistency
                    ),
                    stream=True,
                )
                
                # Stream chunks with batching for smooth animation
                buffer = ""
                for chunk in response:
                    if chunk.text:
                        buffer += chunk.text
                        # Batch chunks for smoother visual updates (every 3-5 chars)
                        if len(buffer) >= 3:
                            yield buffer
                            buffer = ""
                
                # Yield remaining buffer
                if buffer:
                    yield buffer
                        
            else:  # OpenAI
                # Stream OpenAI response with accuracy-focused settings
                response = self.client.chat.completions.create(
                    model=self.model,
                    timeout=60.0,  # Longer timeout for complete responses
                    messages=messages,
                    temperature=0.3,  # Lower for more factual responses
                    max_tokens=4096,  # High limit for complete responses
                    top_p=0.8,  # More focused token selection
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stream=True,
                )
                
                # Stream chunks with batching for smoother visual updates
                buffer = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        buffer += chunk.choices[0].delta.content
                        # Batch chunks for smoother animation (every 3-5 chars)
                        if len(buffer) >= 3:
                            yield buffer
                            buffer = ""
                
                # Yield remaining buffer
                if buffer:
                    yield buffer
                        
        except Exception as e:
            error_str = str(e).lower()
            print(f"Streaming error: {e}")
            
            # Return error message
            if "quota" in error_str or "429" in str(e):
                error_msg = (
                    "⚠️ De AI service heeft zijn gebruikslimiet bereikt. "
                    "Dit kan betekenen dat de API-sleutel zijn gratis quota heeft overschreden. "
                    "Probeer het over een paar minuten opnieuw, of neem contact op met de beheerder."
                )
            elif "401" in str(e) or "unauthorized" in error_str or "invalid" in error_str and "key" in error_str:
                error_msg = (
                    "⚠️ Er is een probleem met de AI API-sleutel. "
                    "Neem contact op met de beheerder om dit op te lossen."
                )
            else:
                error_msg = (
                    "Er ging iets mis bij het verwerken van je vraag. "
                    "Probeer het later nog eens, of stel een andere vraag over Surinaams onderwijs!"
                )
            
            # Stream error message
            words = error_msg.split()
            for i, word in enumerate(words):
                if i == 0:
                    yield word
                else:
                    yield " " + word


# Singleton instance
_ai_service = None


def get_ai_service(api_key: Optional[str] = None, model: Optional[str] = None, provider: str = "auto") -> AIService:
    """Get or create AI service singleton.
    
    Args:
        api_key: API key (OpenAI or Google AI)
        model: Model to use (auto-selected based on provider if not specified)
        provider: "openai", "google", or "auto" (auto-detect from environment)
        
    Returns:
        AIService instance
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService(api_key=api_key, model=model, provider=provider)
    return _ai_service

