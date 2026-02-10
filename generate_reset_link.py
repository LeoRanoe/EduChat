"""
WORKAROUND: Generate a password reset link manually (bypassing email)
This script generates a valid password reset URL that you can use directly in your browser.
Use this while we fix the Supabase email configuration.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

async def generate_reset_link():
    """Generate a password reset link for testing."""
    from educhat.services.supabase_client import get_client
    
    email = "leonardoranoesendjojo@gmail.com"
    
    print("\n" + "="*60)
    print("[WORKAROUND] Generating password reset link manually")
    print("="*60 + "\n")
    
    print("⚠️  NOTE: This is a workaround because Supabase emails aren't")
    print("   arriving. We'll generate the reset link manually.\n")
    
    try:
        client = get_client()
        
        # Method 1: Try to generate a password reset token using Admin API
        print("[1] Attempting to generate recovery token via Admin API...")
        
        result = await asyncio.to_thread(
            lambda: client.auth.admin.generate_link({
                "type": "recovery",
                "email": email,
            })
        )
        
        if result and result.properties:
            action_link = result.properties.get("action_link", "")
            if action_link:
                # Extract the token from the action link
                # Format: https://xxx.supabase.co/auth/v1/verify?token=XXX&type=recovery&redirect_to=...
                import urllib.parse
                parsed = urllib.parse.urlparse(action_link)
                params = urllib.parse.parse_qs(parsed.query)
                
                token = params.get('token', [''])[0]
                
                if token:
                    # Build the local reset URL
                    reset_url = f"http://localhost:3000/auth/reset-password#access_token={token}&type=recovery"
                    
                    print("\n" + "="*60)
                    print("✅ SUCCESS! Manual reset link generated:")
                    print("="*60)
                    print(f"\n{reset_url}\n")
                    print("="*60)
                    print("\n📋 INSTRUCTIONS:")
                    print("1. Copy the URL above")
                    print("2. Open your browser with DevTools (F12) Console tab open")
                    print("3. Paste the URL into your browser address bar")
                    print("4. Press Enter")
                    print("5. Watch the console logs for token extraction")
                    print("6. Enter your new password: test123456")
                    print("7. Click 'Wachtwoord Wijzigen'")
                    print("\n⏰ This token is valid for 1 hour.")
                    print("="*60 + "\n")
                    
                    return {"success": True, "url": reset_url, "token": token}
        
        print("❌ Could not generate token using Admin API")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "="*60)
        print("⚠️  SUPABASE EMAIL CONFIGURATION ISSUE DETECTED")
        print("="*60)
        print("\nTo fix Supabase email sending, follow these steps:")
        print("\n1. Go to: https://supabase.com/dashboard/project/yeqfvvekdwtawbpusluu")
        print("2. Navigate to: Authentication → Email Templates")
        print("3. Check if 'Enable Custom SMTP' is configured")
        print("4. If not, either:")
        print("   a) Configure custom SMTP (Gmail, SendGrid, etc.)")
        print("   b) Or use Supabase's built-in email service")
        print("\n5. Make sure 'Confirm email' is DISABLED for testing:")
        print("   Authentication → Settings → Email Auth")
        print("   Uncheck 'Enable email confirmations'")
        print("\n6. Verify your redirect URLs:")
        print("   Authentication → URL Configuration")
        print("   Add: http://localhost:3000/auth/reset-password")
        print("="*60 + "\n")
        
    return {"success": False}

if __name__ == "__main__":
    result = asyncio.run(generate_reset_link())
