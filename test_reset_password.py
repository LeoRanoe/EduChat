"""
Test script to trigger password reset email for leonardoranoesendjojo@gmail.com
"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

async def test_reset_password():
    """Test triggering a password reset email."""
    from educhat.services.auth_service import get_auth_service
    
    email = "leonardoranoesendjojo@gmail.com"
    
    print("\n" + "="*60)
    print("[TEST] Triggering password reset for:", email)
    print("="*60 + "\n")
    
    auth_service = get_auth_service()
    result = await auth_service.reset_password(email)
    
    print("\n" + "="*60)
    print("[TEST] Result:", result)
    print("="*60 + "\n")
    
    if result.get("success"):
        print("✅ SUCCESS! Password reset email sent.")
        print("📧 Check your Gmail inbox: leonardoranoesendjojo@gmail.com")
        print("📧 Also check your SPAM folder if you don't see it.")
        print("\n⏰ The email may take 1-2 minutes to arrive.")
        print("\n🔗 The reset link will be in the format:")
        print("   http://localhost:3000/auth/reset-password#access_token=XXX&type=recovery")
    else:
        print("❌ FAILED:", result.get("error"))
    
    return result

if __name__ == "__main__":
    result = asyncio.run(test_reset_password())
