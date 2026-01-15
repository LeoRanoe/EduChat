-- Fix RLS policies for conversation-based chat history
-- Run this in Supabase SQL Editor after migration_chat_history.sql

-- Drop old message policies that reference sessions
DROP POLICY IF EXISTS "Users can read messages from own sessions" ON messages;
DROP POLICY IF EXISTS "Service role can manage messages" ON messages;
DROP POLICY IF EXISTS "Users can read messages from their conversations" ON messages;
DROP POLICY IF EXISTS "Users can create messages in their conversations" ON messages;
DROP POLICY IF EXISTS "Users can update messages in their conversations" ON messages;
DROP POLICY IF EXISTS "Users can delete messages in their conversations" ON messages;

-- Enable RLS on conversations and messages if not already
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- =============================================
-- CONVERSATIONS RLS POLICIES
-- =============================================

-- Allow service role full access (bypasses RLS when using service_role key)
CREATE POLICY "Service role full access to conversations"
ON conversations FOR ALL
USING (auth.role() = 'service_role')
WITH CHECK (auth.role() = 'service_role');

-- Users can view their own conversations
CREATE POLICY "Users can view own conversations"
ON conversations FOR SELECT
USING (auth.uid() = user_id OR auth.role() = 'service_role');

-- Users can create their own conversations  
CREATE POLICY "Users can create own conversations"
ON conversations FOR INSERT
WITH CHECK (auth.uid() = user_id OR auth.role() = 'service_role');

-- Users can update their own conversations
CREATE POLICY "Users can update own conversations"
ON conversations FOR UPDATE
USING (auth.uid() = user_id OR auth.role() = 'service_role');

-- Users can delete their own conversations
CREATE POLICY "Users can delete own conversations"
ON conversations FOR DELETE
USING (auth.uid() = user_id OR auth.role() = 'service_role');

-- =============================================
-- MESSAGES RLS POLICIES (using conversation_id)
-- =============================================

-- Allow service role full access
CREATE POLICY "Service role full access to messages"
ON messages FOR ALL
USING (auth.role() = 'service_role')
WITH CHECK (auth.role() = 'service_role');

-- Users can view messages in their conversations
CREATE POLICY "Users can view messages in own conversations"
ON messages FOR SELECT
USING (
    auth.role() = 'service_role'
    OR EXISTS (
        SELECT 1 FROM conversations
        WHERE conversations.id = messages.conversation_id
        AND conversations.user_id = auth.uid()
    )
);

-- Users can insert messages in their conversations
CREATE POLICY "Users can insert messages in own conversations"
ON messages FOR INSERT
WITH CHECK (
    auth.role() = 'service_role'
    OR EXISTS (
        SELECT 1 FROM conversations
        WHERE conversations.id = conversation_id
        AND conversations.user_id = auth.uid()
    )
);

-- Users can update messages in their conversations
CREATE POLICY "Users can update messages in own conversations"
ON messages FOR UPDATE
USING (
    auth.role() = 'service_role'
    OR EXISTS (
        SELECT 1 FROM conversations
        WHERE conversations.id = messages.conversation_id
        AND conversations.user_id = auth.uid()
    )
);

-- Users can delete messages in their conversations
CREATE POLICY "Users can delete messages in own conversations"
ON messages FOR DELETE
USING (
    auth.role() = 'service_role'
    OR EXISTS (
        SELECT 1 FROM conversations
        WHERE conversations.id = messages.conversation_id
        AND conversations.user_id = auth.uid()
    )
);

-- =============================================
-- GRANT PERMISSIONS
-- =============================================

-- Grant all permissions to authenticated users
GRANT ALL ON conversations TO authenticated;
GRANT ALL ON messages TO authenticated;

-- Grant select to anon for public access patterns
GRANT SELECT ON conversations TO anon;
GRANT SELECT ON messages TO anon;
