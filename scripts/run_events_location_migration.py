"""Run migration to add 'location' column to events table."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

def run():
    import re

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("ERROR: DATABASE_URL not set in environment")
        return False

    try:
        import psycopg2
    except ImportError:
        print("psycopg2 not installed, trying psycopg2-binary...")
        os.system(f"{sys.executable} -m pip install psycopg2-binary -q")
        import psycopg2

    # Remove brackets from password (some .env formats use [password])
    clean_url = re.sub(r'\[([^\]]+)\]', r'\1', db_url)

    # Try direct connection first; fall back to Supabase transaction pooler.
    password_match = re.search(r':([^:@]+)@', clean_url)
    pwd = password_match.group(1) if password_match else ''

    project_ref = 'yeqfvvekdwtawbpusluu'
    urls_to_try = [
        clean_url,
        f'postgresql://postgres.{project_ref}:{pwd}@aws-0-us-east-1.pooler.supabase.com:6543/postgres',
    ]

    conn = None
    for attempt_url in urls_to_try:
        try:
            print(f"Trying: {attempt_url[:60]}...")
            conn = psycopg2.connect(attempt_url, connect_timeout=10)
            print("Connected!")
            break
        except Exception as e:
            print(f"  Failed: {e}")

    if conn is None:
        print("ERROR: Could not connect to database via any URL")
        return False
    conn.autocommit = True
    cur = conn.cursor()

    print("Running migration: ADD COLUMN location to events...")
    cur.execute("ALTER TABLE public.events ADD COLUMN IF NOT EXISTS location TEXT;")
    print("ALTER TABLE executed.")

    # Verify
    cur.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name='events' AND column_name='location';"
    )
    row = cur.fetchone()
    if row:
        print(f"✓ Column 'location' now exists in events table")
    else:
        print("✗ Column was NOT found after migration!")

    conn.close()
    return bool(row)

if __name__ == "__main__":
    success = run()
    sys.exit(0 if success else 1)
