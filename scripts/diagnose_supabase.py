"""
Diagnostic Tool: Check Supabase Configuration Status
This script checks your current Supabase setup to identify issues.
"""
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def diagnose_supabase():
    """Run diagnostics on Supabase configuration."""
    print("\n" + "="*70)
    print("🔍 SUPABASE CONFIGURATION DIAGNOSTICS")
    print("="*70 + "\n")
    
    # Check environment variables
    print("📋 STEP 1: Checking Environment Variables")
    print("-" * 70)
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_anon = os.getenv("SUPABASE_ANON_KEY")
    supabase_service = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    site_url = os.getenv("SITE_URL")
    
    if supabase_url:
        print(f"✅ SUPABASE_URL: {supabase_url}")
    else:
        print("❌ SUPABASE_URL: NOT SET")
        
    if supabase_anon:
        print(f"✅ SUPABASE_ANON_KEY: {supabase_anon[:20]}...")
    else:
        print("❌ SUPABASE_ANON_KEY: NOT SET")
        
    if supabase_service:
        print(f"✅ SUPABASE_SERVICE_ROLE_KEY: {supabase_service[:20]}...")
    else:
        print("❌ SUPABASE_SERVICE_ROLE_KEY: NOT SET")
        
    if site_url:
        print(f"✅ SITE_URL: {site_url}")
    else:
        print("❌ SITE_URL: NOT SET")
    
    print()
    
    # Test Supabase connection
    print("📋 STEP 2: Testing Supabase Connection")
    print("-" * 70)
    
    try:
        from educhat.services.supabase_client import get_client
        client = get_client()
        print("✅ Supabase client initialized successfully")
        
        # Try to check auth
        try:
            # This will fail if not authenticated, but that's ok - we just want to test connection
            session = client.auth.get_session()
            print(f"✅ Auth API connection successful")
        except Exception as e:
            if "network" in str(e).lower() or "connection" in str(e).lower():
                print(f"❌ Cannot connect to Supabase: {e}")
            else:
                print(f"✅ Auth API connection successful (session check expected to fail)")
        
    except Exception as e:
        print(f"❌ Failed to initialize Supabase client: {e}")
        return
    
    print()
    
    # Check user existence
    print("📋 STEP 3: Checking User in Database")
    print("-" * 70)
    
    email = "leonardoranoesendjojo@gmail.com"
    
    try:
        # Query to check if user exists
        response = client.table("users").select("*").eq("email", email).execute()
        
        if response.data and len(response.data) > 0:
            user = response.data[0]
            print(f"✅ User found in database:")
            print(f"   - Email: {user.get('email')}")
            print(f"   - User ID: {user.get('id')}")
            print(f"   - Role: {user.get('role')}")
        else:
            print(f"⚠️  User NOT found in users table")
            print(f"   This might mean the user only exists in auth.users")
            print(f"   Check Supabase Dashboard → Authentication → Users")
    except Exception as e:
        print(f"⚠️  Could not query users table: {e}")
        print(f"   User might still exist in auth.users (Supabase Auth)")
    
    print()
    
    # Provide next steps
    print("📋 STEP 4: Next Actions")
    print("-" * 70)
    print()
    print("If all checks above passed, the issue is likely:")
    print("   1. Supabase email service not configured (most likely)")
    print("   2. User email not verified in Supabase")
    print("   3. Rate limiting on email sends")
    print()
    print("🔧 TO FIX:")
    print("   1. Go to Supabase Dashboard")
    print("   2. Check Authentication → Users for the user")
    print("   3. Configure Project Settings → Auth → SMTP Settings")
    print("   4. Or manually send recovery email from Dashboard")
    print()
    print("📖 For detailed instructions, run:")
    print("   python SUPABASE_EMAIL_FIX.py")
    print()
    print("🧪 To test the password reset UI (without email):")
    print("   1. Go to Supabase Dashboard → Authentication → Users")
    print("   2. Click 'Send recovery email' button for the user")
    print("   3. Copy the URL from the email that arrives")
    print("   4. Change the domain to http://localhost:3000")
    print()
    print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(diagnose_supabase())
