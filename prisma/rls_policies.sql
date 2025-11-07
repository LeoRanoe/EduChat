-- Row-Level Security (RLS) Policies for EduChat
-- Apply these policies after running Prisma migrations
-- These policies ensure data security and proper access control

-- Enable RLS on all tables
ALTER TABLE institutions ENABLE ROW LEVEL SECURITY;
ALTER TABLE studies ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_questions ENABLE ROW LEVEL SECURITY;
ALTER TABLE onboarding_answers ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminders ENABLE ROW LEVEL SECURITY;

-- =============================================
-- PUBLIC READ ACCESS (Knowledge Base)
-- Institutions, Studies, Events are public
-- =============================================

-- Institutions: Public read, service role write
CREATE POLICY "Public read access for institutions"
ON institutions FOR SELECT
USING (true);

CREATE POLICY "Service role can insert institutions"
ON institutions FOR INSERT
WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role can update institutions"
ON institutions FOR UPDATE
USING (auth.role() = 'service_role');

-- Studies: Public read, service role write
CREATE POLICY "Public read access for studies"
ON studies FOR SELECT
USING (true);

CREATE POLICY "Service role can insert studies"
ON studies FOR INSERT
WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role can update studies"
ON studies FOR UPDATE
USING (auth.role() = 'service_role');

-- Events: Public read, service role write
CREATE POLICY "Public read access for events"
ON events FOR SELECT
USING (true);

CREATE POLICY "Service role can insert events"
ON events FOR INSERT
WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "Service role can update events"
ON events FOR UPDATE
USING (auth.role() = 'service_role');

-- =============================================
-- USER DATA (Private)
-- Users can only access their own data
-- =============================================

-- Users: Users can read their own data
CREATE POLICY "Users can read own profile"
ON users FOR SELECT
USING (auth.uid()::text = id);

CREATE POLICY "Service role can manage users"
ON users FOR ALL
USING (auth.role() = 'service_role');

-- Sessions: Users can read own sessions, anonymous can read by anonymous_id
CREATE POLICY "Users can read own sessions"
ON sessions FOR SELECT
USING (
  auth.uid()::text = user_id 
  OR auth.role() = 'service_role'
);

CREATE POLICY "Service role can manage sessions"
ON sessions FOR ALL
USING (auth.role() = 'service_role');

-- Messages: Users can read messages from their sessions
CREATE POLICY "Users can read messages from own sessions"
ON messages FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM sessions 
    WHERE sessions.id = messages.session_id 
    AND (sessions.user_id = auth.uid()::text OR auth.role() = 'service_role')
  )
);

CREATE POLICY "Service role can manage messages"
ON messages FOR ALL
USING (auth.role() = 'service_role');

-- =============================================
-- ONBOARDING DATA
-- =============================================

-- Onboarding: Users can read own onboarding
CREATE POLICY "Users can read own onboarding"
ON onboarding FOR SELECT
USING (
  auth.uid()::text = user_id 
  OR auth.role() = 'service_role'
);

CREATE POLICY "Service role can manage onboarding"
ON onboarding FOR ALL
USING (auth.role() = 'service_role');

-- Onboarding Questions: Public read
CREATE POLICY "Public read access for onboarding questions"
ON onboarding_questions FOR SELECT
USING (active = true OR auth.role() = 'service_role');

CREATE POLICY "Service role can manage onboarding questions"
ON onboarding_questions FOR ALL
USING (auth.role() = 'service_role');

-- Onboarding Answers: Users can read own answers
CREATE POLICY "Users can read own onboarding answers"
ON onboarding_answers FOR SELECT
USING (
  EXISTS (
    SELECT 1 FROM onboarding 
    WHERE onboarding.id = onboarding_answers.onboarding_id 
    AND (onboarding.user_id = auth.uid()::text OR auth.role() = 'service_role')
  )
);

CREATE POLICY "Service role can manage onboarding answers"
ON onboarding_answers FOR ALL
USING (auth.role() = 'service_role');

-- =============================================
-- REMINDERS
-- =============================================

