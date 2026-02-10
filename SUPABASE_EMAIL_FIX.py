"""
COMPLETE GUIDE: Fix Supabase Email Configuration
This will help you fix the "no emails arriving" issue.
"""

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                  SUPABASE EMAIL CONFIGURATION FIX                         ║
║                  leonardoranoesendjojo@gmail.com                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

🔍 PROBLEM IDENTIFIED:
   Supabase is not sending password reset emails. This happens when:
   - Email service is not configured in Supabase Dashboard
   - SMTP settings are missing or incorrect
   - Rate limits are hit on Supabase's default email service
   - User email is not verified in Supabase

📋 SOLUTION - Follow these steps IN ORDER:

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 1: Access Your Supabase Dashboard                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

1. Go to: https://supabase.com/dashboard/project/yeqfvvekdwtawbpusluu
2. Log in if needed

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 2: Check Authentication Settings                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

Navigate to: Authentication → Settings

Check these settings:
   ✅ Enable Email Signup: ENABLED
   ✅ Enable Email Confirmations: DISABLED (for testing)
   ✅ Secure Email Change: DISABLED (for testing)

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 3: Configure Email Templates                                        ║
╚═══════════════════════════════════════════════════════════════════════════╝

Navigate to: Authentication → Email Templates

You should see templates for:
   - Confirm signup
   - Magic Link
   - Change Email Address  
   - Reset Password ⬅️ THIS ONE IS IMPORTANT!

Click on "Reset Password" template and verify:
   ✅ Template is enabled
   ✅ Subject line is set
   ✅ Template contains {{ .ConfirmationURL }} or {{ .SiteURL }}

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 4: Check URL Configuration                                          ║
╚═══════════════════════════════════════════════════════════════════════════╝

Navigate to: Authentication → URL Configuration

Add these URLs to "Redirect URLs":
   ✅ http://localhost:3000/*
   ✅ http://localhost:3000/auth/reset-password
   ✅ http://localhost:3000/auth/callback

Site URL should be:
   ✅ http://localhost:3000

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 5: Configure SMTP (CRITICAL!)                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

Navigate to: Project Settings → Auth

Scroll down to "SMTP Settings"

Option A: Use Supabase's Built-in Email (Easiest)
   - Should work by default
   - Limited to ~3 emails per hour on free tier
   - May end up in spam folder

Option B: Configure Custom SMTP (Recommended)
   Use Gmail SMTP:
      Host: smtp.gmail.com
      Port: 587
      User: leonardoranoesendjojo@gmail.com
      Password: [Get App Password from Google]
      Sender email: leonardoranoesendjojo@gmail.com
      Sender name: EduChat

   To get Gmail App Password:
      1. Go to: https://myaccount.google.com/apppasswords
      2. Create new app password for "Mail"
      3. Copy the 16-character password
      4. Use it in SMTP settings

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 6: Verify User Email in Database                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

Navigate to: Authentication → Users

Find user: leonardoranoesendjojo@gmail.com

Check if:
   ✅ Email is confirmed/verified
   ✅ User is not banned
   ✅ Last sign in time shows recent activity

If email is NOT confirmed:
   1. Click on the user
   2. Click "Confirm email" button
   3. This manually confirms the email

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 7: Test Email Sending                                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

After configuration:

1. Run this command in terminal:
   python test_reset_password.py

2. Wait 2-3 minutes for email

3. Check these locations:
   ✅ Gmail Inbox
   ✅ Gmail Spam/Junk folder ⬅️ CHECK THIS!
   ✅ Gmail Promotions tab
   ✅ Gmail Updates tab

╔═══════════════════════════════════════════════════════════════════════════╗
║ STEP 8: Alternative Test (Skip Email)                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

If emails still don't arrive, test the password reset UI directly:

1. In Supabase Dashboard → Authentication → Users
2. Click on leonardoranoesendjojo@gmail.com
3. Click "Send recovery email" button
4. Or manually reset password using "Reset password" button

OR use this test URL format (you'll need a real token):
   http://localhost:3000/auth/reset-password#access_token=VALID_TOKEN&type=recovery

╔═══════════════════════════════════════════════════════════════════════════╗
║ COMMON ISSUES & SOLUTIONS                                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

Issue 1: "User not found"
Solution: Make sure leonardoranoesendjojo@gmail.com exists in Auth → Users

Issue 2: "Rate limit exceeded"  
Solution: Wait 1 hour, then try again. Or configure custom SMTP.

Issue 3: Emails in Spam
Solution: This is normal for localhost testing. Check spam folder!

Issue 4: "Invalid redirect URL"
Solution: Add http://localhost:3000/auth/reset-password to Redirect URLs

Issue 5: No SMTP settings visible
Solution: You need to be on a paid Supabase plan OR use default service

╔═══════════════════════════════════════════════════════════════════════════╗
║ NEXT STEPS                                                                ║
╚═══════════════════════════════════════════════════════════════════════════╝

1. Complete the configuration steps above
2. Run: python test_reset_password.py
3. Check your Gmail (including spam!) within 2-3 minutes
4. If email arrives, click the link and test password reset
5. If still no email, contact me with:
   - Screenshot of Auth → Settings page
   - Screenshot of Auth → Email Templates page  
   - Screenshot of Project Settings → Auth page (SMTP section)

═══════════════════════════════════════════════════════════════════════════

🔧 Want to test the password reset UI without waiting for email?
   Run: python test_direct_password_change.py

This will test changing password directly (logged in user)
to verify the UI works, separate from the email issue.

═══════════════════════════════════════════════════════════════════════════
""")
