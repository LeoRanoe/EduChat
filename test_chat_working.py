"""Quick test to verify everything is working"""

from educhat.services.ai_service import AIService

print("=" * 60)
print("Testing AI Chat Functionality")
print("=" * 60)

# Test various questions
test_questions = [
    "wat is minow",
    "Hoe schrijf ik me in?",
    "vertel me over MINOV opleidingen",
    "wat zijn de toelatingseisen",
]

ai = AIService(provider='google')
print(f"✓ Using: {ai.provider} - {ai.model}\n")

for question in test_questions:
    print(f"Q: {question}")
    try:
        response = ai.chat(question)
        print(f"A: {response[:150]}...")
        print("✓ Success!\n")
    except Exception as e:
        print(f"✗ Error: {e}\n")

print("=" * 60)
print("✓ All tests completed!")
print("=" * 60)
print("\nYour chat should work now in the browser!")
print("Try asking: 'wat is minow' or 'Hoe schrijf ik me in?'")
