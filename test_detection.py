"""
Test script voor schoolwork detectie - Debug hulp

Dit script test of vragen correct worden gedetecteerd als schoolwork of institutions.
"""

# Test cases
test_cases = [
    # Schoolwork vragen (moeten NIET geblokkeerd worden)
    "wat is de stelling van poethagoeras",
    "wat is de stelling van pythagoras",
    "hoe los je een vergelijking op",
    "leg kwadratische vergelijkingen uit",
    "help me met wiskunde",
    "wat is fotosynthese",
    "hoe werkt de d/t regel",
    "mijn python code geeft een error",
    
    # Inschrijving vragen (moeten ook NIET geblokkeerd worden)
    "hoe schrijf ik me in bij adekus",
    "wat zijn de toelatingseisen voor minov",
    "wanneer is de deadline voor inschrijving",
    
    # Zeer off-topic (mogen WEL geblokkeerd worden)
    "wat is het weer vandaag",
    "voetbalwedstrijd vanavond",
    "filmtips voor dit weekend",
]

print("=" * 60)
print("SCHOOLWORK DETECTIE TEST")
print("=" * 60)

# Simuleer de nieuwe detectie logica
def test_detection(message: str):
    """Test of een vraag geblokkeerd wordt."""
    message_lower = message.lower()
    
    # VERY specific off-topic phrases
    definitely_off_topic = [
        "weer vandaag", "weersverwachting morgen", "hoeveel graden wordt het",
        "voetbalwedstrijd vanavond", "voetbaluitslagen gisteren",
        "welke film kijken", "filmreview", "nieuwe films bioscoop",
    ]
    
    # Educational context words
    educational_context_words = [
        "studie", "school", "leren", "examen", "huiswerk", "opdracht",
        "uitleg", "uitleggen", "begrip", "begrijpen", "snap",
        "wiskunde", "nederlands", "engels", "biologie", "natuurkunde",
        "stelling", "pythagoras", "poethagoeras", "vergelijking", "formule",
        "fotosynthese", "d/t", "regel", "code", "error", "python",
        "inschrijven", "toelating", "deadline", "adekus", "minov",
    ]
    
    is_definitely_off_topic = any(phrase in message_lower for phrase in definitely_off_topic)
    has_educational_context = any(word in message_lower for word in educational_context_words)
    
    # Beslissing
    if is_definitely_off_topic and not has_educational_context:
        return "❌ GEBLOKKEERD (off-topic)"
    else:
        return "✅ TOEGESTAAN (gaat naar AI)"

print("\n📚 SCHOOLWORK VRAGEN:")
print("-" * 60)
for question in test_cases[:8]:
    result = test_detection(question)
    print(f"{result:<30} | {question}")

print("\n🏫 INSCHRIJVING VRAGEN:")
print("-" * 60)
for question in test_cases[8:11]:
    result = test_detection(question)
    print(f"{result:<30} | {question}")

print("\n🚫 OFF-TOPIC VRAGEN:")
print("-" * 60)
for question in test_cases[11:]:
    result = test_detection(question)
    print(f"{result:<30} | {question}")

print("\n" + "=" * 60)
print("CONCLUSIE:")
print("=" * 60)
print("✅ Alle schoolwork vragen moeten TOEGESTAAN zijn")
print("✅ Alle inschrijving vragen moeten TOEGESTAAN zijn")
print("❌ Zeer off-topic vragen mogen GEBLOKKEERD worden")
print("\nAls dit niet klopt, is er een probleem met de filter!")
print("=" * 60)
