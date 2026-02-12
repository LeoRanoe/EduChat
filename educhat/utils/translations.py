"""
Translations Module for EduChat - Dutch/English Support

Provides a comprehensive translation system with:
- Dutch (nl) and English (en) language support
- Hardcoded dictionaries for fast lookups
- Helper function t() for component use
- Organized by section for maintainability
"""

from typing import Dict, Any


# =============================================================================
# TRANSLATION DICTIONARIES
# =============================================================================

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # =========================================================================
    # COMMON / SHARED
    # =========================================================================
    "app_name": {
        "nl": "EduChat",
        "en": "EduChat",
    },
    "app_tagline": {
        "nl": "Surinaams Onderwijs AI",
        "en": "Surinamese Education AI",
    },
    "loading": {
        "nl": "Laden...",
        "en": "Loading...",
    },
    "save": {
        "nl": "Opslaan",
        "en": "Save",
    },
    "cancel": {
        "nl": "Annuleren",
        "en": "Cancel",
    },
    "close": {
        "nl": "Sluiten",
        "en": "Close",
    },
    "back": {
        "nl": "Terug",
        "en": "Back",
    },
    "next": {
        "nl": "Volgende",
        "en": "Next",
    },
    "skip": {
        "nl": "Overslaan",
        "en": "Skip",
    },
    "complete": {
        "nl": "Voltooien",
        "en": "Complete",
    },
    "submit": {
        "nl": "Verzenden",
        "en": "Submit",
    },
    "search": {
        "nl": "Zoeken",
        "en": "Search",
    },
    "settings": {
        "nl": "Instellingen",
        "en": "Settings",
    },
    "language": {
        "nl": "Taal",
        "en": "Language",
    },
    "dutch": {
        "nl": "Nederlands",
        "en": "Dutch",
    },
    "english": {
        "nl": "Engels",
        "en": "English",
    },
    
    # =========================================================================
    # NAVIGATION / NAVBAR
    # =========================================================================
    "nav_login": {
        "nl": "Inloggen",
        "en": "Login",
    },
    "nav_signup": {
        "nl": "Registreren",
        "en": "Sign Up",
    },
    "nav_logout": {
        "nl": "Uitloggen",
        "en": "Logout",
    },
    "nav_start_now": {
        "nl": "Start Nu",
        "en": "Start Now",
    },
    "nav_chat": {
        "nl": "Chat",
        "en": "Chat",
    },
    "nav_calendar": {
        "nl": "Kalender",
        "en": "Calendar",
    },
    "nav_profile": {
        "nl": "Profiel",
        "en": "Profile",
    },
    "dark_mode": {
        "nl": "Donkere modus",
        "en": "Dark mode",
    },
    "light_mode": {
        "nl": "Lichte modus",
        "en": "Light mode",
    },
    
    # =========================================================================
    # LANDING PAGE
    # =========================================================================
    "landing_hero_title": {
        "nl": "Jouw AI-assistent voor",
        "en": "Your AI assistant for",
    },
    "landing_hero_title_accent": {
        "nl": "Surinaams Onderwijs",
        "en": "Surinamese Education",
    },
    "landing_hero_subtitle": {
        "nl": "Krijg directe antwoorden op al je vragen over studies, inschrijvingen en onderwijsinstellingen in Suriname.",
        "en": "Get instant answers to all your questions about studies, enrollments, and educational institutions in Suriname.",
    },
    "landing_cta_start": {
        "nl": "Begin Chat",
        "en": "Start Chat",
    },
    "landing_cta_guest": {
        "nl": "Probeer als Gast",
        "en": "Try as Guest",
    },
    "landing_features_title": {
        "nl": "Waarom EduChat?",
        "en": "Why EduChat?",
    },
    "landing_features_subtitle": {
        "nl": "Alles wat je nodig hebt voor je studie in Suriname",
        "en": "Everything you need for your studies in Suriname",
    },
    
    # Feature cards
    "feature_instant_answers_title": {
        "nl": "Directe Antwoorden",
        "en": "Instant Answers",
    },
    "feature_instant_answers_desc": {
        "nl": "Krijg direct antwoord op je vragen over Surinaams onderwijs, 24/7 beschikbaar.",
        "en": "Get immediate answers to your questions about Surinamese education, available 24/7.",
    },
    "feature_personalized_title": {
        "nl": "Gepersonaliseerd",
        "en": "Personalized",
    },
    "feature_personalized_desc": {
        "nl": "Advies op maat gebaseerd op jouw onderwijsniveau en interesses.",
        "en": "Tailored advice based on your education level and interests.",
    },
    "feature_calendar_title": {
        "nl": "Slimme Kalender",
        "en": "Smart Calendar",
    },
    "feature_calendar_desc": {
        "nl": "Mis nooit meer een deadline met automatische herinneringen.",
        "en": "Never miss a deadline with automatic reminders.",
    },
    "feature_institutions_title": {
        "nl": "Alle Instellingen",
        "en": "All Institutions",
    },
    "feature_institutions_desc": {
        "nl": "Informatie over universiteiten, MINOV, en meer.",
        "en": "Information about universities, MINOV, and more.",
    },
    "feature_deadlines_title": {
        "nl": "Deadlines & Data",
        "en": "Deadlines & Dates",
    },
    "feature_deadlines_desc": {
        "nl": "Blijf op de hoogte van toelating deadlines en examens.",
        "en": "Stay informed about admission deadlines and exams.",
    },
    "feature_study_advice_title": {
        "nl": "Studieadvies",
        "en": "Study Advice",
    },
    "feature_study_advice_desc": {
        "nl": "Hulp bij het kiezen van de juiste studie voor jou.",
        "en": "Help choosing the right study for you.",
    },
    "feature_free_title": {
        "nl": "100% Gratis",
        "en": "100% Free",
    },
    "feature_free_desc": {
        "nl": "Toegankelijk voor alle Surinaamse studenten.",
        "en": "Accessible to all Surinamese students.",
    },
    "feature_secure_title": {
        "nl": "Veilig & Privé",
        "en": "Safe & Private",
    },
    "feature_secure_desc": {
        "nl": "Je gegevens zijn veilig en worden nooit gedeeld.",
        "en": "Your data is safe and never shared.",
    },
    
    # =========================================================================
    # LANDING PAGE - ADDITIONAL KEYS
    # =========================================================================
    "landing_subtitle": {
        "nl": "Surinaams Onderwijs AI",
        "en": "Surinamese Education AI",
    },
    "login": {
        "nl": "Inloggen",
        "en": "Login",
    },
    "start_now": {
        "nl": "Start Nu",
        "en": "Start Now",
    },
    "ai_powered_badge": {
        "nl": "AI-Powered Studiegids",
        "en": "AI-Powered Study Guide",
    },
    "welcome_to": {
        "nl": "Welkom bij ",
        "en": "Welcome to ",
    },
    "hero_description_1": {
        "nl": "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
        "en": "EduChat helps you easily find information about the Ministry of Education (MINOV) and everything related to education in Suriname.",
    },
    "hero_description_2": {
        "nl": "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
        "en": "Whether you want to compare study options, search for school info, or are just curious – it's here to explain it simply, your way.",
    },
    "start_chat": {
        "nl": "Begin Chat",
        "en": "Start Chat",
    },
    "popular_questions": {
        "nl": "Populaire vragen:",
        "en": "Popular Questions:",
    },
    "step_by_step_guide": {
        "nl": "Of start met een stap-voor-stap gids:",
        "en": "Or start with a step-by-step guide:",
    },
    "enrollment_process_title": {
        "nl": "Inschrijvingsproces",
        "en": "Enrollment Process",
    },
    "enrollment_process_desc": {
        "nl": "Leer stap voor stap hoe je je inschrijft voor een opleiding",
        "en": "Learn step by step how to enroll in a program",
    },
    "enrollment_process_prompt": {
        "nl": "Hoe schrijf ik me in voor een opleiding? Kun je me stap voor stap door het proces leiden?",
        "en": "How do I enroll in a program? Can you guide me through the process step by step?",
    },
    "required_documents_title": {
        "nl": "Benodigde documenten",
        "en": "Required Documents",
    },
    "required_documents_desc": {
        "nl": "Ontdek welke documenten je nodig hebt voor je inschrijving",
        "en": "Discover which documents you need for your enrollment",
    },
    "required_documents_prompt": {
        "nl": "Welke documenten heb ik nodig om me in te schrijven? Kun je een volledige lijst geven?",
        "en": "Which documents do I need to enroll? Can you provide a complete list?",
    },
    "admission_requirements_title": {
        "nl": "Toelatingseisen",
        "en": "Admission Requirements",
    },
    "admission_requirements_desc": {
        "nl": "Bekijk de vereisten en voorwaarden voor toelating",
        "en": "View the requirements and conditions for admission",
    },
    "admission_requirements_prompt": {
        "nl": "Wat zijn de toelatingseisen voor studies in Suriname? Welke voorwaarden moet ik vervullen?",
        "en": "What are the admission requirements for studies in Suriname? Which conditions must I fulfill?",
    },
    "ai_study_guide": {
        "nl": "Jouw AI Studiegids",
        "en": "Your AI Study Guide",
    },
    "welcome_to": {
        "nl": "Welkom bij",
        "en": "Welcome to",
    },
    "welcome_description_1": {
        "nl": "EduChat helpt je makkelijk informatie te vinden over het Ministerie van Onderwijs (MINOV) en alles wat met onderwijs in Suriname te maken heeft.",
        "en": "EduChat helps you easily find information about the Ministry of Education (MINOV) and everything related to education in Suriname.",
    },
    "welcome_description_2": {
        "nl": "Of je nu studiekeuzes wilt vergelijken, schoolinfo zoekt, of gewoon nieuwsgierig bent – het is er om het jou simpel uit te leggen, op jouw manier.",
        "en": "Whether you want to compare study choices, find school information, or are just curious – it's here to explain it simply, your way.",
    },
    "chat_placeholder": {
        "nl": "Vraag mij van alles over onderwijs...",
        "en": "Ask me anything about education...",
    },
    "type_message": {
        "nl": "Typ je bericht",
        "en": "Type your message",
    },
    "send_message": {
        "nl": "Verstuur bericht",
        "en": "Send message",
    },
    "try_as_guest": {
        "nl": "Probeer als Gast",
        "en": "Try as Guest",
    },
    "free_to_use": {
        "nl": "Gratis te gebruiken",
        "en": "Free to use",
    },
    "available_24_7": {
        "nl": "24/7 beschikbaar",
        "en": "Available 24/7",
    },
    "focus_suriname": {
        "nl": "Focus op Suriname",
        "en": "Focus on Suriname",
    },
    "chat_preview_question": {
        "nl": "Welke opleidingen biedt MINOV aan?",
        "en": "What programs does MINOV offer?",
    },
    "chat_preview_answer": {
        "nl": "MINOV biedt diverse technische opleidingen...",
        "en": "MINOV offers various technical programs...",
    },
    "features_title": {
        "nl": "Alles wat je Nodig Hebt voor je Studiekeuze",
        "en": "Everything You Need for Your Study Choice",
    },
    "features_subtitle": {
        "nl": "Complete ondersteuning voor het Surinaamse onderwijssysteem",
        "en": "Complete support for the Surinamese education system",
    },
    "feature_find_programs": {
        "nl": "Opleidingen Vinden",
        "en": "Find Programs",
    },
    "feature_find_programs_desc": {
        "nl": "Ontdek alle beschikbare opleidingen bij MINOV, universiteiten en andere instellingen in Suriname",
        "en": "Discover all available programs at MINOV, universities and other institutions in Suriname",
    },
    "feature_requirements": {
        "nl": "Toelatingseisen",
        "en": "Admission Requirements",
    },
    "feature_requirements_desc": {
        "nl": "Krijg duidelijke informatie over toelatingseisen, benodigde documenten en inschrijvingsprocedures",
        "en": "Get clear information about admission requirements, required documents and enrollment procedures",
    },
    "feature_deadlines": {
        "nl": "Deadlines & Data",
        "en": "Deadlines & Dates",
    },
    "feature_deadlines_desc": {
        "nl": "Blijf op de hoogte van belangrijke deadlines voor inschrijvingen en aanmeldingen",
        "en": "Stay informed about important deadlines for enrollments and applications",
    },
    "feature_direct_answers": {
        "nl": "Directe Antwoorden",
        "en": "Direct Answers",
    },
    "feature_direct_answers_desc": {
        "nl": "Stel je vraag in het Nederlands en krijg meteen een helder antwoord van onze AI",
        "en": "Ask your question and get an immediate clear answer from our AI",
    },
    "feature_guidance": {
        "nl": "Studiekeuzebegeleiding",
        "en": "Study Choice Guidance",
    },
    "feature_guidance_desc": {
        "nl": "Persoonlijk advies om de opleiding te vinden die bij jou past",
        "en": "Personal advice to find the program that suits you",
    },
    "feature_privacy": {
        "nl": "Veilig & Privé",
        "en": "Safe & Private",
    },
    "feature_privacy_desc": {
        "nl": "Jouw gegevens zijn veilig en al je gesprekken blijven privé",
        "en": "Your data is safe and all your conversations remain private",
    },
    "superfast_badge": {
        "nl": "Supersnel en Makkelijk",
        "en": "Super Fast and Easy",
    },
    "how_it_works": {
        "nl": "Zo Werkt EduChat",
        "en": "How EduChat Works",
    },
    "how_it_works_subtitle": {
        "nl": "In drie eenvoudige stappen naar de juiste studiekeuze",
        "en": "Three simple steps to the right study choice",
    },
    "step1_title": {
        "nl": "Stel je Vraag",
        "en": "Ask Your Question",
    },
    "step1_desc": {
        "nl": "Typ je vraag over opleidingen, toelatingseisen, inschrijvingen of studiefinanciering",
        "en": "Type your question about programs, admission requirements, enrollments or student financing",
    },
    "step2_title": {
        "nl": "Krijg Direct Antwoord",
        "en": "Get Instant Answers",
    },
    "step2_desc": {
        "nl": "Ontvang binnen seconden een helder en compleet antwoord met alle benodigde informatie",
        "en": "Receive a clear and complete answer within seconds with all the information you need",
    },
    "step3_title": {
        "nl": "Maak je Keuze",
        "en": "Make Your Choice",
    },
    "step3_desc": {
        "nl": "Gebruik de informatie om een weloverwogen studiekeuze te maken en je toekomst vorm te geven",
        "en": "Use the information to make an informed study choice and shape your future",
    },
    "cta_title": {
        "nl": "Klaar om te Beginnen?",
        "en": "Ready to Start?",
    },
    "cta_subtitle": {
        "nl": "Start nu met EduChat en krijg alle antwoorden die je nodig hebt voor je studiekeuze in Suriname",
        "en": "Start now with EduChat and get all the answers you need for your study choice in Suriname",
    },
    "start_free": {
        "nl": "Begin Nu Gratis",
        "en": "Start Free Now",
    },
    "stat_students": {
        "nl": "Tevreden Studenten",
        "en": "Happy Students",
    },
    "stat_response_time": {
        "nl": "Gemiddelde Reactietijd",
        "en": "Average Response Time",
    },
    "stat_available": {
        "nl": "Altijd Beschikbaar",
        "en": "Always Available",
    },
    "trust_badge": {
        "nl": "100% Gratis • Geen Registratie Vereist • Direct Beginnen",
        "en": "100% Free • No Registration Required • Start Immediately",
    },
    
    # Institutions section
    "landing_institutions_title": {
        "nl": "Ondersteunde Instellingen",
        "en": "Supported Institutions",
    },
    "landing_institutions_subtitle": {
        "nl": "Informatie over alle Surinaamse onderwijsinstellingen",
        "en": "Information about all Surinamese educational institutions",
    },
    
    # Footer
    "footer_about": {
        "nl": "Over EduChat",
        "en": "About EduChat",
    },
    "footer_privacy": {
        "nl": "Privacy",
        "en": "Privacy",
    },
    "footer_terms": {
        "nl": "Voorwaarden",
        "en": "Terms",
    },
    "footer_contact": {
        "nl": "Contact",
        "en": "Contact",
    },
    "footer_copyright": {
        "nl": "© 2026 EduChat. Gemaakt voor Surinaamse studenten.",
        "en": "© 2026 EduChat. Made for Surinamese students.",
    },
    
    # =========================================================================
    # AUTH MODAL
    # =========================================================================
    "auth_welcome": {
        "nl": "Welkom bij EduChat",
        "en": "Welcome to EduChat",
    },
    "auth_welcome_back": {
        "nl": "Welkom terug",
        "en": "Welcome back",
    },
    "auth_subtitle": {
        "nl": "Jouw AI-assistent voor Surinaams onderwijs",
        "en": "Your AI assistant for Surinamese education",
    },
    "benefit_direct_answers": {
        "nl": "Directe antwoorden op je vragen",
        "en": "Instant answers to your questions",
    },
    "benefit_study_material": {
        "nl": "Studiemateriaal op maat",
        "en": "Tailored study material",
    },
    "benefit_24_7": {
        "nl": "24/7 beschikbaar",
        "en": "Available 24/7",
    },
    "benefit_free": {
        "nl": "Gratis te gebruiken",
        "en": "Free to use",
    },
    "auth_login_title": {
        "nl": "Log in op je account",
        "en": "Log in to your account",
    },
    "auth_signup_title": {
        "nl": "Maak een account aan",
        "en": "Create an account",
    },
    "auth_login_subtitle": {
        "nl": "Vul je gegevens in om verder te gaan",
        "en": "Enter your details to continue",
    },
    "auth_signup_subtitle": {
        "nl": "Start je reis naar studiesucces",
        "en": "Start your journey to study success",
    },
    
    # Form fields
    "auth_email": {
        "nl": "E-mailadres",
        "en": "Email address",
    },
    "auth_email_placeholder": {
        "nl": "naam@voorbeeld.com",
        "en": "name@example.com",
    },
    "auth_password": {
        "nl": "Wachtwoord",
        "en": "Password",
    },
    "auth_password_placeholder": {
        "nl": "Voer je wachtwoord in",
        "en": "Enter your password",
    },
    "auth_confirm_password": {
        "nl": "Bevestig wachtwoord",
        "en": "Confirm password",
    },
    "auth_confirm_password_placeholder": {
        "nl": "Herhaal je wachtwoord",
        "en": "Repeat your password",
    },
    "auth_firstname": {
        "nl": "Voornaam",
        "en": "First name",
    },
    "auth_firstname_placeholder": {
        "nl": "Je voornaam",
        "en": "Your first name",
    },
    "auth_lastname": {
        "nl": "Achternaam",
        "en": "Last name",
    },
    "auth_lastname_placeholder": {
        "nl": "Je achternaam",
        "en": "Your last name",
    },
    "auth_remember_me": {
        "nl": "Onthoud mij",
        "en": "Remember me",
    },
    "auth_forgot_password": {
        "nl": "Wachtwoord vergeten?",
        "en": "Forgot password?",
    },
    
    # Buttons
    "auth_login_btn": {
        "nl": "Inloggen",
        "en": "Log in",
    },
    "auth_signup_btn": {
        "nl": "Account aanmaken",
        "en": "Create account",
    },
    "auth_google_btn": {
        "nl": "Doorgaan met Google",
        "en": "Continue with Google",
    },
    "auth_guest_btn": {
        "nl": "Doorgaan als gast",
        "en": "Continue as guest",
    },
    
    # Switching views
    "auth_no_account": {
        "nl": "Nog geen account?",
        "en": "Don't have an account?",
    },
    "auth_has_account": {
        "nl": "Heb je al een account?",
        "en": "Already have an account?",
    },
    "auth_signup_link": {
        "nl": "Registreren",
        "en": "Sign up",
    },
    "auth_login_link": {
        "nl": "Inloggen",
        "en": "Log in",
    },
    
    # Dividers
    "auth_or": {
        "nl": "of",
        "en": "or",
    },
    
    # Benefits list
    "auth_benefit_1": {
        "nl": "Gepersonaliseerd studieadvies",
        "en": "Personalized study advice",
    },
    "auth_benefit_2": {
        "nl": "Bewaar je chatgeschiedenis",
        "en": "Save your chat history",
    },
    "auth_benefit_3": {
        "nl": "Deadline herinneringen",
        "en": "Deadline reminders",
    },
    "auth_benefit_4": {
        "nl": "Google Calendar sync",
        "en": "Google Calendar sync",
    },
    
    # Validation errors
    "error_email_required": {
        "nl": "E-mailadres is verplicht",
        "en": "Email address is required",
    },
    "error_email_invalid": {
        "nl": "Voer een geldig e-mailadres in",
        "en": "Enter a valid email address",
    },
    "error_password_required": {
        "nl": "Wachtwoord is verplicht",
        "en": "Password is required",
    },
    "error_password_short": {
        "nl": "Wachtwoord moet minimaal 6 tekens zijn",
        "en": "Password must be at least 6 characters",
    },
    "error_passwords_mismatch": {
        "nl": "Wachtwoorden komen niet overeen",
        "en": "Passwords do not match",
    },
    "error_firstname_required": {
        "nl": "Voornaam is verplicht",
        "en": "First name is required",
    },
    "error_login_failed": {
        "nl": "Inloggen mislukt. Controleer je gegevens.",
        "en": "Login failed. Please check your credentials.",
    },
    "error_signup_failed": {
        "nl": "Registratie mislukt. Probeer het opnieuw.",
        "en": "Registration failed. Please try again.",
    },
    
    # Success messages
    "success_login": {
        "nl": "Succesvol ingelogd!",
        "en": "Successfully logged in!",
    },
    "success_signup": {
        "nl": "Account aangemaakt! Controleer je e-mail.",
        "en": "Account created! Check your email.",
    },
    "success_logout": {
        "nl": "Succesvol uitgelogd",
        "en": "Successfully logged out",
    },
    
    # =========================================================================
    # ONBOARDING
    # =========================================================================
    "onboarding_title": {
        "nl": "Laten we je leren kennen",
        "en": "Let's get to know you",
    },
    "onboarding_subtitle": {
        "nl": "Een paar vragen om je ervaring te personaliseren",
        "en": "A few questions to personalize your experience",
    },
    
    # Question 0: Education Level
    "onboarding_q0_title": {
        "nl": "Welke opleiding volg je momenteel?",
        "en": "What education are you currently pursuing?",
    },
    "onboarding_q0_desc": {
        "nl": "Dit helpt ons om informatie op jouw niveau aan te passen.",
        "en": "This helps us adjust information to your level.",
    },
    
    # Question 1: Age
    "onboarding_q1_title": {
        "nl": "Wat is jouw leeftijd?",
        "en": "What is your age?",
    },
    "onboarding_q1_desc": {
        "nl": "We passen onze communicatie aan op jouw leeftijdsgroep.",
        "en": "We adjust our communication to your age group.",
    },
    
    # Question 2: District
    "onboarding_q2_title": {
        "nl": "In welk district woon je?",
        "en": "Which district do you live in?",
    },
    "onboarding_q2_desc": {
        "nl": "We kunnen je informatie geven over scholen in jouw regio.",
        "en": "We can give you information about schools in your area.",
    },
    
    # Question 3: Favorite Subjects
    "onboarding_q3_title": {
        "nl": "Wat zijn je favoriete vakken?",
        "en": "What are your favorite subjects?",
    },
    "onboarding_q3_desc": {
        "nl": "Selecteer de vakken waar je het meest van houdt (meerdere mogelijk).",
        "en": "Select the subjects you enjoy most (multiple allowed).",
    },
    
    # Question 4: Future Plans
    "onboarding_q4_title": {
        "nl": "Heb je plannen om verder te studeren?",
        "en": "Do you plan to continue studying?",
    },
    "onboarding_q4_desc": {
        "nl": "We kunnen je helpen met studiekeuzes en toekomstplanning.",
        "en": "We can help you with study choices and future planning.",
    },
    
    # Question 5: Help Areas
    "onboarding_q5_title": {
        "nl": "Waarmee kan EduChat je helpen?",
        "en": "How can EduChat help you?",
    },
    "onboarding_q5_desc": {
        "nl": "Selecteer alles wat van toepassing is (meerdere mogelijk).",
        "en": "Select everything that applies (multiple allowed).",
    },
    
    # Question 6: Communication Style
    "onboarding_q6_title": {
        "nl": "Hoe mag EduChat met je communiceren?",
        "en": "How should EduChat communicate with you?",
    },
    "onboarding_q6_desc": {
        "nl": "Kies de communicatiestijl die het beste bij je past.",
        "en": "Choose the communication style that suits you best.",
    },
    
    # Question 7: Study Directions
    "onboarding_q7_title": {
        "nl": "Welke studierichtingen interesseren je?",
        "en": "Which study directions interest you?",
    },
    "onboarding_q7_desc": {
        "nl": "Selecteer de gebieden waar je meer over wilt weten (meerdere mogelijk).",
        "en": "Select the areas you want to know more about (multiple allowed).",
    },
    
    # Legacy keys (for compatibility)
    # Step 1: Education Level
    "onboarding_step1_title": {
        "nl": "Wat is je onderwijsniveau?",
        "en": "What is your education level?",
    },
    "onboarding_step1_subtitle": {
        "nl": "Dit helpt ons relevante informatie te tonen",
        "en": "This helps us show relevant information",
    },
    
    # Step 2: Study Directions
    "onboarding_step2_title": {
        "nl": "Welke studierichtingen interesseren je?",
        "en": "Which study directions interest you?",
    },
    "onboarding_step2_subtitle": {
        "nl": "Selecteer één of meer opties",
        "en": "Select one or more options",
    },
    
    # Step 3: Age
    "onboarding_step3_title": {
        "nl": "Wat is je leeftijdsgroep?",
        "en": "What is your age group?",
    },
    "onboarding_step3_subtitle": {
        "nl": "Dit helpt ons de toon aan te passen",
        "en": "This helps us adjust the tone",
    },
    
    # Step 4: District
    "onboarding_step4_title": {
        "nl": "In welk district woon je?",
        "en": "Which district do you live in?",
    },
    "onboarding_step4_subtitle": {
        "nl": "Voor relevante lokale informatie",
        "en": "For relevant local information",
    },
    
    # Step 5: Subjects
    "onboarding_step5_title": {
        "nl": "Wat zijn je favoriete vakken?",
        "en": "What are your favorite subjects?",
    },
    "onboarding_step5_subtitle": {
        "nl": "Selecteer de vakken waar je van houdt",
        "en": "Select the subjects you enjoy",
    },
    
    # Step 6: Future Plans
    "onboarding_step6_title": {
        "nl": "Wat zijn je toekomstplannen?",
        "en": "What are your future plans?",
    },
    "onboarding_step6_subtitle": {
        "nl": "Na je huidige opleiding",
        "en": "After your current education",
    },
    
    # Step 7: Goals
    "onboarding_step7_title": {
        "nl": "Waar wil je mee geholpen worden?",
        "en": "What would you like help with?",
    },
    "onboarding_step7_subtitle": {
        "nl": "Selecteer je belangrijkste doelen",
        "en": "Select your main goals",
    },
    
    # Step 8: Formality
    "onboarding_step8_title": {
        "nl": "Hoe formeel wil je dat ik antwoord?",
        "en": "How formal would you like my responses?",
    },
    "onboarding_step8_subtitle": {
        "nl": "Kies je voorkeursaanspreekstijl",
        "en": "Choose your preferred communication style",
    },
    
    # Completion
    "onboarding_complete_title": {
        "nl": "Je bent klaar!",
        "en": "You're all set!",
    },
    "onboarding_complete_subtitle": {
        "nl": "Je ervaring is gepersonaliseerd",
        "en": "Your experience is personalized",
    },
    "onboarding_start_chatting": {
        "nl": "Start met Chatten",
        "en": "Start Chatting",
    },
    
    # =========================================================================
    # CHAT INTERFACE
    # =========================================================================
    "chat_welcome_title": {
        "nl": "Hallo! Ik ben EduChat",
        "en": "Hello! I'm EduChat",
    },
    "chat_welcome_subtitle": {
        "nl": "Jouw AI-assistent voor Surinaams onderwijs. Hoe kan ik je vandaag helpen?",
        "en": "Your AI assistant for Surinamese education. How can I help you today?",
    },
    "chat_input_placeholder": {
        "nl": "Stel je vraag over Surinaams onderwijs...",
        "en": "Ask your question about Surinamese education...",
    },
    "chat_send": {
        "nl": "Verstuur",
        "en": "Send",
    },
    "chat_new_conversation": {
        "nl": "Nieuw gesprek",
        "en": "New conversation",
    },
    "chat_conversations": {
        "nl": "Gesprekken",
        "en": "Conversations",
    },
    "chat_no_conversations": {
        "nl": "Nog geen gesprekken",
        "en": "No conversations yet",
    },
    "chat_today": {
        "nl": "Vandaag",
        "en": "Today",
    },
    "chat_yesterday": {
        "nl": "Gisteren",
        "en": "Yesterday",
    },
    "chat_this_week": {
        "nl": "Deze week",
        "en": "This week",
    },
    "chat_this_month": {
        "nl": "Deze maand",
        "en": "This month",
    },
    "chat_older": {
        "nl": "Ouder",
        "en": "Older",
    },
    
    # Quick actions
    "chat_quick_enrollment": {
        "nl": "Hoe schrijf ik me in?",
        "en": "How do I enroll?",
    },
    "chat_quick_deadlines": {
        "nl": "Wat zijn de deadlines?",
        "en": "What are the deadlines?",
    },
    "chat_quick_requirements": {
        "nl": "Toelatingseisen",
        "en": "Admission requirements",
    },
    "chat_quick_costs": {
        "nl": "Studiekosten",
        "en": "Study costs",
    },
    
    # Message actions
    "chat_copy": {
        "nl": "Kopiëren",
        "en": "Copy",
    },
    "chat_copied": {
        "nl": "Gekopieerd!",
        "en": "Copied!",
    },
    "chat_regenerate": {
        "nl": "Opnieuw genereren",
        "en": "Regenerate",
    },
    "chat_like": {
        "nl": "Leuk",
        "en": "Like",
    },
    "chat_dislike": {
        "nl": "Niet leuk",
        "en": "Dislike",
    },
    
    # =========================================================================
    # GUEST BANNER
    # =========================================================================
    "guest_banner_text": {
        "nl": "Je gebruikt EduChat als gast. Maak een account aan om je gesprekken te bewaren.",
        "en": "You're using EduChat as a guest. Create an account to save your conversations.",
    },
    "guest_banner_cta": {
        "nl": "Account aanmaken",
        "en": "Create account",
    },
    
    # =========================================================================
    # CALENDAR
    # =========================================================================
    "calendar_title": {
        "nl": "Kalender",
        "en": "Calendar",
    },
    "calendar_sync": {
        "nl": "Synchroniseren",
        "en": "Sync",
    },
    "calendar_syncing": {
        "nl": "Synchroniseren...",
        "en": "Syncing...",
    },
    "calendar_last_sync": {
        "nl": "Laatste sync",
        "en": "Last sync",
    },
    "calendar_no_events": {
        "nl": "Geen evenementen",
        "en": "No events",
    },
    "calendar_add_event": {
        "nl": "Evenement toevoegen",
        "en": "Add event",
    },
    
    # Days of week
    "calendar_mon": {"nl": "Ma", "en": "Mon"},
    "calendar_tue": {"nl": "Di", "en": "Tue"},
    "calendar_wed": {"nl": "Wo", "en": "Wed"},
    "calendar_thu": {"nl": "Do", "en": "Thu"},
    "calendar_fri": {"nl": "Vr", "en": "Fri"},
    "calendar_sat": {"nl": "Za", "en": "Sat"},
    "calendar_sun": {"nl": "Zo", "en": "Sun"},
    
    # Months
    "month_january": {"nl": "Januari", "en": "January"},
    "month_february": {"nl": "Februari", "en": "February"},
    "month_march": {"nl": "Maart", "en": "March"},
    "month_april": {"nl": "April", "en": "April"},
    "month_may": {"nl": "Mei", "en": "May"},
    "month_june": {"nl": "Juni", "en": "June"},
    "month_july": {"nl": "Juli", "en": "July"},
    "month_august": {"nl": "Augustus", "en": "August"},
    "month_september": {"nl": "September", "en": "September"},
    "month_october": {"nl": "Oktober", "en": "October"},
    "month_november": {"nl": "November", "en": "November"},
    "month_december": {"nl": "December", "en": "December"},
    
    # =========================================================================
    # REMINDERS
    # =========================================================================
    "reminders_title": {
        "nl": "Herinneringen",
        "en": "Reminders",
    },
    "reminders_add": {
        "nl": "Herinnering toevoegen",
        "en": "Add reminder",
    },
    "reminders_no_reminders": {
        "nl": "Geen herinneringen",
        "en": "No reminders",
    },
    "reminders_delete": {
        "nl": "Verwijderen",
        "en": "Delete",
    },
    
    # =========================================================================
    # SIDEBAR 
    # =========================================================================
    "new_conversation": {
        "nl": "Nieuw gesprek",
        "en": "New conversation",
    },
    "conversations": {
        "nl": "Gesprekken",
        "en": "Conversations",
    },
    "no_conversations_yet": {
        "nl": "Nog geen gesprekken",
        "en": "No conversations yet",
    },
    "start_first_conversation": {
        "nl": "Start je eerste gesprek hierboven",
        "en": "Start your first conversation above",
    },
    "preferences": {
        "nl": "Voorkeuren",
        "en": "Preferences",
    },
    "start_onboarding": {
        "nl": "Start Onboarding",
        "en": "Start Onboarding",
    },
    "guest": {
        "nl": "GAST",
        "en": "GUEST",
    },
    "reminders": {
        "nl": "Reminders",
        "en": "Reminders",
    },
    "events": {
        "nl": "Events",
        "en": "Events",
    },
    "dark": {
        "nl": "Donker",
        "en": "Dark",
    },
    "light": {
        "nl": "Licht",
        "en": "Light",
    },
    "switch_to_dark_mode": {
        "nl": "Schakel naar donkere modus",
        "en": "Switch to dark mode",
    },
    "switch_to_light_mode": {
        "nl": "Schakel naar lichte modus",
        "en": "Switch to light mode",
    },
    "dark_mode_desc": {
        "nl": "Donkere modus - vermindert vermoeidheid van de ogen",
        "en": "Dark mode - reduces eye strain",
    },
    "light_mode_desc": {
        "nl": "Lichte modus - vermindert vermoeidheid van de ogen",  
        "en": "Light mode - reduces eye strain",
    },
    "sync_calendar": {
        "nl": "Sync Kalender",
        "en": "Sync Calendar",
    },
    "logout": {
        "nl": "Uitloggen",
        "en": "Logout",
    },
    
    # =========================================================================
    # SETTINGS
    # =========================================================================
    "settings_title": {
        "nl": "Instellingen",
        "en": "Settings",
    },
    "settings_appearance": {
        "nl": "Uiterlijk",
        "en": "Appearance",
    },
    "settings_theme": {
        "nl": "Thema",
        "en": "Theme",
    },
    "settings_language": {
        "nl": "Taal",
        "en": "Language",
    },
    "settings_notifications": {
        "nl": "Meldingen",
        "en": "Notifications",
    },
    "settings_account": {
        "nl": "Account",
        "en": "Account",
    },
    "settings_delete_account": {
        "nl": "Account verwijderen",
        "en": "Delete account",
    },
    "settings_export_data": {
        "nl": "Gegevens exporteren",
        "en": "Export data",
    },
    
    # =========================================================================
    # TOASTS / NOTIFICATIONS
    # =========================================================================
    "toast_success": {
        "nl": "Gelukt",
        "en": "Success",
    },
    "toast_error": {
        "nl": "Fout",
        "en": "Error",
    },
    "toast_warning": {
        "nl": "Waarschuwing",
        "en": "Warning",
    },
    "toast_info": {
        "nl": "Info",
        "en": "Info",
    },
    "toast_message_copied": {
        "nl": "Bericht gekopieerd naar klembord",
        "en": "Message copied to clipboard",
    },
    "toast_settings_saved": {
        "nl": "Instellingen opgeslagen",
        "en": "Settings saved",
    },
    "toast_reminder_added": {
        "nl": "Herinnering toegevoegd",
        "en": "Reminder added",
    },
    "toast_conversation_deleted": {
        "nl": "Gesprek verwijderd",
        "en": "Conversation deleted",
    },
    
    # =========================================================================
    # AI SERVICE MESSAGES
    # =========================================================================
    "ai_error_generic": {
        "nl": "Er ging iets mis bij het verwerken van je vraag. Probeer het later nog eens!",
        "en": "Something went wrong while processing your question. Please try again later!",
    },
    "ai_error_quota": {
        "nl": "De AI service heeft zijn gebruikslimiet bereikt. Probeer het over een paar minuten opnieuw.",
        "en": "The AI service has reached its usage limit. Please try again in a few minutes.",
    },
    "ai_error_api_key": {
        "nl": "Er is een probleem met de AI API-sleutel. Neem contact op met de beheerder.",
        "en": "There is an issue with the AI API key. Please contact the administrator.",
    },
    "ai_invalid_response": {
        "nl": "Sorry, ik kon geen goed antwoord genereren. Kun je je vraag anders formuleren?",
        "en": "Sorry, I couldn't generate a good response. Could you rephrase your question?",
    },
    "ai_off_topic": {
        "nl": "Ik ben gespecialiseerd in Surinaams onderwijs. Heb je vragen over studies, inschrijvingen, of onderwijsinstellingen?",
        "en": "I specialize in Surinamese education. Do you have questions about studies, enrollments, or educational institutions?",
    },
    "ai_no_info": {
        "nl": "Ik heb geen specifieke informatie hierover. Neem contact op met de instelling of raadpleeg hun website.",
        "en": "I don't have specific information about this. Please contact the institution or check their website.",
    },
    
    # =========================================================================
    # EDUCATION OPTIONS (Keep in Dutch - cultural context)
    # Labels are translated, but values stay in Dutch for cultural accuracy
    # =========================================================================
    "edu_level_label": {
        "nl": "Onderwijsniveau",
        "en": "Education Level",
    },
    "study_direction_label": {
        "nl": "Studierichting",
        "en": "Study Direction",
    },
    "district_label": {
        "nl": "District",
        "en": "District",
    },
    "age_group_label": {
        "nl": "Leeftijdsgroep",
        "en": "Age Group",
    },
    
    # =========================================================================
    # PERSONALIZATION INDICATOR
    # =========================================================================
    "personalized": {
        "nl": "Gepersonaliseerd",
        "en": "Personalized",
    },
    "personalization_info": {
        "nl": "EduChat past antwoorden aan op basis van:",
        "en": "EduChat adapts answers based on:",
    },
    "personalization_education_level": {
        "nl": "Je onderwijsniveau",
        "en": "Your education level",
    },
    "personalization_subjects": {
        "nl": "Je favoriete vakken",
        "en": "Your favorite subjects",
    },
    "personalization_interests": {
        "nl": "Je interessegebieden",
        "en": "Your areas of interest",
    },
    "personalization_style": {
        "nl": "Je communicatiestijl",
        "en": "Your communication style",
    },
    "personalization_preferences": {
        "nl": "Je voorkeuren",
        "en": "Your preferences",
    },
}


