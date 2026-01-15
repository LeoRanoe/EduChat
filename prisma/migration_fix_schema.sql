-- Migration: Fix Schema Issues
-- Date: 2026-01-15
-- Description: Fixes references to non-existent tables and removes deprecated users table
-- Run this ONLY if you have an existing database with the old schema

-- ============================================================================
-- STEP 1: Drop deprecated users table (Supabase Auth manages users now)
-- ============================================================================
-- WARNING: Only run if you're sure you want to remove the old users table
-- All user data should be in auth.users (Supabase Auth)

DROP TABLE IF EXISTS users CASCADE;

-- ============================================================================
-- STEP 2: Fix onboarding table - remove session_id reference
-- ============================================================================
-- The sessions table doesn't exist, we link directly to auth.users

-- Drop old index if it exists
DROP INDEX IF EXISTS idx_onboarding_session_id;

-- Remove session_id column if it exists
ALTER TABLE onboarding DROP COLUMN IF EXISTS session_id;

-- Ensure user_id is properly set
ALTER TABLE onboarding 
    ALTER COLUMN user_id SET NOT NULL,
    DROP CONSTRAINT IF EXISTS onboarding_user_id_fkey,
    ADD CONSTRAINT onboarding_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- Add answers column if it doesn't exist (for storing quiz answers as JSONB)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'onboarding' AND column_name = 'answers'
    ) THEN
        ALTER TABLE onboarding ADD COLUMN answers JSONB;
    END IF;
END $$;

-- ============================================================================
-- STEP 3: Fix reminders table - reference auth.users instead of old users table
-- ============================================================================

ALTER TABLE reminders 
    DROP CONSTRAINT IF EXISTS reminders_user_id_fkey,
    ADD CONSTRAINT reminders_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- ============================================================================
-- STEP 4: Fix conversations table - ensure it references auth.users
-- ============================================================================

ALTER TABLE conversations 
    DROP CONSTRAINT IF EXISTS conversations_user_id_fkey,
    ADD CONSTRAINT conversations_user_id_fkey 
        FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Schema migration completed successfully!';
    RAISE NOTICE '';
    RAISE NOTICE 'Changes applied:';
    RAISE NOTICE '  1. Removed deprecated users table';
    RAISE NOTICE '  2. Fixed onboarding table (removed session_id, added answers)';
    RAISE NOTICE '  3. Fixed reminders table (now references auth.users)';
    RAISE NOTICE '  4. Fixed conversations table (now references auth.users)';
    RAISE NOTICE '';
    RAISE NOTICE 'All foreign keys now correctly reference auth.users (Supabase Auth)';
END $$;
