"""
ALTERNATIVE TEST: Simulate password reset URL
This creates a test URL you can manually use to test the reset password page UI.
NOTE: You'll still need a real token from Supabase for it to actually work.
"""
import webbrowser
import time

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║              MANUAL PASSWORD RESET URL TEST                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

Since Supabase emails aren't arriving, here's how to manually test:

METHOD 1: Get Token from Supabase Dashboard
══════════════════════════════════════════════════════════════════════════

1. Go to: https://supabase.com/dashboard/project/yeqfvvekdwtawbpusluu
2. Navigate to: Authentication → Users
3. Find user: leonardoranoesendjojo@gmail.com
4. Click the three dots (...) menu
5. Click "Send recovery email" 
6. Check your email (including SPAM folder!)
7. Copy the full URL from the email

The URL should look like:
   https://yeqfvvekdwtawbpusluu.supabase.co/auth/v1/verify?token=XXX&type=recovery&redirect_to=...

8. Change the beginning to: http://localhost:3000/auth/reset-password
9. Change the ? to #
10. Remove everything after &type=recovery

Final format should be:
   http://localhost:3000/auth/reset-password#access_token=LONG_TOKEN_HERE&type=recovery


METHOD 2: Test with Development Account
══════════════════════════════════════════════════════════════════════════

If you have access to Supabase Dashboard:

1. Create a new test user
2. From Dashboard manually reset their password
3. Or manually update password in database

METHOD 3: Check Supabase Logs
══════════════════════════════════════════════════════════════════════════

1. Go to: https://supabase.com/dashboard/project/yeqfvvekdwtawbpusluu
2. Navigate to: Logs → Auth Logs
3. Look for "password_recovery" events
4. Check if emails are being attempted
5. Look for any error messages

TESTING THE UI (WITHOUT EMAIL)
══════════════════════════════════════════════════════════════════════════

You can test the UI appearance by visiting:
   http://localhost:3000/auth/reset-password

This will show:
   ✅ The password reset form
   ❌ Error: "Wachten op reset token..." (waiting for token)
   
This is EXPECTED since you don't have a token in the URL hash.

TO FIX THE EMAIL ISSUE PERMANENTLY:
══════════════════════════════════════════════════════════════════════════

Run this command to see the complete fix guide:
   python SUPABASE_EMAIL_FIX.py

Or configure SMTP in Supabase Dashboard:
   Project Settings → Auth → SMTP Settings

╚═══════════════════════════════════════════════════════════════════════════╝
""")

print("\n⏳ Opening password reset page in 3 seconds...")
print("   (This will show the UI without a token)")
time.sleep(3)

url = "http://localhost:3000/auth/reset-password"
print(f"\n🌐 Opening: {url}")
try:
    webbrowser.open(url)
    print("✅ Browser opened!")
    print("\n📝 You should see:")
    print("   - Password reset form")
    print("   - Red box saying 'Wachten op reset token...'")
    print("   - This is NORMAL without a valid token in URL")
except Exception as e:
    print(f"❌ Could not open browser: {e}")
    print(f"\nManually visit: {url}")