# =============================================================================
# EDUCATION OPTIONS - Keep Dutch terms but translate descriptions
# =============================================================================

EDUCATION_LEVELS_TRANSLATIONS = {
    "nl": [
        {"value": "glo", "label": "GLO - Gewoon Lager Onderwijs", "emoji": "📚"},
        {"value": "mulo", "label": "MULO - Meer Uitgebreid Lager Onderwijs", "emoji": "📖"},
        {"value": "vos", "label": "VOS - Voortgezet Onderwijs op Secundair niveau", "emoji": "🎒"},
        {"value": "havo", "label": "HAVO - Hoger Algemeen Voortgezet Onderwijs", "emoji": "📝"},
        {"value": "vwo", "label": "VWO - Voorbereidend Wetenschappelijk Onderwijs", "emoji": "🔬"},
        {"value": "mbo", "label": "MBO - Middelbaar Beroepsonderwijs", "emoji": "🛠️"},
        {"value": "hbo", "label": "HBO - Hoger Beroepsonderwijs", "emoji": "🎓"},
        {"value": "wo", "label": "WO - Wetenschappelijk Onderwijs", "emoji": "🏛️"},
    ],
    "en": [
        {"value": "glo", "label": "GLO - Primary Education", "emoji": "📚"},
        {"value": "mulo", "label": "MULO - Extended Primary Education", "emoji": "📖"},
        {"value": "vos", "label": "VOS - Secondary Vocational Education", "emoji": "🎒"},
        {"value": "havo", "label": "HAVO - Higher General Secondary", "emoji": "📝"},
        {"value": "vwo", "label": "VWO - Pre-University Education", "emoji": "🔬"},
        {"value": "mbo", "label": "MBO - Vocational Training", "emoji": "🛠️"},
        {"value": "hbo", "label": "HBO - Professional Higher Education", "emoji": "🎓"},
        {"value": "wo", "label": "WO - University Education", "emoji": "🏛️"},
    ],
}


