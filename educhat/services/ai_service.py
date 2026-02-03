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
    
    # Suriname-focused system prompt with strict accuracy guidelines - Dutch
    SYSTEM_PROMPT_NL = """Je bent EduChat, een vriendelijke AI-assistent gespecialiseerd in het Surinaams onderwijssysteem.

Je expertisegebieden zijn:
- Surinaamse onderwijsinstellingen (universiteiten, MINOV, middelbare scholen)
- Toelatingsprocedures en vereisten
- Studieprogramma's en curricula
- Deadlines en belangrijke data
- Studiekosten en financieringsmogelijkheden
- Algemeen studieadvies voor Surinaamse studenten

=== NAUWKEURIGHEID & HULPVAARDIGHEID ===
1. PRIMAIR: Gebruik informatie die DIRECT uit de verstrekte context komt
2. SECUNDAIR: Als context onvoldoende is, geef algemeen studieadvies gebaseerd op de onderwijscontext van Suriname
3. Wees ALTIJD DUIDELIJK over de bron:
   - "Volgens de database van [instelling]..." voor exacte context-data
   - "Op basis van algemene studierichtlijnen..." voor algemeen advies
   - "Dit is een algemene richtlijn, verifieer bij de instelling voor exacte details"
4. GEBRUIK gebruikerscontext (opleidingsniveau, leeftijd, interesses) om antwoorden te personaliseren
5. Als specifieke data ontbreekt (deadlines, vereisten):
   - Geef algemene richtlijnen voor dat type informatie
   - Adviseer waar de student de exacte informatie kan vinden
   - Suggereer contactmethoden (website, telefoonnummer, e-mail)
6. MENG NOOIT data van verschillende instellingen zonder dit expliciet te vermelden
7. Eén vraag = één duidelijk, gefocust antwoord met concrete stappen waar mogelijk
8. Bij verouderde data: vermeld dit + verwijs naar actuele bronnen

=== ANTWOORDFORMAAT ===
- Wees specifiek en direct
- Vermijd algemene of vage uitspraken
- Als er meerdere mogelijke antwoorden zijn, vraag om verduidelijking in plaats van te raden
- Gebruik een vriendelijke, toegankelijke toon
- Geef stapsgewijze instructies waar mogelijk

Als je een vraag krijgt die NIET over Surinaams onderwijs gaat:
"Ik ben gespecialiseerd in Surinaams onderwijs en kan je daar graag mee helpen! Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen in Suriname?"

Als specifieke context ontbreekt:
1. Geef algemene richtlijnen die voor de meeste Surinaamse instellingen gelden
2. Vermeld expliciet: "Dit is algemeen advies - voor [instelling]-specifieke details, raadpleeg..."
3. Suggereer concrete acties: "Bezoek [website], bel [algemeen nummer], of ga langs tijdens kantooruren"
4. Als de gebruiker vragen heeft die aansluiten bij hun onboarding-voorkeuren, gebruik die context om gericht advies te geven
"""
    
    # English system prompt
    SYSTEM_PROMPT_EN = """You are EduChat, a friendly AI assistant specialized in the Surinamese education system.

Your areas of expertise are:
- Surinamese educational institutions (universities, MINOV, secondary schools)
- Admission procedures and requirements
- Study programs and curricula
- Deadlines and important dates
- Study costs and financing options
- General study advice for Surinamese students

=== CRITICAL ACCURACY RULES ===
1. ONLY answer with information that comes DIRECTLY from the provided context
2. NEVER guess, assume, or make up information
3. If the context does NOT contain an answer to the question, say: "I don't have enough information to answer this question accurately. Please consult the official website of the institution or contact them directly."
4. NEVER mix information from different institutions unless explicitly asked to compare
5. One question = one clear, focused answer
6. CITE specific sources when giving factual information (e.g., "According to AdeKUS data...")
7. If data may be outdated (such as deadlines), mention this explicitly
8. ALWAYS validate that your answer is directly related to what was asked

=== RESPONSE FORMAT ===
- Be specific and direct
- Avoid general or vague statements
- If there are multiple possible answers, ask for clarification instead of guessing
- Use a friendly, accessible tone
- Provide step-by-step instructions where possible

If you receive a question that is NOT about Surinamese education:
"I specialize in Surinamese education and would be happy to help you with that! Do you have questions about studies, enrollments, or educational institutions in Suriname?"

If the context does NOT contain a relevant answer:
"I don't have specific information about [topic] in my database. For accurate information, I recommend contacting [relevant institution] directly or checking their official website."
"""
    
    # Keep legacy SYSTEM_PROMPT for backwards compatibility
    SYSTEM_PROMPT = SYSTEM_PROMPT_NL
    
    # Schoolwork-focused system prompts with anti-cheating guidelines - Dutch
    SCHOOLWORK_PROMPT_NL = """Je bent EduChat, een vriendelijke AI-leercoach gespecialiseerd in Surinaams onderwijs en schoolvakken.

Je helpt leerlingen met hun schoolwerk door ze te LEREN, niet door antwoorden te geven.

=== VAKGEBIEDEN ===
Je kunt helpen met:
- **Wiskunde** (rekenen, algebra, meetkunde, goniometrie, calculus)
- **Nederlands** (spelling, grammatica, literatuur, essays, tekstanalyse)
- **Engels** (grammatica, schrijfvaardigheid, literatuur, vocabulaire)
- **Programmeren/ICT** (Python, JavaScript, algoritmen, debugging, web development)
- **Andere vakken** (natuurkunde, scheikunde, biologie, geschiedenis, etc.)

Alle niveaus: GLO, MULO, LBGO, HAVO, VWO

=== ONDERWIJSAANPAK (VERPLICHT!) ===

**1. EERST BEGRIJPEN**
- Vraag ALTIJD: "Wat heb je tot nu toe geprobeerd?"
- Vraag: "Welk deel begrijp je niet precies?"
- Bepaal het opleidingsniveau en pas uitleg daarop aan

**2. CONCEPT LEREN, GEEN ANTWOORDEN**
- Leg uit WAAROM iets werkt, niet alleen HOE
- Gebruik stap-voor-stap uitleg
- Geef een VERGELIJKBAAR voorbeeld, NOOIT het exacte probleem
- Laat de leerling het zelf toepassen op hun specifieke vraag

**3. SOCRATISCHE METHODE**
- Stel sturende vragen: "Wat denk je dat de eerste stap is?"
- Hints geven in plaats van directe oplossingen
- Laat leerlingen hun redenering uitleggen

**4. GEBRUIK CURRICULUMKENNIS**
- Gebruik de curriculum data om uitleg aan te passen aan niveau
- Verwijs naar veelvoorkomende struikelblokken
- Gebruik Surinaams relevante voorbeelden waar mogelijk

=== ANTI-VALS SPELEN REGELS (STRIKT!) ===

**NOOIT:**
- Volledige huiswerken maken
- Hele essays of verslagen schrijven
- Complete code schrijven zonder uitleg
- Antwoorden geven op tentamenvragen tijdens tentamentijd
- Data of resultaten verzinnen voor verslagen

**WEL:**
- Concepten uitleggen met voorbeelden
- Structuur en aanpak bespreken (outline, stappenplan)
- Debugging tips en richtingen aangeven
- Formules uitleggen en toepassen op vergelijkbaar probleem
- Essays reviewen en verbeterpunten aangeven (geen herschrijven!)
- Stukje code analyseren en uitleggen hoe het werkt

**RODE VLAGGEN (LET OP):**
Als een leerling vraagt:
- "Geef me gewoon het antwoord"
- "Schrijf dit essay voor me"
- "Wat is de code voor [exact hun opdracht]"
- "Los deze som op" (zonder enige eigen poging)

**JE ANTWOORD DAN:**
"Ik help je graag leren hoe je dit zelf kunt oplossen! Laat me zien wat je tot nu toe hebt geprobeerd, dan kunnen we samen kijken waar je vastloopt. Dat is veel nuttiger dan als ik het gewoon voor je doe - dan leer je niks! 😊"

=== STAPPENPLAN VOOR HULP ===

**Wiskunde:**
1. Vraag wat ze al geprobeerd hebben
2. Leg het concept/formule uit
3. Werk een VERGELIJKBAAR voorbeeld uit (niet hun exacte som)
4. Laat hen hun eigen som proberen met hints
5. Check hun werk en geef feedback

**Nederlands/Engels schrijven:**
1. Vraag om hun onderwerp en wat ze al hebben
2. Bespreek structuur en opzet
3. Geef tips voor elk onderdeel (inleiding, argumenten, conclusie)
4. ALS ze al iets geschreven hebben: review en verbeterpunten
5. SCHRIJF NOOIT complete teksten - alleen tips en voorbeelden

**Programmeren:**
1. Vraag hun code en error messages
2. Leg het concept uit (loops, functies, etc.)
3. Toon VERGELIJKBAAR voorbeeld
4. Help met debugging aanpak: "Wat gebeurt er op regel X?"
5. Hints voor hun specifieke probleem, geen complete oplossing

=== ANTWOORDFORMAAT ===
- Gebruik duidelijke stappen en bullet points
- Gebruik emoji's voor vriendelijkheid (💡 📝 ✅ ❌)
- Code in code blocks: ```python
- Formules duidelijk: `a² + b² = c²`
- Vraag regelmatig: "Begrijp je dit zo ver?"

=== AANMOEDIGING ===
- Wees positief over pogingen, ook als het fout is
- "Goede poging!" of "Je bent al op de goede weg!"
- Vier successen: "Heel goed! Je snapt het! 🎉"
- Bij frustratie: "Dit is lastig, maar je kunt het leren!"

=== WANNEER DOORVERWIJZEN ===
Als het gaat om:
- Medische/psychologische problemen → schooldecaan of zorgcoördinator
- Pesten/veiligheid → mentor of directie
- Studiefinanciering → studiefinancieringsloket
- Toelatingseisen specifieke instelling → die instelling contacteren

ONTHOUD: Je doel is LEREN bevorderen, NIET huiswerk maken. Een leerling die het zelf oplost met jouw begeleiding leert 100x meer dan een leerling die het antwoord kopieert!"""

    # Schoolwork-focused system prompt - English
    SCHOOLWORK_PROMPT_EN = """You are EduChat, a friendly AI learning coach specialized in Surinamese education and school subjects.

You help students with their schoolwork by teaching them, NOT by giving answers.

=== SUBJECT AREAS ===
You can help with:
- **Mathematics** (arithmetic, algebra, geometry, trigonometry, calculus)
- **Dutch Language** (spelling, grammar, literature, essays, text analysis)
- **English Language** (grammar, writing skills, literature, vocabulary)
- **Programming/ICT** (Python, JavaScript, algorithms, debugging, web development)
- **Other subjects** (physics, chemistry, biology, history, etc.)

All levels: GLO, MULO, LBGO, HAVO, VWO

=== TEACHING APPROACH (MANDATORY!) ===

**1. UNDERSTAND FIRST**
- ALWAYS ask: "What have you tried so far?"
- Ask: "Which part don't you understand exactly?"
- Determine education level and adapt explanation accordingly

**2. TEACH CONCEPTS, NOT ANSWERS**
- Explain WHY something works, not just HOW
- Use step-by-step explanations
- Give a SIMILAR example, NEVER their exact problem
- Let the student apply it to their specific question

**3. SOCRATIC METHOD**
- Ask guiding questions: "What do you think the first step is?"
- Give hints instead of direct solutions
- Have students explain their reasoning

**4. USE CURRICULUM KNOWLEDGE**
- Use curriculum data to adapt explanations to level
- Reference common difficulties
- Use Surinamese-relevant examples where possible

=== ANTI-CHEATING RULES (STRICT!) ===

**NEVER:**
- Complete entire homework assignments
- Write full essays or reports
- Write complete code without explanation
- Give answers to exam questions during exam time
- Make up data or results for reports

**DO:**
- Explain concepts with examples
- Discuss structure and approach (outline, step plan)
- Give debugging tips and directions
- Explain formulas and apply to similar problem
- Review essays and point out improvements (no rewriting!)
- Analyze code snippet and explain how it works

**RED FLAGS (WATCH OUT):**
When a student asks:
- "Just give me the answer"
- "Write this essay for me"
- "What's the code for [exactly their assignment]"
- "Solve this problem" (without any own attempt)

**YOUR RESPONSE THEN:**
"I'm happy to help you learn how to solve this yourself! Show me what you've tried so far, and we can look together at where you're stuck. That's much more useful than if I just do it for you - then you don't learn anything! 😊"

=== STEP-BY-STEP HELP PLAN ===

**Mathematics:**
1. Ask what they've already tried
2. Explain the concept/formula
3. Work through a SIMILAR example (not their exact problem)
4. Let them try their own problem with hints
5. Check their work and give feedback

**Dutch/English writing:**
1. Ask about their topic and what they already have
2. Discuss structure and setup
3. Give tips for each part (intro, arguments, conclusion)
4. IF they've already written something: review and improvement points
5. NEVER write complete texts - only tips and examples

**Programming:**
1. Ask for their code and error messages
2. Explain the concept (loops, functions, etc.)
3. Show SIMILAR example
4. Help with debugging approach: "What happens on line X?"
5. Hints for their specific problem, no complete solution

=== RESPONSE FORMAT ===
- Use clear steps and bullet points
- Use emojis for friendliness (💡 📝 ✅ ❌)
- Code in code blocks: ```python
- Formulas clearly: `a² + b² = c²`
- Ask regularly: "Do you understand so far?"

=== ENCOURAGEMENT ===
- Be positive about attempts, even if wrong
- "Good try!" or "You're on the right track!"
- Celebrate successes: "Very good! You got it! 🎉"
- With frustration: "This is difficult, but you can learn it!"

=== WHEN TO REFER ===
When it's about:
- Medical/psychological problems → school counselor
- Bullying/safety → mentor or administration
- Study financing → student finance office
- Admission requirements specific institution → contact that institution

REMEMBER: Your goal is to promote LEARNING, NOT do homework. A student who solves it themselves with your guidance learns 100x more than a student who copies the answer!"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, provider: str = "auto", language: str = "nl"):
        """Initialize AI service.
        
        Args:
            api_key: API key (defaults to env var)
            model: Model to use (defaults based on provider)
            provider: "openai", "google", or "auto" (auto-detect from env)
            language: Response language "nl" (Dutch) or "en" (English)
        """
        self.language = language
        
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
    
    def get_system_prompt(self, language: str = None, mode: str = "institutions") -> str:
        """Get the system prompt for the specified language and mode.
        
        Args:
            language: "nl" for Dutch, "en" for English. Defaults to instance language.
            mode: "institutions" for school info, "schoolwork" for homework help
            
        Returns:
            System prompt string
        """
        lang = language or self.language
        
        if mode == "schoolwork":
            return self.SCHOOLWORK_PROMPT_EN if lang == "en" else self.SCHOOLWORK_PROMPT_NL
        else:
            return self.SYSTEM_PROMPT_EN if lang == "en" else self.SYSTEM_PROMPT_NL
    
    def set_language(self, language: str):
        """Set the response language.
        
        Args:
            language: "nl" for Dutch, "en" for English
        """
        if language in ["nl", "en"]:
            self.language = language
    
    def _is_education_related(self, message: str) -> bool:
        """Check if message is related to education.
        
        Args:
            message: User message
            
        Returns:
            True if education-related
        """
        # Expanded list of education keywords including common variations and typos
        # Includes both Dutch and English keywords
        education_keywords = [
            # Dutch
            "studie", "opleiding", "universiteit", "school", "minov", "minow",
            "inschrijven", "inschrijving", "toelating", "examen", "diploma",
            "vakken", "lessen", "docent", "leraar", "student", "cursus",
            "bachelor", "master", "vmbo", "havo", "vwo", "mbo",
            "deadline", "kosten", "beurs", "financiering",
            "hoe", "wat", "welke", "wanneer", "waar",
            "helpen", "help", "vraag", "vragen", "info", "informatie",
            # English
            "study", "education", "university", "college", "enrollment", "enroll",
            "admission", "exam", "degree", "subjects", "classes", "teacher",
            "professor", "tuition", "scholarship", "requirements",
            "how", "what", "which", "when", "where", "question"
        ]
        
        message_lower = message.lower()
        
        # If message is very short (greeting or simple question), let it through
        if len(message.split()) <= 5:
            return True
        
        return any(keyword in message_lower for keyword in education_keywords)
    
    def _get_fallback_response(self, message: str, language: str = None) -> str:
        """Get fallback response for off-topic questions.
        
        Args:
            message: User message
            language: Response language
            
        Returns:
            Fallback response or None to let AI handle it
        """
        lang = language or self.language
        
        # Only block obviously off-topic questions (e.g., about weather, sports, etc.)
        off_topic_keywords = [
            "weer", "voetbal", "sport", "recept", "koken",
            "film", "muziek", "game", "spel",
            "weather", "football", "soccer", "recipe", "cooking",
            "movie", "music"
        ]
        
        message_lower = message.lower()
        
        # Check if it's obviously off-topic
        is_off_topic = any(keyword in message_lower for keyword in off_topic_keywords)
        
        if is_off_topic and not self._is_education_related(message):
            if lang == "en":
                return (
                    "I specialize in Surinamese education and would be happy to help you with that! "
                    "Do you have questions about studies, enrollments, or educational institutions in Suriname? "
                    "For example:\n"
                    "- How do I enroll in a program?\n"
                    "- What documents do I need?\n"
                    "- What are the admission requirements?\n"
                    "- Tell me about MINOV programs"
                )
            else:
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
            "i'm certain that",
            "it's well known",
            "everyone knows",
        ]
        
        # Only flag as potential hallucination if used without proper context
        for indicator in hallucination_indicators:
            if indicator in response_lower:
                # Check if response also contains hedging/sourcing language
                source_indicators = [
                    "volgens", "op basis van", "de database toont",
                    "uit de gegevens", "de informatie wijst",
                    "according to", "based on", "the data shows",
                    "from the information"
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
    
    def analyze_query_for_scraping(self, message: str) -> Dict[str, Any]:
        """Analyze user query to determine if scraping is needed and what to scrape.
        
        Args:
            message: User message to analyze
            
        Returns:
            Dictionary with scraping recommendations:
            {
                "should_scrape": bool,
                "scrape_type": "events" | "institutions" | "general",
                "institutions": List[str],  # Specific institutions to focus on
                "keywords": List[str],  # Keywords for focused scraping
            }
        """
        message_lower = message.lower()
        
        # Institution names to detect
        institutions = {
            "adekus": ["adekus", "ade kus", "anton de kom"],
            "iob": ["iob", "institute of business"],
            "natin": ["natin", "nationaal"],
            "ptc": ["ptc", "polytechnic"],
            "ahkco": ["ahkco"],
            "fhi": ["fhi", "ferrier"],
            "minov": ["minov", "ministerie van onderwijs"],
            "imeao": ["imeao"],
            "sma": ["sma", "surinaams management"],
        }
        
        # Event/deadline-related keywords
        event_keywords = [
            "deadline", "inschrijving", "aanmeld", "open dag", "open day",
            "examen", "test", "intake", "selectie", "wanneer", "when",
            "datum", "date", "tijdstip", "time", "periode", "period",
            "evenement", "event", "activiteit", "activity"
        ]
        
        # Program/curriculum keywords
        program_keywords = [
            "programma", "program", "opleiding", "studie", "study",
            "vakken", "subjects", "curriculum", "cursus", "course",
            "bachelor", "master", "diploma", "certificaat", "certificate"
        ]
        
        # Requirements keywords
        requirement_keywords = [
            "vereisten", "requirements", "toelating", "admission",
            "nodig", "need", "moet", "should", "voorwaarden", "conditions",
            "diploma", "cijfers", "grades", "punten", "points"
        ]
        
        # Detect mentioned institutions
        detected_institutions = []
        for inst_key, variations in institutions.items():
            if any(var in message_lower for var in variations):
                detected_institutions.append(inst_key)
        
        # Determine scrape type
        should_scrape = False
        scrape_type = "general"
        keywords = []
        
        # Check for event-related queries
        if any(keyword in message_lower for keyword in event_keywords):
            should_scrape = True
            scrape_type = "events"
            keywords.extend([k for k in event_keywords if k in message_lower])
        
        # Check for program queries
        elif any(keyword in message_lower for keyword in program_keywords):
            should_scrape = True
            scrape_type = "institutions"
            keywords.extend([k for k in program_keywords if k in message_lower])
        
        # Check for requirement queries
        elif any(keyword in message_lower for keyword in requirement_keywords):
            should_scrape = True
            scrape_type = "institutions"
            keywords.extend([k for k in requirement_keywords if k in message_lower])
        
        # If institutions mentioned, definitely should scrape
        if detected_institutions:
            should_scrape = True
            if scrape_type == "general":
                scrape_type = "institutions"
        
        return {
            "should_scrape": should_scrape,
            "scrape_type": scrape_type,
            "institutions": detected_institutions,
            "keywords": keywords[:5],  # Limit to top 5 keywords
        }
    
    def chat(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        language: str = None
    ) -> str:
        """Get AI response for a message.
        
        Args:
            message: User message
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
            context: Additional context (e.g., user preferences from onboarding)
            language: Response language ("nl" or "en"), defaults to instance language
            
        Returns:
            AI response
            
        Raises:
            Exception: If AI call fails after retries
        """
        lang = language or self.language
        
        # Check for off-topic questions
        fallback = self._get_fallback_response(message, lang)
        if fallback:
            return fallback
        
        # Detect if this is schoolwork-related and which subjects
        subject_detection = self.detect_subject_and_level(message, context)
        mode = subject_detection.get("mode", "institutions")
        
        # Build messages array with language-appropriate system prompt for the detected mode
        system_prompt = self.get_system_prompt(lang, mode)
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add context if available
        if context:
            context_prompt = self._build_context_prompt(context, lang)
            if context_prompt:
                messages.append({"role": "system", "content": context_prompt})
        
        # If schoolwork mode, add curriculum and examples context
        if mode == "schoolwork":
            # Add curriculum context
            curriculum_context = self._get_curriculum_context(
                subject_detection.get("subjects", []),
                subject_detection.get("education_level"),
                subject_detection.get("topics", [])
            )
            if curriculum_context:
                messages.append({"role": "system", "content": curriculum_context})
            
            # Add teaching examples context
            examples_context = self._get_example_context(
                subject_detection.get("subjects", []),
                subject_detection.get("topics", [])
            )
            if examples_context:
                messages.append({"role": "system", "content": examples_context})
        else:
            # Add education data context for institutions mode
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
                if lang == "en":
                    return (
                        "Sorry, I couldn't generate a good response. "
                        "Could you rephrase your question? "
                        "I'm happy to help with questions about Surinamese education!"
                    )
                else:
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
                if lang == "en":
                    return (
                        "⚠️ The AI service has reached its usage limit. "
                        "This may mean the API key has exceeded its free quota. "
                        "Please try again in a few minutes, or contact the administrator."
                    )
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
    
    def _build_context_prompt(self, context: Dict[str, Any], language: str = "nl") -> Optional[str]:
        """Build context prompt from user preferences.
        
        Args:
            context: User context (from onboarding)
            language: Response language ("nl" or "en")
            
        Returns:
            Context prompt or None
        """
        parts = []
        
        if language == "en":
            # English context building
            if context.get("education_level"):
                parts.append(f"The user is currently studying: {context['education_level']}")
            
            if context.get("age_group"):
                parts.append(f"Age group: {context['age_group']}")
            
            if context.get("district"):
                parts.append(f"Lives in: {context['district']}")
            
            if context.get("study_directions"):
                directions = context["study_directions"]
                if isinstance(directions, list) and directions:
                    parts.append(f"Interested in study directions: {', '.join(directions)}")
                elif isinstance(directions, str) and directions:
                    parts.append(f"Interested in study directions: {directions}")
            
            if context.get("favorite_subjects"):
                subjects = context["favorite_subjects"]
                if isinstance(subjects, list) and subjects:
                    parts.append(f"Favorite subjects: {', '.join(subjects)}")
                elif isinstance(subjects, str) and subjects:
                    parts.append(f"Favorite subjects: {subjects}")
            
            if context.get("future_plans"):
                parts.append(f"Future plans: {context['future_plans']}")
            
            if context.get("improvement_areas"):
                areas = context["improvement_areas"]
                if isinstance(areas, list) and areas:
                    parts.append(f"Looking for help with: {', '.join(areas)}")
                elif isinstance(areas, str) and areas:
                    parts.append(f"Looking for help with: {areas}")
            
            if context.get("formality_preference"):
                formality = context["formality_preference"]
                formality_map = {
                    "Informeel & vriendelijk": "Use a casual, friendly tone as if talking to a friend. Be personal and informal.",
                    "Normaal": "Use a friendly, accessible tone that's not too formal or informal.",
                    "Formeel & zakelijk": "Use a professional, formal tone. Be respectful and businesslike.",
                    "informal": "Use a casual, friendly tone as if talking to a friend.",
                    "normal": "Use a friendly, accessible tone that's not too formal or informal.",
                    "formal": "Use a professional, formal tone. Be respectful and businesslike.",
                }
                if formality in formality_map:
                    parts.append(formality_map[formality])
            
            if context.get("tone") and not context.get("formality_preference"):
                parts.append(f"Communication style: {context['tone']}")
        else:
            # Dutch context building (original)
            if context.get("education_level"):
                parts.append(f"De gebruiker volgt momenteel: {context['education_level']}")
            
            if context.get("age_group"):
                parts.append(f"Leeftijdsgroep: {context['age_group']}")
            
            if context.get("district"):
                parts.append(f"Woont in: {context['district']}")
            
            if context.get("study_directions"):
                directions = context["study_directions"]
                if isinstance(directions, list) and directions:
                    parts.append(f"Geïnteresseerd in studierichtingen: {', '.join(directions)}")
                elif isinstance(directions, str) and directions:
                    parts.append(f"Geïnteresseerd in studierichtingen: {directions}")
            
            if context.get("favorite_subjects"):
                subjects = context["favorite_subjects"]
                if isinstance(subjects, list) and subjects:
                    parts.append(f"Favoriete vakken: {', '.join(subjects)}")
                elif isinstance(subjects, str) and subjects:
                    parts.append(f"Favoriete vakken: {subjects}")
            
            if context.get("future_plans"):
                parts.append(f"Toekomstplannen: {context['future_plans']}")
            
            if context.get("improvement_areas"):
                areas = context["improvement_areas"]
                if isinstance(areas, list) and areas:
                    parts.append(f"Zoekt hulp bij: {', '.join(areas)}")
                elif isinstance(areas, str) and areas:
                    parts.append(f"Zoekt hulp bij: {areas}")
            
            if context.get("formality_preference"):
                formality = context["formality_preference"]
                formality_map = {
                    "Informeel & vriendelijk": "Gebruik een casual, vriendelijke toon alsof je met een vriend praat. Wees persoonlijk en informeel.",
                    "Normaal": "Gebruik een vriendelijke, toegankelijke toon die niet te formeel of te informeel is.",
                    "Formeel & zakelijk": "Gebruik een professionele, formele toon. Wees respectvol en zakelijk.",
                    "informal": "Gebruik een casual, vriendelijke toon.",
                    "normal": "Gebruik een vriendelijke, toegankelijke toon.",
                    "formal": "Gebruik een professionele, formele toon.",
                }
                if formality in formality_map:
                    parts.append(formality_map[formality])
            
            if context.get("tone") and not context.get("formality_preference"):
                parts.append(f"Communicatiestijl: {context['tone']}")
        
        # Audience level (same for both languages)
        if context.get("audience"):
            parts.append(f"Let op: {context['audience']}")
        
        # Add scraped events context if available
        if context.get("scraped_events"):
            parts.append(context["scraped_events"])
        
        if parts:
            return "=== CONTEXT OVER DE GEBRUIKER ===\nPas je antwoorden aan op basis van het volgende:\n" + "\n".join(f"- {p}" for p in parts)
        
        return None
    
    def _load_curriculum_data(self) -> Optional[Dict]:
        """Load curriculum data from JSON file.
        
        Returns:
            Curriculum data dictionary or None if loading fails
        """
        try:
            import json
            import os
            
            # Get the path to curriculum.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', '..', 'data', 'curriculum.json')
            
            if not os.path.exists(data_path):
                print(f"Curriculum file not found at {data_path}")
                return None
            
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading curriculum data: {e}")
            return None
    
    def _load_subject_examples(self) -> Optional[Dict]:
        """Load subject examples from JSON file.
        
        Returns:
            Subject examples dictionary or None if loading fails
        """
        try:
            import json
            import os
            
            # Get the path to subject_examples.json
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, '..', '..', 'data', 'subject_examples.json')
            
            if not os.path.exists(data_path):
                print(f"Subject examples file not found at {data_path}")
                return None
            
            with open(data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading subject examples: {e}")
            return None
    
    def detect_subject_and_level(self, message: str, user_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Detect if the message is about schoolwork and which subject/level.
        
        Args:
            message: User message
            user_context: User onboarding context with education level
            
        Returns:
            Dictionary with:
            {
                "is_schoolwork": bool,
                "subjects": List[str],  # e.g., ["wiskunde", "nederlands"]
                "education_level": str,  # e.g., "HAVO"
                "topics": List[str],  # e.g., ["algebra", "vergelijkingen"]
                "mode": "schoolwork" | "institutions"
            }
        """
        message_lower = message.lower()
        
        # Subject keywords mapping
        subject_keywords = {
            "wiskunde": ["wiskunde", "math", "rekenen", "algebra", "meetkunde", "goniometrie", 
                        "calculus", "som", "formule", "vergelijking", "functie", "grafiek"],
            "nederlands": ["nederlands", "dutch", "spelling", "grammatica", "essay", "opstel", 
                          "literatuur", "d/t", "werkwoord", "zinsdeel", "schrijven"],
            "engels": ["engels", "english", "grammar", "tense", "writing", "vocabulary"],
            "programmeren": ["programmeren", "programming", "code", "python", "javascript", 
                            "java", "function", "loop", "algorithm", "debug", "error", "syntax"],
            "natuurkunde": ["natuurkunde", "physics", "kracht", "energie", "beweging"],
            "scheikunde": ["scheikunde", "chemistry", "molecuul", "reactie", "element"],
            "biologie": ["biologie", "biology", "cel", "dna", "evolutie", "ecosysteem"],
            "geschiedenis": ["geschiedenis", "history", "oorlog", "revolutie", "eeuw"],
            "aardrijkskunde": ["aardrijkskunde", "geography", "land", "klimaat", "kaart"]
        }
        
        # Homework indicators
        homework_indicators = [
            "huiswerk", "homework", "opdracht", "assignment", "oefening", "practice",
            "help me", "help mij", "hoe", "how", "uitleg", "explain", "oplossen", "solve",
            "snap niet", "don't understand", "begrijp niet", "stuck", "vastgelopen",
            "examen", "exam", "toets", "test", "oefenen", "studeren", "study"
        ]
        
        # Detect subjects
        detected_subjects = []
        detected_topics = []
        
        for subject, keywords in subject_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_subjects.append(subject)
                # Add the matched keywords as topics
                detected_topics.extend([kw for kw in keywords if kw in message_lower])
        
        # Check if it's homework-related
        is_homework = any(indicator in message_lower for indicator in homework_indicators)
        is_schoolwork = is_homework or (len(detected_subjects) > 0)
        
        # Get education level from user context
        education_level = None
        if user_context and user_context.get("education_level"):
            education_level = user_context["education_level"]
        
        return {
            "is_schoolwork": is_schoolwork,
            "subjects": detected_subjects,
            "education_level": education_level,
            "topics": list(set(detected_topics)),  # Remove duplicates
            "mode": "schoolwork" if is_schoolwork else "institutions"
        }
    
    def _get_curriculum_context(self, subjects: List[str], education_level: Optional[str], topics: List[str]) -> Optional[str]:
        """Get curriculum context for detected subjects.
        
        Args:
            subjects: List of detected subjects
            education_level: User's education level
            topics: Detected topics
            
        Returns:
            Curriculum context string or None
        """
        if not subjects:
            return None
        
        curriculum_data = self._load_curriculum_data()
        if not curriculum_data:
            return None
        
        context_parts = []
        context_parts.append("\n=== CURRICULUM INFORMATIE ===")
        
        for subject in subjects:
            subject_data = curriculum_data.get("subjects", {}).get(subject)
            if not subject_data:
                continue
            
            context_parts.append(f"\n**VAK: {subject_data.get('name_nl', subject.upper())}**")
            
            # Add level-specific information
            if education_level:
                level_data = subject_data.get("education_levels", {}).get(education_level)
                if level_data:
                    context_parts.append(f"Niveau: {level_data.get('level_name')} ({level_data.get('age_range')})")
                    
                    # Add relevant topics for this level
                    topics_data = level_data.get("topics", [])
                    if topics_data:
                        context_parts.append("\nRelevante onderwerpen voor dit niveau:")
                        for topic in topics_data[:3]:  # Limit to top 3 topics
                            context_parts.append(f"- {topic.get('name')}: {', '.join(topic.get('subtopics', [])[:3])}")
                            if topic.get('common_difficulties'):
                                context_parts.append(f"  Veelvoorkomende struikelblokken: {', '.join(topic.get('common_difficulties', [])[:2])}")
            
            # Add exam prep strategies
            if subject_data.get("exam_prep_strategies"):
                context_parts.append(f"\nStudietips voor {subject}:")
                for strategy in subject_data.get("exam_prep_strategies", [])[:3]:
                    context_parts.append(f"- {strategy}")
            
            # Add anti-cheating approach
            if subject_data.get("anti_cheating_approach"):
                context_parts.append(f"\n⚠️ Aanpak: {subject_data['anti_cheating_approach']}")
        
        # Add general teaching principles
        general_principles = curriculum_data.get("general_teaching_principles", {})
        if general_principles:
            context_parts.append("\n=== LESPRINCIPES ===")
            for key, value in list(general_principles.items())[:5]:
                context_parts.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        return "\n".join(context_parts)
    
    def _get_example_context(self, subjects: List[str], topics: List[str]) -> Optional[str]:
        """Get teaching examples for detected subjects.
        
        Args:
            subjects: List of detected subjects
            topics: Detected topics
            
        Returns:
            Examples context string or None
        """
        if not subjects:
            return None
        
        examples_data = self._load_subject_examples()
        if not examples_data:
            return None
        
        context_parts = []
        context_parts.append("\n=== VOORBEELDEN VOOR UITLEG ===")
        context_parts.append("Gebruik deze als REFERENTIE voor je uitleg, niet als directe antwoorden!")
        
        for subject in subjects:
            subject_examples = examples_data.get("examples", {}).get(subject)
            if not subject_examples:
                continue
            
            # Add up to 2 relevant examples per subject
            example_count = 0
            for example_key, example_data in subject_examples.items():
                if example_count >= 2:
                    break
                
                # Check if example is relevant to detected topics
                if topics:
                    example_text = str(example_data).lower()
                    if not any(topic.lower() in example_text for topic in topics):
                        continue
                
                if isinstance(example_data, dict) and example_data.get("concept"):
                    context_parts.append(f"\n**Voorbeeld: {example_data.get('concept')}**")
                    if example_data.get("step_by_step"):
                        context_parts.append("Stappenplan:")
                        for step in example_data["step_by_step"]:
                            context_parts.append(f"  {step}")
                    if example_data.get("similar_practice"):
                        context_parts.append(f"Oefenopdracht: {example_data['similar_practice']}")
                    example_count += 1
        
        # Add teaching strategies
        strategies = examples_data.get("teaching_strategies", {})
        if strategies.get("when_student_asks_for_help"):
            context_parts.append("\n=== AANPAK VOOR HULP ===")
            for step in strategies["when_student_asks_for_help"]:
                context_parts.append(f"- {step}")
        
        return "\n".join(context_parts)
    
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
        
        # Detect if this is schoolwork-related and which subjects
        subject_detection = self.detect_subject_and_level(message, context)
        mode = subject_detection.get("mode", "institutions")
        
        # Select appropriate system prompt based on mode
        system_prompt = self.get_system_prompt(self.language, mode)
        
        # Build messages array
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add context if available
        if context:
            context_prompt = self._build_context_prompt(context)
            if context_prompt:
                messages.append({"role": "system", "content": context_prompt})
        
        # If schoolwork mode, add curriculum and examples context
        if mode == "schoolwork":
            # Add curriculum context
            curriculum_context = self._get_curriculum_context(
                subject_detection.get("subjects", []),
                subject_detection.get("education_level"),
                subject_detection.get("topics", [])
            )
            if curriculum_context:
                messages.append({"role": "system", "content": curriculum_context})
            
            # Add teaching examples context
            examples_context = self._get_example_context(
                subject_detection.get("subjects", []),
                subject_detection.get("topics", [])
            )
            if examples_context:
                messages.append({"role": "system", "content": examples_context})
        else:
            # Add education data context for institutions mode
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


    async def get_chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_message: Optional[str] = None
    ) -> Optional[str]:
        """Get chat completion asynchronously (for async contexts like event scraping).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum response tokens
            system_message: Optional custom system message
        
        Returns:
            Response text or None on error
        """
        try:
            if self.provider == "google":
                # Build conversation
                chat = self.client.start_chat(history=[])
                
                # Send all messages
                for msg in messages:
                    if msg["role"] == "user":
                        response = chat.send_message(msg["content"])
                
                return response.text
                
            elif self.provider == "openai":
                # Build messages with system prompt
                full_messages = []
                if system_message:
                    full_messages.append({"role": "system", "content": system_message})
                else:
                    full_messages.append({"role": "system", "content": self.SYSTEM_PROMPT})
                
                full_messages.extend(messages)
                
                # Get completion
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=full_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                
                return response.choices[0].message.content
                
        except Exception as e:
            print(f"Error in async chat completion: {e}")
            return None
    
    async def generate_practice_problem(
        self,
        subject: str,
        education_level: str,
        topic: Optional[str] = None,
        difficulty: str = "medium",
        user_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a custom practice problem for a specific subject and topic.
        
        This method creates practice problems that:
        - Match the curriculum and education level
        - Follow anti-cheating principles (teach concepts, not give answers)
        - Include hints and step-by-step guidance
        - Are culturally relevant (Surinamese context where applicable)
        
        Args:
            subject: Subject name (e.g., "wiskunde", "natuurkunde")
            education_level: Education level (e.g., "GLO", "MULO", "HAVO", "VWO")
            topic: Optional specific topic within the subject
            difficulty: Difficulty level ("easy", "medium", "hard")
            user_context: Optional user context for personalization
        
        Returns:
            Dict with:
                - problem: The problem statement
                - hints: List of progressive hints
                - solution_approach: General approach without full answer
                - related_concept: The underlying concept being tested
                - success: Boolean indicating if generation was successful
        """
        try:
            # Load curriculum data to get relevant topics
            curriculum = self._load_curriculum_data()
            
            if not curriculum or subject not in curriculum.get("subjects", {}):
                return {
                    "success": False,
                    "error": f"Subject '{subject}' not found in curriculum"
                }
            
            subject_data = curriculum["subjects"][subject]
            
            # Get education level data
            levels = subject_data.get("education_levels", {})
            if education_level not in levels:
                return {
                    "success": False,
                    "error": f"Education level '{education_level}' not available for {subject}"
                }
            
            level_data = levels[education_level]
            
            # Get topic info
            topics = level_data.get("topics", [])
            if not topics:
                return {
                    "success": False,
                    "error": f"No topics found for {subject} at {education_level} level"
                }
            
            # Select topic (specific or random)
            selected_topic = None
            if topic:
                # Find matching topic
                for t in topics:
                    if topic.lower() in t.get("name", "").lower():
                        selected_topic = t
                        break
            
            if not selected_topic:
                # Pick random topic
                import random
                selected_topic = random.choice(topics)
            
            # Build practice problem generation prompt
            difficulty_guidance = {
                "easy": "basis niveau, eenvoudige concepten, rechttoe rechtaan",
                "medium": "gemiddeld niveau, meerdere stappen, conceptueel begrip vereist",
                "hard": "uitdagend niveau, complexe toepassing, kritisch denken vereist"
            }
            
            practice_prompt = f"""Genereer een oefenopgave voor een Surinaamse leerling.

VEREISTEN:
- Vak: {subject_data.get('name_nl', subject)}
- Onderwerp: {selected_topic.get('name', 'algemeen')}
- Niveau: {education_level} ({level_data.get('age_range', '')} jaar)
- Moeilijkheidsgraad: {difficulty} ({difficulty_guidance.get(difficulty, 'medium')})

ONDERWERP DETAILS:
- Subtopics: {', '.join(selected_topic.get('subtopics', []))}
- Leerdoelen: {'; '.join(selected_topic.get('learning_objectives', [])[:2])}
- Veelvoorkomende problemen: {'; '.join(selected_topic.get('common_difficulties', [])[:2])}

CULTURELE CONTEXT:
Gebruik waar mogelijk Surinaamse voorbeelden (bijv. Afobaka dam voor energie, Surinaamse rivier voor geografie, lokale producten voor economie, etc.)

ANTI-CHEATING PRINCIPES:
1. Geef NIET de volledige oplossing
2. Geef hints die stapsgewijs helpen
3. Focus op begrip van het concept
4. Gebruik vergelijkbare voorbeelden uit subject_examples.json

{f'LEERLING CONTEXT: {user_context}' if user_context else ''}

GENEREER (in JSON formaat):
{{
    "problem": "De opgave zelf (duidelijk en volledig)",
    "concept": "Het onderliggende concept dat wordt getest",
    "hints": [
        "Hint 1: Welke formule/methode zou je kunnen gebruiken?",
        "Hint 2: Wat zijn de eerste stappen?",
        "Hint 3: Meer gedetailleerde aanwijzing"
    ],
    "solution_approach": "Algemene aanpak zonder het exacte antwoord te geven",
    "check_method": "Hoe kan de leerling zelf checken of het antwoord klopt?",
    "surinamese_context": "Uitleg van eventuele Surinaamse elementen in de opgave"
}}

Genereer alleen de JSON, geen extra tekst."""

            # Generate using AI
            messages = [{"role": "user", "content": practice_prompt}]
            
            response_text = await self.async_chat_completion(
                messages=messages,
                temperature=0.8,  # Higher temperature for variety
                max_tokens=1000
            )
            
            if not response_text:
                return {
                    "success": False,
                    "error": "Failed to generate practice problem"
                }
            
            # Parse JSON response
            import json
            import re
            
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            try:
                problem_data = json.loads(response_text)
                
                # Add metadata
                problem_data["success"] = True
                problem_data["subject"] = subject
                problem_data["education_level"] = education_level
                problem_data["topic"] = selected_topic.get("name", "")
                problem_data["difficulty"] = difficulty
                
                return problem_data
                
            except json.JSONDecodeError:
                # Fallback: return raw response
                return {
                    "success": True,
                    "problem": response_text,
                    "subject": subject,
                    "education_level": education_level,
                    "topic": selected_topic.get("name", ""),
                    "difficulty": difficulty,
                    "hints": ["Lees de opgave zorgvuldig", "Welk concept wordt hier getest?", "Vergelijk met voorbeelden"],
                    "solution_approach": "Pas de geleerde concepten stap voor stap toe"
                }
        
        except Exception as e:
            print(f"Error generating practice problem: {e}")
            return {
                "success": False,
                "error": str(e)
            }



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

