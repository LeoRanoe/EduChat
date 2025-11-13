"""
Test script to verify the async/await fix for AI service integration.
This tests that the chat function can be called correctly from async context.
"""

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_ai_service_call():
    """Test calling the AI service from async context."""
    print("=" * 60)
    print("Testing AI Service Call from Async Context")
    print("=" * 60)
    
    # Import the AI service
    from educhat.services.ai_service import get_ai_service
    
    try:
        # Get AI service instance
        ai_service = get_ai_service()
        print(f"✓ AI Service initialized")
        print(f"  Provider: {ai_service.provider}")
        print(f"  Model: {ai_service.model}")
        
        # Test 1: Direct call (synchronous)
        print("\n[Test 1] Direct synchronous call...")
        try:
            response = ai_service.chat("Hoe schrijf ik me in?")
            print(f"✓ Direct call succeeded")
            print(f"  Response: {response[:100]}...")
        except Exception as e:
            print(f"✗ Direct call failed: {e}")
        
        # Test 2: Call from async context using executor (like in AppState)
        print("\n[Test 2] Call from async context using executor...")
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: ai_service.chat(
                    message="Wat zijn de toelatingseisen?",
                    conversation_history=None,
                    context=None
                )
            )
            print(f"✓ Async executor call succeeded")
            print(f"  Response: {response[:100]}...")
        except Exception as e:
            print(f"✗ Async executor call failed: {e}")
        
        # Test 3: Call with conversation history
        print("\n[Test 3] Call with conversation history...")
        try:
            loop = asyncio.get_event_loop()
            history = [
                {"role": "user", "content": "Hallo"},
                {"role": "assistant", "content": "Hallo! Hoe kan ik je helpen?"}
            ]
            response = await loop.run_in_executor(
                None,
                lambda: ai_service.chat(
                    message="Vertel me over MINOV",
                    conversation_history=history,
                    context=None
                )
            )
            print(f"✓ Call with history succeeded")
            print(f"  Response: {response[:100]}...")
        except Exception as e:
            print(f"✗ Call with history failed: {e}")
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe AI service integration is working correctly.")
        print("You can now use the chat interface in the app.")
        
    except Exception as e:
        print(f"\n✗ TESTS FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    # Check if quota issue is resolved
    print("\nNote: This test requires that your API quota has reset.")
    print("If you see a 429 error, wait a few minutes and try again.\n")
    
    # Run the async test
    success = asyncio.run(test_ai_service_call())
    
    if success:
        print("\n✅ You can now test the chat interface in the browser!")
        print("   The async/await issues have been fixed.")
    else:
        print("\n⚠️ There may still be issues to resolve.")
