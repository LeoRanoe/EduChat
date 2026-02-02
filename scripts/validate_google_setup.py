#!/usr/bin/env python3
"""
Google Auth & Calendar Setup Validation Script
Checks all prerequisites before running the application
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def check_dependencies() -> Tuple[bool, List[str]]:
    """Check if required Python packages are installed"""
    print_header("1. Checking Python Dependencies")
    
    required_packages = [
        ('google.auth', 'google-auth'),
        ('google_auth_oauthlib', 'google-auth-oauthlib'),
        ('google_auth_httplib2', 'google-auth-httplib2'),
        ('googleapiclient', 'google-api-python-client'),
        ('bs4', 'beautifulsoup4'),
        ('aiohttp', 'aiohttp'),
        ('supabase', 'supabase'),
        ('openai', 'openai'),
        ('google.generativeai', 'google-generativeai'),
    ]
    
    missing = []
    all_installed = True
    
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
            print_success(f"{package_name} is installed")
        except ImportError:
            print_error(f"{package_name} is NOT installed")
            missing.append(package_name)
            all_installed = False
    
    return all_installed, missing


def check_env_variables() -> Tuple[bool, List[str]]:
    """Check if required environment variables are set"""
    print_header("2. Checking Environment Variables")
    
    required_vars = [
        ('SUPABASE_URL', 'Supabase project URL'),
        ('SUPABASE_ANON_KEY', 'Supabase anonymous key'),
        ('SITE_URL', 'Site URL for OAuth redirects'),
    ]
    
    optional_vars = [
        ('OPENAI_API_KEY', 'OpenAI API key (for AI features)'),
        ('GOOGLE_AI_API_KEY', 'Google AI API key (alternative to OpenAI)'),
        ('SUPABASE_SERVICE_ROLE_KEY', 'Supabase service role key'),
    ]
    
    missing = []
    all_present = True
    
    # Check required variables
    for var_name, description in required_vars:
        value = os.getenv(var_name)
        if value and value.strip():
            print_success(f"{var_name}: {description}")
        else:
            print_error(f"{var_name} is NOT set - {description}")
            missing.append(var_name)
            all_present = False
    
    # Check optional variables (at least one AI key needed)
    ai_key_present = False
    for var_name, description in optional_vars:
        value = os.getenv(var_name)
        if value and value.strip():
            print_success(f"{var_name}: {description}")
            if 'API_KEY' in var_name and ('OPENAI' in var_name or 'GOOGLE_AI' in var_name):
                ai_key_present = True
        else:
            print_warning(f"{var_name} is NOT set - {description}")
    
    if not ai_key_present:
        print_error("No AI API key found (need OPENAI_API_KEY or GOOGLE_AI_API_KEY)")
        missing.append("AI_API_KEY")
        all_present = False
    
    return all_present, missing


def check_credentials_folder() -> Tuple[bool, List[str]]:
    """Check credentials folder setup"""
    print_header("3. Checking Credentials Folder")
    
    issues = []
    all_good = True
    
    # Check if credentials folder exists
    creds_dir = Path("credentials")
    if not creds_dir.exists():
        print_error("credentials/ folder does NOT exist")
        issues.append("credentials/ folder missing")
        all_good = False
        return all_good, issues
    else:
        print_success("credentials/ folder exists")
    
    # Check for credentials.json
    creds_file = creds_dir / "credentials.json"
    if creds_file.exists():
        print_success("credentials.json found")
        
        # Try to validate it's valid JSON
        try:
            import json
            with open(creds_file, 'r') as f:
                data = json.load(f)
                if 'installed' in data or 'web' in data:
                    print_success("credentials.json appears valid")
                else:
                    print_warning("credentials.json format may be incorrect")
        except json.JSONDecodeError:
            print_error("credentials.json is NOT valid JSON")
            issues.append("Invalid credentials.json")
            all_good = False
    else:
        print_error("credentials.json NOT found in credentials/ folder")
        print_info("Download from Google Cloud Console and place in credentials/")
        issues.append("credentials.json missing")
        all_good = False
    
    # Check for .gitignore
    gitignore = creds_dir / ".gitignore"
    if gitignore.exists():
        print_success(".gitignore exists in credentials/ folder")
    else:
        print_warning(".gitignore missing in credentials/ (credentials may be exposed to git)")
    
    return all_good, issues


def check_env_file() -> Tuple[bool, List[str]]:
    """Check if .env file exists"""
    print_header("4. Checking .env File")
    
    issues = []
    all_good = True
    
    env_file = Path(".env")
    if env_file.exists():
        print_success(".env file exists")
        
        # Load dotenv
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print_success("Successfully loaded .env file")
        except ImportError:
            print_warning("python-dotenv not installed")
        except Exception as e:
            print_error(f"Error loading .env: {e}")
            issues.append(".env loading error")
            all_good = False
    else:
        print_error(".env file does NOT exist")
        print_info("Copy .env.example to .env and fill in your values")
        issues.append(".env file missing")
        all_good = False
    
    return all_good, issues


def check_google_cloud_setup() -> None:
    """Display Google Cloud Console setup checklist"""
    print_header("5. Google Cloud Console Setup (Manual)")
    
    print_info("You need to manually complete these steps in Google Cloud Console:")
    print("\n1. Create/Select a Google Cloud Project")
    print("   → https://console.cloud.google.com/")
    
    print("\n2. Enable Google Calendar API")
    print("   → APIs & Services → Enable APIs and Services")
    print("   → Search for 'Google Calendar API' → Enable")
    
    print("\n3. Create OAuth 2.0 Credentials")
    print("   → APIs & Services → Credentials → Create Credentials")
    
    print("\n   A. Desktop App Credentials (for Calendar API)")
    print("      → Application type: Desktop app")
    print("      → Download JSON → Save as credentials/credentials.json")
    
    print("\n   B. Web App Credentials (for Google Sign-In)")
    print("      → Application type: Web application")
    print("      → Add Authorized redirect URIs:")
    print("         • http://localhost:3000/auth/callback")
    print("         • https://[your-supabase-project].supabase.co/auth/v1/callback")
    print("      → Note the Client ID and Client Secret")
    
    print_warning("These steps must be completed manually!")


def check_supabase_setup() -> None:
    """Display Supabase setup checklist"""
    print_header("6. Supabase Setup (Manual)")
    
    print_info("You need to manually complete these steps in Supabase Dashboard:")
    print("\n1. Enable Google Authentication Provider")
    print("   → Authentication → Providers → Google")
    print("   → Enable Google provider")
    print("   → Enter Client ID and Client Secret from Google Cloud Console (Web App)")
    
    print("\n2. Configure Redirect URLs")
    print("   → Authentication → URL Configuration")
    print("   → Add redirect URLs:")
    print("      • http://localhost:3000/auth/callback (development)")
    print("      • https://yourdomain.com/auth/callback (production)")
    
    print("\n3. Verify Database Tables")
    print("   → Table Editor → Check for required tables:")
    print("      • users, user_profiles, reminders, chat_history, etc.")
    
    print_warning("These steps must be completed manually!")


def main():
    """Run all validation checks"""
    print(f"\n{Colors.BOLD}Google Auth & Calendar Setup Validator{Colors.RESET}")
    print(f"{Colors.BOLD}EduChat Application{Colors.RESET}\n")
    
    all_checks_passed = True
    all_issues = []
    
    # Run automated checks
    deps_ok, missing_deps = check_dependencies()
    if not deps_ok:
        all_checks_passed = False
        all_issues.extend(missing_deps)
    
    env_file_ok, env_file_issues = check_env_file()
    if not env_file_ok:
        all_checks_passed = False
        all_issues.extend(env_file_issues)
    
    env_vars_ok, missing_vars = check_env_variables()
    if not env_vars_ok:
        all_checks_passed = False
        all_issues.extend(missing_vars)
    
    creds_ok, creds_issues = check_credentials_folder()
    if not creds_ok:
        all_checks_passed = False
        all_issues.extend(creds_issues)
    
    # Display manual setup checklists
    check_google_cloud_setup()
    check_supabase_setup()
    
    # Summary
    print_header("Validation Summary")
    
    if all_checks_passed:
        print_success("All automated checks PASSED! ✓")
        print_info("Complete the manual setup steps above, then run: reflex run")
    else:
        print_error(f"Found {len(all_issues)} issues that need attention:")
        for issue in all_issues:
            print(f"  • {issue}")
        
        print("\n" + Colors.BOLD + "Next Steps:" + Colors.RESET)
        
        if missing_deps:
            print("1. Install missing packages:")
            print(f"   pip install {' '.join(missing_deps)}")
        
        if missing_vars or env_file_issues:
            print("2. Create/update .env file with required variables")
            print("   Copy .env.example to .env and fill in values")
        
        if creds_issues:
            print("3. Download credentials.json from Google Cloud Console")
            print("   Place in credentials/ folder")
        
        print("\nThen run this script again to verify!")
    
    print()
    sys.exit(0 if all_checks_passed else 1)


if __name__ == "__main__":
    main()
