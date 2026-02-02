#!/usr/bin/env python3
"""
Interactive setup checklist for Google Auth & Calendar features
Run this after completing manual configuration steps
"""

import os
import sys
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def print_box(title, items, completed_items):
    """Print a checklist box"""
    width = 60
    print(f"\n{BOLD}{BLUE}┌{'─' * (width-2)}┐{RESET}")
    print(f"{BOLD}{BLUE}│ {title.ljust(width-3)}│{RESET}")
    print(f"{BOLD}{BLUE}├{'─' * (width-2)}┤{RESET}")
    
    for i, item in enumerate(items, 1):
        check = f"{GREEN}✓{RESET}" if i in completed_items else f"{RED}✗{RESET}"
        print(f"{BOLD}{BLUE}│{RESET} {check} {item.ljust(width-5)}{BOLD}{BLUE}│{RESET}")
    
    print(f"{BOLD}{BLUE}└{'─' * (width-2)}┘{RESET}")
    
    completed = len(completed_items)
    total = len(items)
    percentage = (completed / total * 100) if total > 0 else 0
    
    if completed == total:
        print(f"{GREEN}{BOLD}✓ COMPLETE ({completed}/{total}) - {percentage:.0f}%{RESET}")
    else:
        print(f"{YELLOW}{BOLD}⚠ IN PROGRESS ({completed}/{total}) - {percentage:.0f}%{RESET}")

def check_automated_prerequisites():
    """Check automated prerequisites and return completed items"""
    completed = []
    
    # Check dependencies
    try:
        import google.auth
        import google_auth_oauthlib
        import googleapiclient
        import bs4
        import aiohttp
        completed.append(1)
    except ImportError:
        pass
    
    # Check .env file
    if Path(".env").exists():
        from dotenv import load_dotenv
        load_dotenv()
        completed.append(2)
    
    # Check environment variables
    required_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SITE_URL']
    if all(os.getenv(var) for var in required_vars):
        completed.append(3)
    
    # Check AI key (at least one)
    if os.getenv('OPENAI_API_KEY') or os.getenv('GOOGLE_AI_API_KEY'):
        completed.append(4)
    
    # Check credentials folder
    if Path("credentials").exists():
        completed.append(5)
    
    # Check credentials .gitignore
    if Path("credentials/.gitignore").exists():
        completed.append(6)
    
    return completed

def check_manual_configuration():
    """Check manual configuration and return completed items"""
    completed = []
    
    # Check credentials.json
    if Path("credentials/credentials.json").exists():
        try:
            import json
            with open("credentials/credentials.json", 'r') as f:
                data = json.load(f)
                if 'installed' in data or 'web' in data:
                    completed.append(1)
        except:
            pass
    
    # Can't automatically check Google Cloud Console setup
    # User needs to confirm manually
    
    return completed

def main():
    """Main interactive checklist"""
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}{'Google Auth & Calendar Setup Progress'.center(60)}{RESET}")
    print(f"{BOLD}{'EduChat Application'.center(60)}{RESET}")
    print(f"{BOLD}{'='*60}{RESET}")
    
    # Automated Prerequisites
    auto_items = [
        "Google packages installed (google-auth, etc.)",
        ".env file exists",
        "Environment variables configured",
        "AI API key configured (Google AI or OpenAI)",
        "credentials/ folder created",
        "credentials/.gitignore created",
    ]
    auto_completed = check_automated_prerequisites()
    print_box("AUTOMATED PREREQUISITES", auto_items, auto_completed)
    
    # Manual Configuration - Google Cloud Console
    google_items = [
        "credentials.json downloaded and placed in credentials/",
        "Google Cloud project created",
        "Google Calendar API enabled",
        "Desktop App OAuth credentials created",
        "Web App OAuth credentials created",
        "Client ID and Client Secret copied",
    ]
    google_completed = check_manual_configuration()
    print_box("GOOGLE CLOUD CONSOLE (Manual)", google_items, google_completed)
    
    # Manual Configuration - Supabase
    supabase_items = [
        "Navigate to Supabase Dashboard",
        "Go to Authentication → Providers → Google",
        "Enable Google provider",
        "Paste Client ID from Google Cloud Console",
        "Paste Client Secret from Google Cloud Console",
        "Click Save",
        "Verify redirect URLs configured",
    ]
    supabase_completed = []  # Can't auto-check, user must verify
    print_box("SUPABASE CONFIGURATION (Manual)", supabase_items, supabase_completed)
    
    # Testing
    testing_items = [
        "Run validation script (python scripts/validate_google_setup.py)",
        "Start application (reflex run)",
        "Test Google Sign-In at http://localhost:3000",
        "Test Calendar Sync (Events → Sync button)",
        "Verify events display in calendar",
        "Create reminder and verify sync to Google Calendar",
    ]
    testing_completed = []  # Can't auto-check
    print_box("TESTING CHECKLIST", testing_items, testing_completed)
    
    # Overall Progress
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    auto_progress = len(auto_completed) / len(auto_items) * 100
    
    print(f"\n{BOLD}Overall Progress:{RESET}")
    print(f"  • Automated Setup: {GREEN}{auto_progress:.0f}%{RESET} ({len(auto_completed)}/{len(auto_items)})")
    print(f"  • Manual Config:   {YELLOW}Requires your action{RESET}")
    print(f"  • Testing:         {YELLOW}After configuration{RESET}")
    
    # Next Steps
    print(f"\n{BOLD}Next Steps:{RESET}")
    
    if auto_progress < 100:
        print(f"  {RED}1. Complete automated prerequisites{RESET}")
        print(f"     Run: {BLUE}pip install -r requirements.txt{RESET}")
    else:
        print(f"  {GREEN}✓ Automated prerequisites complete!{RESET}")
    
    if not Path("credentials/credentials.json").exists():
        print(f"  {YELLOW}2. Follow Google Cloud Console setup{RESET}")
        print(f"     Guide: {BLUE}GOOGLE_QUICK_START.md{RESET}")
    else:
        print(f"  {GREEN}✓ credentials.json found!{RESET}")
    
    print(f"  {YELLOW}3. Complete Supabase configuration{RESET}")
    print(f"     Guide: {BLUE}GOOGLE_QUICK_START.md → Step 2{RESET}")
    
    print(f"  {YELLOW}4. Test the features{RESET}")
    print(f"     Run: {BLUE}reflex run{RESET}")
    
    # Documentation
    print(f"\n{BOLD}Documentation:{RESET}")
    print(f"  • Quick Start:  {BLUE}GOOGLE_QUICK_START.md{RESET}")
    print(f"  • Full Guide:   {BLUE}GOOGLE_SETUP_COMPLETE_GUIDE.md{RESET}")
    print(f"  • Validation:   {BLUE}python scripts/validate_google_setup.py{RESET}")
    
    print(f"\n{BOLD}{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()
