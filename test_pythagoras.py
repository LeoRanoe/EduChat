"""
Quick test voor Pythagoras detectie
"""

message = "wat is de stelling van poethagoeras"
message_lower = message.lower()

# Test de keywords
wiskunde_keywords = [
    "wiskunde", "math", "pythagoras", "poethagoeras", "pitagoras", 
    "stelling", "theorem", "vergelijking", "algebra"
]

print("=" * 60)
print("PYTHAGORAS DETECTIE TEST")
print("=" * 60)
print(f"\nVraag: '{message}'")
print(f"\nGevonden keywords:")

found = []
for keyword in wiskunde_keywords:
    if keyword in message_lower:
        found.append(keyword)
        print(f"  ✅ {keyword}")

if found:
    print(f"\n✅ RESULTAAT: Wiskunde vraag gedetecteerd!")
    print(f"   Mode: schoolwork")
    print(f"   Subject: wiskunde")
    print(f"   Topics: {found}")
    print(f"\n✅ Deze vraag zou MOETEN werken in de app!")
else:
    print(f"\n❌ PROBLEEM: Geen wiskunde keywords gevonden!")
    print(f"   De vraag wordt NIET herkend als schoolwork")

print("=" * 60)

# Test ook educational context
educational_words = ["stelling", "pythagoras", "poethagoeras"]
has_educational = any(word in message_lower for word in educational_words)

print(f"\nEducatieve context check:")
if has_educational:
    print(f"  ✅ Bevat educatieve woorden: {[w for w in educational_words if w in message_lower]}")
    print(f"  ✅ Filter zou deze vraag MOETEN doorlaten")
else:
    print(f"  ❌ Geen educatieve woorden gevonden")

print("=" * 60)