STUDY_DIRECTIONS_TRANSLATIONS = {
    "nl": [
        {"value": "tech", "label": "Techniek & IT", "emoji": "💻"},
        {"value": "health", "label": "Gezondheid & Zorg", "emoji": "🏥"},
        {"value": "economics", "label": "Economie & Business", "emoji": "📊"},
        {"value": "law", "label": "Recht & Bestuur", "emoji": "⚖️"},
        {"value": "education", "label": "Onderwijs & Pedagogiek", "emoji": "👨‍🏫"},
        {"value": "nature", "label": "Natuur & Milieu", "emoji": "🌿"},
        {"value": "arts", "label": "Kunst & Cultuur", "emoji": "🎨"},
        {"value": "social", "label": "Sociale Wetenschappen", "emoji": "🤝"},
    ],
    "en": [
        {"value": "tech", "label": "Technology & IT", "emoji": "💻"},
        {"value": "health", "label": "Health & Care", "emoji": "🏥"},
        {"value": "economics", "label": "Economics & Business", "emoji": "📊"},
        {"value": "law", "label": "Law & Government", "emoji": "⚖️"},
        {"value": "education", "label": "Education & Pedagogy", "emoji": "👨‍🏫"},
        {"value": "nature", "label": "Nature & Environment", "emoji": "🌿"},
        {"value": "arts", "label": "Arts & Culture", "emoji": "🎨"},
        {"value": "social", "label": "Social Sciences", "emoji": "🤝"},
    ],
}


