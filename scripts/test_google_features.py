#!/usr/bin/env python3
"""
Quick test script to verify Google Auth and Calendar setup
"""

import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("Google Auth & Calendar - Quick Test")
print("=" * 60)

# Test 1: Check Supabase Google Auth Config
print("\n1. Checking Supabase Configuration...")
supabase_url = os.getenv('SUPABASE_URL')
if supabase_url:
    print(f"   ✓ Supabase URL: {supabase_url}")
    print(f"   → Manual check: Is Google provider enabled in Supabase?")
    print(f"   → Dashboard: {supabase_url.replace('https://', 'https://supabase.com/dashboard/project/')}")
else:
    print("   ✗ SUPABASE_URL not set")

# Test 2: Check credentials.json
print("\n2. Checking Google Calendar Credentials...")
from pathlib import Path
creds_file = Path("credentials/credentials.json")
if creds_file.exists():
    import json
    with open(creds_file, 'r') as f:
        data = json.load(f)
    
    if 'web' in data:
        print("   ✓ Web App credentials found")
        print(f"   → Client ID: {data['web']['client_id'][:20]}...")
        print(f"   → Project: {data['web']['project_id']}")
        print(f"   ⚠ Note: You have WEB credentials")
        print(f"   → These work for both Sign-In and Calendar")
    elif 'installed' in data:
        print("   ✓ Desktop App credentials found")
        print(f"   → Client ID: {data['installed']['client_id'][:20]}...")
    else:
        print("   ✗ Unknown credentials format")
else:
    print("   ✗ credentials.json not found")

# Test 3: Test Google Calendar Service
print("\n3. Testing Google Calendar Service...")
try:
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from educhat.services.google_calendar_service import GoogleCalendarService
    
    cal_service = GoogleCalendarService(user_id="test_user")
    print("   ✓ Calendar service initialized")
    print("   → Ready to authenticate (will open browser on first use)")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Check if Google Calendar API is enabled
print("\n4. Google Calendar API Status...")
print("   ⚠ Manual check required:")
print("   → Go to: https://console.cloud.google.com/apis/dashboard")
print(f"   → Project: gen-lang-client-0858981362")
print("   → Verify 'Google Calendar API' is enabled")

print("\n" + "=" * 60)
print("Next Steps:")
print("=" * 60)
print("1. Enable Google Calendar API in Google Cloud Console")
print("   https://console.cloud.google.com/apis/library/calendar-json.googleapis.com")
print()
print("2. Configure Google provider in Supabase:")
print("   - Client ID: 10600403770-g5d8giep61tgb9g0ccm6hpbio8l8saco.apps.googleusercontent.com")
print("   - Client Secret: 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")
print()
print("3. Test the features:")
print("   - Google Sign-In: http://localhost:3000")
print("   - Calendar Sync: Click 'Sync Events' in the app")
print("=" * 60)
