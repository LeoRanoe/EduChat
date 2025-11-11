"""
Pre-Deployment Verification Script for EduChat

Run this before pushing to GitHub/deploying to Render.
It checks that all required files and configurations are present.
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description=""):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    desc = f" - {description}" if description else ""
    print(f"{status} {filepath}{desc}")
    return exists

def check_env_var(var_name, required=True):
    """Check if environment variable is set."""
    value = os.getenv(var_name)
    exists = value is not None and value != ""
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUIRED" if required else "OPTIONAL"
    print(f"{status} {var_name} ({req_text})")
    return exists if required else True

def main():
    print("="*70)
    print("🚀 EduChat - Pre-Deployment Verification")
    print("="*70)
    print()
    
    all_good = True
    
    # Check required files
    print("📂 Checking deployment files...")
    files = {
        "render.yaml": "Render configuration",
        "start.sh": "Startup script",
        ".renderignore": "Build optimization",
        "requirements.txt": "Python dependencies",
        "rxconfig.py": "Reflex configuration",
        ".env.example": "Environment template",
        "RENDER_DEPLOYMENT.md": "Deployment guide",
        "DEPLOYMENT_SUMMARY.md": "Setup summary",
    }
    
    for filepath, desc in files.items():
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check database files
    print("🗄️ Checking database files...")
    db_files = {
        "prisma/create_tables.sql": "Table creation SQL",
        "prisma/rls_policies.sql": "Security policies",
    }
    
    for filepath, desc in db_files.items():
        if not check_file(filepath, desc):
            all_good = False
    print()
    
    # Check service files
    print("🔧 Checking service files...")
    service_files = {
        "educhat/services/supabase_client.py": ("Supabase service layer", True),
    }
    
    optional_service_files = {
        "seed_data.py": "Data seeding script",
        "test_service.py": "Connection test script",
    }
    
    for filepath, (desc, required) in service_files.items():
        if not check_file(filepath, desc):
            all_good = False
    
    for filepath, desc in optional_service_files.items():
        exists = os.path.exists(filepath)
        status = "✅" if exists else "⚠️"
        print(f"{status} {filepath} - {desc} (optional)")
    print()
    
    # Check environment variables
    print("🔐 Checking environment variables...")
    print("(Note: Load .env first with: python-dotenv or manually)")
    print()
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        "DATABASE_URL": True,
        "SUPABASE_URL": True,
        "SUPABASE_ANON_KEY": True,
        "SUPABASE_SERVICE_ROLE_KEY": True,
        "SESSION_SECRET": True,
    }
    
    optional_vars = {
        "OPENAI_API_KEY": False,
        "GOOGLE_AI_API_KEY": False,
        "APP_ENV": False,
        "DEBUG": False,
    }
    
    for var, required in required_vars.items():
        if not check_env_var(var, required):
            all_good = False
    
    for var, required in optional_vars.items():
        check_env_var(var, required)
    
    print()
    
    # Check dependencies
    print("📦 Checking Python dependencies...")
    try:
        import reflex
        print("✅ reflex installed")
    except ImportError:
        print("⚠️  reflex not installed (required for deployment)")
        print("   Run: pip install -r requirements.txt")
    
    try:
        from supabase import create_client
        print("✅ supabase installed")
    except ImportError:
        print("❌ supabase not installed")
        all_good = False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv installed")
    except ImportError:
        print("❌ python-dotenv not installed")
        all_good = False
    
    print()
    
    # Final verdict
    print("="*70)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print("="*70)
        print()
        print("🚀 You're ready to deploy!")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Add Render deployment configuration'")
        print("3. git push origin main")
        print("4. Go to https://dashboard.render.com/")
        print("5. Create new Web Service from your GitHub repo")
        print("6. Add environment variables in Render dashboard")
        print("7. Deploy!")
        print()
        return 0
    else:
        print("❌ SOME CHECKS FAILED")
        print("="*70)
        print()
        print("⚠️ Please fix the issues above before deploying.")
        print()
        print("Common fixes:")
        print("- Missing files: Check DEPLOYMENT_SUMMARY.md")
        print("- Missing env vars: Copy .env.example to .env and fill in values")
        print("- Missing dependencies: pip install -r requirements.txt")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