AGE_GROUPS_TRANSLATIONS = {
    "nl": [
        {"value": "under_15", "label": "Jonger dan 15", "emoji": "🧒"},
        {"value": "15_18", "label": "15-18 jaar", "emoji": "🧑"},
        {"value": "18_25", "label": "18-25 jaar", "emoji": "👨‍🎓"},
        {"value": "25_35", "label": "25-35 jaar", "emoji": "👨‍💼"},
        {"value": "over_35", "label": "35 jaar of ouder", "emoji": "🧓"},
    ],
    "en": [
        {"value": "under_15", "label": "Under 15", "emoji": "🧒"},
        {"value": "15_18", "label": "15-18 years", "emoji": "🧑"},
        {"value": "18_25", "label": "18-25 years", "emoji": "👨‍🎓"},
        {"value": "25_35", "label": "25-35 years", "emoji": "👨‍💼"},
        {"value": "over_35", "label": "35 years or older", "emoji": "🧓"},
    ],
}


# Districts stay the same - geographic names
DISTRICTS = [
    {"value": "paramaribo", "label": "Paramaribo", "emoji": "🏙️"},
    {"value": "wanica", "label": "Wanica", "emoji": "🏘️"},
    {"value": "nickerie", "label": "Nickerie", "emoji": "🌾"},
    {"value": "para", "label": "Para", "emoji": "🌴"},
    {"value": "commewijne", "label": "Commewijne", "emoji": "🌳"},
    {"value": "saramacca", "label": "Saramacca", "emoji": "🛶"},
    {"value": "marowijne", "label": "Marowijne", "emoji": "🏞️"},
    {"value": "brokopondo", "label": "Brokopondo", "emoji": "💧"},
    {"value": "sipaliwini", "label": "Sipaliwini", "emoji": "🌲"},
    {"value": "coronie", "label": "Coronie", "emoji": "🥥"},
]


