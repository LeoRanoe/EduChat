# Database Migrations Guide

## 📋 Overview

This folder contains SQL migration files for the EduChat database schema.

---

## 🗂️ Migration Files

### 1. `create_tables.sql` (Initial Schema)
**Purpose:** Creates all database tables from scratch  
**When to use:** Setting up a new database  
**Run:** Once at initial setup

```sql
-- In Supabase SQL Editor:
-- Copy and paste the entire create_tables.sql content
```

---

### 2. `migration_fix_schema.sql` (Schema Fixes)
**Purpose:** Fixes schema issues in existing databases  
**When to use:** If you have an old schema that needs updating  
**Run:** Once to migrate from old schema to new schema

**What it fixes:**
- ✅ Removes deprecated `users` table (Supabase Auth manages users now)
- ✅ Fixes `onboarding` table (removes non-existent `session_id` reference)
- ✅ Adds `answers` JSONB column to `onboarding` table
- ✅ Updates `reminders` to reference `auth.users` instead of old `users` table
- ✅ Updates `conversations` to reference `auth.users`

```sql
-- In Supabase SQL Editor:
-- Copy and paste the entire migration_fix_schema.sql content
```

⚠️ **WARNING:** This migration drops the old `users` table. Make sure all user data is in Supabase Auth (`auth.users`) before running.

---

### 3. `rls_policies.sql` (Row Level Security)
**Purpose:** Sets up Row Level Security policies  
**When to use:** After creating tables (recommended for security)  
**Run:** Once after initial setup or schema migration

---

## 🚀 Setup Instructions

### For New Database (Fresh Install)

```bash
# Step 1: Create Supabase project at https://supabase.com
# Step 2: Go to SQL Editor in Supabase Dashboard
# Step 3: Run create_tables.sql
# Step 4: Run rls_policies.sql (optional but recommended)
# Step 5: Done! ✅
```

### For Existing Database (Migration)

```bash
# Step 1: Backup your database first!
# Step 2: Go to SQL Editor in Supabase Dashboard
# Step 3: Run migration_fix_schema.sql
# Step 4: Verify everything works
# Step 5: Done! ✅
```

---

## 🔍 Verifying Migration Success

After running migrations, verify with these queries:

```sql
-- Check that users table is gone
SELECT table_name FROM information_schema.tables 
WHERE table_name = 'users';
-- Should return no rows

-- Check onboarding table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'onboarding';
-- Should NOT have session_id
-- Should have answers (jsonb)

-- Check foreign key constraints
SELECT
    conname AS constraint_name,
    conrelid::regclass AS table_name,
    confrelid::regclass AS referenced_table
FROM pg_constraint
WHERE contype = 'f' 
AND (conrelid::regclass::text = 'onboarding' 
     OR conrelid::regclass::text = 'reminders'
     OR conrelid::regclass::text = 'conversations');
-- All should reference auth.users
```

---

## 📝 Migration History

| Date | File | Description |
|------|------|-------------|
| 2026-01-15 | `migration_fix_schema.sql` | Fixed schema issues: removed old users table, fixed foreign keys to auth.users |
| 2025-XX-XX | `create_tables.sql` | Initial schema creation |

---

## 🐛 Troubleshooting

### Error: "table users does not exist"
**Solution:** This is expected if you already ran the migration. The old users table has been removed.

### Error: "column session_id does not exist"
**Solution:** This is expected after migration. The session_id column has been removed from onboarding table.

### Error: "relation auth.users does not exist"
**Problem:** Supabase Auth is not enabled  
**Solution:** 
1. Go to Supabase Dashboard
2. Authentication should be enabled by default
3. If not, contact Supabase support

### Foreign Key Constraint Errors
**Problem:** Existing data references old users table  
**Solution:** 
1. Backup your data first
2. Migrate user data to Supabase Auth before running migration
3. Or manually update foreign keys in your data

---

## 🔐 Best Practices

1. **Always backup before migrations**
   ```bash
   # In Supabase Dashboard:
   # Settings > Database > Backups
   ```

2. **Test migrations on staging first**
   - Create a separate Supabase project for testing
   - Run migration there first
   - Verify everything works

3. **Run migrations in order**
   - Initial setup: `create_tables.sql` → `rls_policies.sql`
   - Existing DB: `migration_fix_schema.sql` → verify

4. **Check logs after migration**
   ```sql
   -- Check for any errors
   SELECT * FROM pg_stat_activity WHERE state = 'active';
   ```

---

## 📞 Support

If you encounter issues:

1. Check the error message in Supabase SQL Editor
2. Review the verification queries above
3. Check [DATABASE_OVERVIEW.md](../DATABASE_OVERVIEW.md) for schema documentation
4. Open an issue on GitHub

---

**Last Updated:** January 15, 2026
