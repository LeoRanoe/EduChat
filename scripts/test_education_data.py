"""
Test script to verify Supabase education data and search functionality.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from educhat.services.supabase_client import get_service
from educhat.services.education_service import get_education_service
from dotenv import load_dotenv

load_dotenv()


def test_supabase_connection():
    """Test basic Supabase connection."""
    print("🔌 Testing Supabase connection...")
    try:
        db = get_service()
        print("✅ Successfully connected to Supabase")
        return True
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return False


def test_institutions_table():
    """Test institutions table queries."""
    print("\n📚 Testing institutions table...")
    
    try:
        db = get_service()
        
        # Get all institutions
        institutions = db.get_all_institutions()
        print(f"   Found {len(institutions)} institutions in database")
        
        if institutions:
            print("\n   Sample institution:")
            inst = institutions[0]
            print(f"   - Name: {inst.get('name', 'N/A')}")
            print(f"   - Short name: {inst.get('short_name', 'N/A')}")
            print(f"   - Location: {inst.get('location', 'N/A')}")
        
        # Test search
        print("\n🔍 Testing search...")
        results = db.search_institutions("Universiteit")
        print(f"   Search 'Universiteit': {len(results)} results")
        
        if results:
            for r in results:
                print(f"   - {r.get('name', 'Unknown')}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_education_service():
    """Test education service integration."""
    print("\n🎓 Testing education service...")
    
    try:
        edu = get_education_service()
        
        # Test query context
        test_query = "Welke universiteiten zijn er in Suriname?"
        print(f"\n   Query: '{test_query}'")
        
        context = edu.get_context_for_query(test_query)
        if context:
            print("\n   Context generated:")
            print(f"   {context[:200]}...")
        else:
            print("   ⚠️  No context generated")
        
        # Test search
        print("\n🔍 Testing local + Supabase search...")
        results = edu.search_institutions("opleid")
        print(f"   Search 'opleid': {len(results)} results")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_database():
    """Clean up existing test data."""
    print("\n🗑️  Cleaning up database...")
    
    try:
        db = get_service()
        
        # Get all institutions
        institutions = db.get_all_institutions()
        print(f"   Found {len(institutions)} institutions to delete")
        
        if institutions:
            confirm = input("   Delete all institutions? (yes/no): ")
            if confirm.lower() == 'yes':
                for inst in institutions:
                    db.client.table('institutions').delete().eq('id', inst['id']).execute()
                print("   ✅ Database cleaned")
            else:
                print("   ❌ Cleanup cancelled")
        else:
            print("   ✅ Database already empty")
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("EduChat - Supabase Education Data Test")
    print("=" * 60)
    
    # Test connection
    if not test_supabase_connection():
        print("\n❌ Connection test failed. Fix connection before proceeding.")
        sys.exit(1)
    
    # Ask what to do
    print("\n" + "=" * 60)
    print("Options:")
    print("1. Test existing data")
    print("2. Clean database and exit (then run import)")
    print("3. Test everything (connection, data, search)")
    print("=" * 60)
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == '1':
        test_institutions_table()
        test_education_service()
    elif choice == '2':
        cleanup_database()
    elif choice == '3':
        test_institutions_table()
        test_education_service()
    else:
        print("Invalid choice")