SCHOOL_SUBJECTS_TRANSLATIONS = {
    "nl": [
        {"value": "math", "label": "Wiskunde", "emoji": "🔢"},
        {"value": "dutch", "label": "Nederlands", "emoji": "📝"},
        {"value": "english", "label": "Engels", "emoji": "🇬🇧"},
        {"value": "science", "label": "Natuurkunde", "emoji": "⚗️"},
        {"value": "biology", "label": "Biologie", "emoji": "🧬"},
        {"value": "chemistry", "label": "Scheikunde", "emoji": "🧪"},
        {"value": "history", "label": "Geschiedenis", "emoji": "📜"},
        {"value": "geography", "label": "Aardrijkskunde", "emoji": "🌍"},
        {"value": "economics", "label": "Economie", "emoji": "💰"},
        {"value": "accounting", "label": "Boekhouden", "emoji": "📊"},
        {"value": "art", "label": "Beeldende vorming", "emoji": "🎨"},
        {"value": "music", "label": "Muziek", "emoji": "🎵"},
        {"value": "pe", "label": "Lichamelijke opvoeding", "emoji": "⚽"},
        {"value": "ict", "label": "Informatica", "emoji": "💻"},
    ],
    "en": [
        {"value": "math", "label": "Mathematics", "emoji": "🔢"},
        {"value": "dutch", "label": "Dutch", "emoji": "📝"},
        {"value": "english", "label": "English", "emoji": "🇬🇧"},
        {"value": "science", "label": "Physics", "emoji": "⚗️"},
        {"value": "biology", "label": "Biology", "emoji": "🧬"},
        {"value": "chemistry", "label": "Chemistry", "emoji": "🧪"},
        {"value": "history", "label": "History", "emoji": "📜"},
        {"value": "geography", "label": "Geography", "emoji": "🌍"},
        {"value": "economics", "label": "Economics", "emoji": "💰"},
        {"value": "accounting", "label": "Accounting", "emoji": "📊"},
        {"value": "art", "label": "Art", "emoji": "🎨"},
        {"value": "music", "label": "Music", "emoji": "🎵"},
        {"value": "pe", "label": "Physical Education", "emoji": "⚽"},
        {"value": "ict", "label": "Computer Science", "emoji": "💻"},
    ],
}


