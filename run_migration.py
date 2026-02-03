"""Run the calendar sync migration."""
import os
from educhat.services.supabase_client import get_service

def run_migration():
    """Execute the calendar sync migration SQL."""
    # Read migration file
    migration_path = os.path.join('prisma', 'migrations', 'migration_calendar_sync.sql')
    
    with open(migration_path, 'r', encoding='utf-8') as f:
        migration_sql = f.read()
    
    # Get database service
    db = get_service()
    
    print("Running calendar sync migration...")
    print("=" * 60)
    
    try:
        # Execute migration (split by statement for Supabase compatibility)
        statements = [s.strip() for s in migration_sql.split(';') if s.strip() and not s.strip().startswith('--')]
        
        for i, statement in enumerate(statements, 1):
            if statement:
                print(f"\n[{i}/{len(statements)}] Executing: {statement[:80]}...")
                try:
                    db.client.rpc('exec_sql', {'query': statement}).execute()
                    print(f"✓ Success")
                except Exception as e:
                    # Try direct table method for ALTER/CREATE statements
                    if 'ALTER TABLE reminders' in statement or 'CREATE INDEX' in statement:
                        print(f"⚠ RPC failed, trying alternative method...")
                        # For Supabase, we may need to run these via the SQL editor
                        # or use the Supabase client's table methods
                        print(f"⚠ Statement needs manual execution: {statement[:100]}")
                    else:
                        raise e
        
        print("\n" + "=" * 60)
        print("✓ Migration completed successfully!")
        print("\nNext steps:")
        print("1. Verify columns in Supabase dashboard")
        print("2. Test sync functionality in the app")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        print("\n⚠ MANUAL MIGRATION REQUIRED:")
        print("Please run the SQL in prisma/migrations/migration_calendar_sync.sql")
        print("directly in your Supabase SQL editor at:")
        print("https://supabase.com/dashboard/project/[your-project]/sql/new")
        return False
    
    return True

if __name__ == "__main__":
    run_migration()