-- Reminders: Users can only access their own reminders
CREATE POLICY "Users can read own reminders"
ON reminders FOR SELECT
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can create own reminders"
ON reminders FOR INSERT
WITH CHECK (auth.uid()::text = user_id);

CREATE POLICY "Users can update own reminders"
ON reminders FOR UPDATE
USING (auth.uid()::text = user_id);

CREATE POLICY "Users can delete own reminders"
ON reminders FOR DELETE
USING (auth.uid()::text = user_id);

CREATE POLICY "Service role can manage all reminders"
ON reminders FOR ALL
USING (auth.role() = 'service_role');

-- =============================================
-- INDEXES FOR PERFORMANCE
-- =============================================

-- Full-text search indexes using GIN
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;

-- Institution search
CREATE INDEX idx_institutions_name_trgm ON institutions USING GIN (name gin_trgm_ops);
CREATE INDEX idx_institutions_description_trgm ON institutions USING GIN (description gin_trgm_ops);

-- Study search
CREATE INDEX idx_studies_title_trgm ON studies USING GIN (title gin_trgm_ops);
CREATE INDEX idx_studies_keywords_trgm ON studies USING GIN (keywords gin_trgm_ops);
CREATE INDEX idx_studies_description_trgm ON studies USING GIN (description gin_trgm_ops);

-- Message search (for future features)
CREATE INDEX idx_messages_content_trgm ON messages USING GIN (content gin_trgm_ops);

-- Composite indexes for common queries
CREATE INDEX idx_sessions_user_last_active ON sessions (user_id, last_active DESC);
CREATE INDEX idx_messages_session_timestamp ON messages (session_id, timestamp);
CREATE INDEX idx_reminders_user_date ON reminders (user_id, date) WHERE sent = false;

-- =============================================
-- FUNCTIONS FOR SEARCH
-- =============================================

-- Function to search institutions
CREATE OR REPLACE FUNCTION search_institutions(search_query TEXT)
RETURNS TABLE (
  id VARCHAR,
  name VARCHAR,
  short_name VARCHAR,
  description TEXT,
  location VARCHAR,
  similarity REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    i.id,
    i.name,
    i.short_name,
    i.description,
    i.location,
    GREATEST(
      similarity(i.name, search_query),
      similarity(COALESCE(i.short_name, ''), search_query),
      similarity(COALESCE(i.description, ''), search_query)
    ) as similarity
  FROM institutions i
  WHERE 
    i.name ILIKE '%' || search_query || '%'
    OR i.short_name ILIKE '%' || search_query || '%'
    OR i.description ILIKE '%' || search_query || '%'
  ORDER BY similarity DESC
  LIMIT 20;
END;
$$ LANGUAGE plpgsql;

-- Function to search studies
CREATE OR REPLACE FUNCTION search_studies(search_query TEXT)
RETURNS TABLE (
  id VARCHAR,
  institution_id VARCHAR,
  title VARCHAR,
  description TEXT,
  type VARCHAR,
  keywords TEXT,
  similarity REAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT 
    s.id,
    s.institution_id,
    s.title,
    s.description,
    s.type,
    s.keywords,
    GREATEST(
      similarity(s.title, search_query),
      similarity(COALESCE(s.keywords, ''), search_query),
      similarity(COALESCE(s.description, ''), search_query)
    ) as similarity
  FROM studies s
  WHERE 
    s.title ILIKE '%' || search_query || '%'
    OR s.keywords ILIKE '%' || search_query || '%'
    OR s.description ILIKE '%' || search_query || '%'
  ORDER BY similarity DESC
  LIMIT 30;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- COMMENTS
-- =============================================

COMMENT ON POLICY "Public read access for institutions" ON institutions IS 
'Allows anyone to read institution data for knowledge base';

COMMENT ON POLICY "Service role can manage sessions" ON sessions IS 
'Backend service needs full access to manage chat sessions';

COMMENT ON FUNCTION search_institutions IS 
'Full-text search for institutions using trigram similarity';

COMMENT ON FUNCTION search_studies IS 
'Full-text search for studies using trigram similarity';