FUTURE_PLANS_TRANSLATIONS = {
    "nl": [
        {"value": "further_study", "label": "Verder studeren", "emoji": "🎓"},
        {"value": "work", "label": "Gaan werken", "emoji": "💼"},
        {"value": "study_abroad", "label": "Studeren in het buitenland", "emoji": "✈️"},
        {"value": "own_business", "label": "Eigen bedrijf starten", "emoji": "🚀"},
        {"value": "not_sure", "label": "Nog niet zeker", "emoji": "🤔"},
    ],
    "en": [
        {"value": "further_study", "label": "Continue studying", "emoji": "🎓"},
        {"value": "work", "label": "Start working", "emoji": "💼"},
        {"value": "study_abroad", "label": "Study abroad", "emoji": "✈️"},
        {"value": "own_business", "label": "Start own business", "emoji": "🚀"},
        {"value": "not_sure", "label": "Not sure yet", "emoji": "🤔"},
    ],
}


IMPROVEMENT_GOALS_TRANSLATIONS = {
    "nl": [
        {"value": "better_grades", "label": "Betere cijfers halen", "emoji": "📈"},
        {"value": "study_planning", "label": "Studieplanning", "emoji": "📅"},
        {"value": "exam_prep", "label": "Examenvoorbereiding", "emoji": "📝"},
        {"value": "study_choice", "label": "Studiekeuze maken", "emoji": "🎯"},
        {"value": "motivation", "label": "Motivatie verbeteren", "emoji": "💪"},
        {"value": "stress", "label": "Stress verminderen", "emoji": "🧘"},
        {"value": "time_management", "label": "Timemanagement", "emoji": "⏰"},
        {"value": "career_orientation", "label": "Loopbaanoriëntatie", "emoji": "🧭"},
    ],
    "en": [
        {"value": "better_grades", "label": "Get better grades", "emoji": "📈"},
        {"value": "study_planning", "label": "Study planning", "emoji": "📅"},
        {"value": "exam_prep", "label": "Exam preparation", "emoji": "📝"},
        {"value": "study_choice", "label": "Choose a study", "emoji": "🎯"},
        {"value": "motivation", "label": "Improve motivation", "emoji": "💪"},
        {"value": "stress", "label": "Reduce stress", "emoji": "🧘"},
        {"value": "time_management", "label": "Time management", "emoji": "⏰"},
        {"value": "career_orientation", "label": "Career orientation", "emoji": "🧭"},
    ],
}


