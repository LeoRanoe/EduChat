"""Test script to verify Gemini API integration"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test 1: Check if API key is loaded
print("=" * 50)
print("TEST 1: Environment Variables")
print("=" * 50)
api_key = os.getenv("GOOGLE_AI_API_KEY")
if api_key:
    print(f"✓ GOOGLE_AI_API_KEY found: {api_key[:10]}...{api_key[-4:]}")
else:
    print("✗ GOOGLE_AI_API_KEY not found")
    exit(1)

# Test 2: Import Google AI library
print("\n" + "=" * 50)
print("TEST 2: Import Google AI Library")
print("=" * 50)
try:
    import google.generativeai as genai
    print("✓ google.generativeai imported successfully")
except ImportError as e:
    print(f"✗ Failed to import: {e}")
    exit(1)

# Test 3: Configure and test API
print("\n" + "=" * 50)
print("TEST 3: Configure and Test API")
print("=" * 50)
try:
    genai.configure(api_key=api_key)
    print("✓ API configured successfully")
    
    # List available models
    print("\nAvailable Gemini models:")
    for model in genai.list_models():
        if 'gemini' in model.name.lower():
            print(f"  - {model.name}")
    
except Exception as e:
    print(f"✗ Configuration failed: {e}")
    exit(1)

# Test 4: Simple API call
print("\n" + "=" * 50)
print("TEST 4: Simple API Call")
print("=" * 50)
try:
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Say hello in Dutch")
    print(f"✓ API call successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ API call failed: {e}")
    exit(1)

# Test 5: Test AIService
print("\n" + "=" * 50)
print("TEST 5: Test AIService")
print("=" * 50)
try:
    from educhat.services.ai_service import AIService
    
    ai_service = AIService(provider="google")
    print(f"✓ AIService initialized with provider: {ai_service.provider}")
    print(f"✓ Using model: {ai_service.model}")
    
    # Test a simple education question
    response = ai_service.chat("Hoe schrijf ik me in voor MINOV?")
    print(f"✓ Chat response received!")
    print(f"Response preview: {response[:200]}...")
    
except Exception as e:
    print(f"✗ AIService test failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n" + "=" * 50)
print("✓ ALL TESTS PASSED!")
print("=" * 50)
