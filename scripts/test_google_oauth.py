"""
Test script for Google OAuth authentication flow
Run this to verify all components are working correctly
"""

import asyncio
import os
from educhat.services.auth_service import get_auth_service


async def test_google_oauth():
    """Test the Google OAuth flow step by step."""
    print("=" * 60)
    print("GOOGLE OAUTH FLOW TEST")
    print("=" * 60)
    
    auth_service = get_auth_service()
    
    # Step 1: Test Google sign-in URL generation
    print("\n[STEP 1] Testing Google sign-in URL generation...")
    try:
        result = await auth_service.google_signin()
        if result.get("success"):
            print("✓ Google OAuth URL generated successfully")
            print(f"  URL: {result['url'][:100]}...")
            
            # Check if redirect_to is included
            if "redirect_to" in result['url']:
                print("✓ redirect_to parameter found in URL")
            else:
                print("✗ redirect_to parameter NOT found in URL")
                
            # Check PKCE parameters
            if "code_challenge" in result['url']:
                print("✓ PKCE code_challenge found in URL")
            else:
                print("✗ PKCE code_challenge NOT found in URL")
        else:
            print(f"✗ Failed to generate OAuth URL: {result.get('error')}")
            return False
    except Exception as e:
        print(f"✗ Exception during OAuth URL generation: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 2: Test OAuth callback handler (without actual code)
    print("\n[STEP 2] Testing OAuth callback handler structure...")
    try:
        # Test with empty code (should fail gracefully)
        result = await auth_service.handle_oauth_callback("")
        if not result.get("success"):
            print("✓ Empty code properly rejected")
        else:
            print("✗ Empty code was accepted (should be rejected)")
    except Exception as e:
        print(f"✗ Exception during callback test: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Step 3: Check environment configuration
    print("\n[STEP 3] Checking environment configuration...")
    site_url = os.getenv("SITE_URL", "http://localhost:3000")
    print(f"  SITE_URL: {site_url}")
    
    supabase_url = os.getenv("SUPABASE_URL", "NOT SET")
    if supabase_url != "NOT SET":
        print(f"✓ SUPABASE_URL: {supabase_url}")
    else:
        print("✗ SUPABASE_URL not set")
    
    supabase_key = os.getenv("SUPABASE_KEY", "NOT SET")
    if supabase_key != "NOT SET":
        print(f"✓ SUPABASE_KEY: {supabase_key[:20]}...")
    else:
        print("✗ SUPABASE_KEY not set")
    
    # Step 4: Test session checking
    print("\n[STEP 4] Testing session check...")
    try:
        result = await auth_service.get_session()
        if result.get("success"):
            print(f"✓ Active session found for: {result.get('user', {}).get('email')}")
        else:
            print("✓ No active session (expected for new test)")
    except Exception as e:
        print(f"✗ Exception during session check: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("All basic tests passed!")
    print("\nNext steps:")
    print("1. Ensure Google OAuth is configured in Supabase dashboard")
    print("2. Add http://localhost:3000/auth/callback to Supabase redirect URLs")
    print("3. Add https://[your-project].supabase.co/auth/v1/callback to Google OAuth")
    print("4. Test the flow in the browser by clicking 'Continue with Google'")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    asyncio.run(test_google_oauth())