FORMALITY_OPTIONS_TRANSLATIONS = {
    "nl": [
        {"value": "informal", "label": "Informeel (je/jij)", "description": "Relaxed en vriendelijk", "emoji": "😊"},
        {"value": "normal", "label": "Normaal", "description": "Balans tussen formeel en informeel", "emoji": "👋"},
        {"value": "formal", "label": "Formeel (u)", "description": "Professioneel en beleefd", "emoji": "🎩"},
    ],
    "en": [
        {"value": "informal", "label": "Informal", "description": "Relaxed and friendly", "emoji": "😊"},
        {"value": "normal", "label": "Normal", "description": "Balance between formal and informal", "emoji": "👋"},
        {"value": "formal", "label": "Formal", "description": "Professional and polite", "emoji": "🎩"},
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def t(key: str, lang: str = "nl") -> str:
    """
    Get translation for a key in the specified language.
    
    Args:
        key: Translation key (e.g., "auth_login_title")
        lang: Language code ("nl" or "en"), defaults to Dutch
        
    Returns:
        Translated string, or key if not found
    """
    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(lang, TRANSLATIONS[key].get("nl", key))
    return key


def tx(key: str):
    """
    Get reactive translation for a key that updates with language changes.
    
    For use in Reflex components. Returns a conditional component that
    shows the correct translation based on AuthState.language.
    
    Args:
        key: Translation key (e.g., "auth_login_title")
        
    Returns:
        Reflex component with translation
    """
    import reflex as rx
    from educhat.state.auth_state import AuthState
    
    return rx.cond(
        AuthState.is_dutch,
        TRANSLATIONS.get(key, {}).get("nl", key),
        TRANSLATIONS.get(key, {}).get("en", key),
    )


def get_education_levels(lang: str = "nl") -> list:
    """Get education levels for the specified language."""
    return EDUCATION_LEVELS_TRANSLATIONS.get(lang, EDUCATION_LEVELS_TRANSLATIONS["nl"])


def get_study_directions(lang: str = "nl") -> list:
    """Get study directions for the specified language."""
    return STUDY_DIRECTIONS_TRANSLATIONS.get(lang, STUDY_DIRECTIONS_TRANSLATIONS["nl"])


def get_age_groups(lang: str = "nl") -> list:
    """Get age groups for the specified language."""
    return AGE_GROUPS_TRANSLATIONS.get(lang, AGE_GROUPS_TRANSLATIONS["nl"])


def get_school_subjects(lang: str = "nl") -> list:
    """Get school subjects for the specified language."""
    return SCHOOL_SUBJECTS_TRANSLATIONS.get(lang, SCHOOL_SUBJECTS_TRANSLATIONS["nl"])


def get_future_plans(lang: str = "nl") -> list:
    """Get future plans for the specified language."""
    return FUTURE_PLANS_TRANSLATIONS.get(lang, FUTURE_PLANS_TRANSLATIONS["nl"])


def get_improvement_goals(lang: str = "nl") -> list:
    """Get improvement goals for the specified language."""
    return IMPROVEMENT_GOALS_TRANSLATIONS.get(lang, IMPROVEMENT_GOALS_TRANSLATIONS["nl"])


def get_formality_options(lang: str = "nl") -> list:
    """Get formality options for the specified language."""
    return FORMALITY_OPTIONS_TRANSLATIONS.get(lang, FORMALITY_OPTIONS_TRANSLATIONS["nl"])


def get_districts() -> list:
    """Get districts (same for all languages - geographic names)."""
    return DISTRICTS


def get_month_name(month: int, lang: str = "nl") -> str:
    """Get month name for the specified language."""
    month_keys = [
        "month_january", "month_february", "month_march", "month_april",
        "month_may", "month_june", "month_july", "month_august",
        "month_september", "month_october", "month_november", "month_december"
    ]
    if 1 <= month <= 12:
        return t(month_keys[month - 1], lang)
    return ""


def get_weekday_short(day: int, lang: str = "nl") -> str:
    """Get short weekday name (0=Monday, 6=Sunday)."""
    day_keys = [
        "calendar_mon", "calendar_tue", "calendar_wed", "calendar_thu",
        "calendar_fri", "calendar_sat", "calendar_sun"
    ]
    if 0 <= day <= 6:
        return t(day_keys[day], lang)
    return ""


# =============================================================================
# AI SYSTEM PROMPTS - Bilingual
# =============================================================================

AI_SYSTEM_PROMPTS = {
    "nl": """Je bent EduChat, een vriendelijke AI-assistent gespecialiseerd in het Surinaams onderwijssysteem.

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
""",
    
    "en": """You are EduChat, a friendly AI assistant specialized in the Surinamese education system.

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
""",
}


def get_ai_system_prompt(lang: str = "nl") -> str:
    """Get the AI system prompt for the specified language."""
    return AI_SYSTEM_PROMPTS.get(lang, AI_SYSTEM_PROMPTS["nl"])
