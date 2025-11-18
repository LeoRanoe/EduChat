-- EduChat Database Schema Migration
-- Run this in Supabase SQL Editor to create all tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- === Knowledge Base Tables ===

-- Institutions table
CREATE TABLE IF NOT EXISTS institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR NOT NULL,
    short_name VARCHAR,
    description TEXT,
    location VARCHAR,
    website VARCHAR,
    contact JSONB,
    enrollment_process TEXT,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_institutions_name ON institutions(name);

-- Studies table
CREATE TABLE IF NOT EXISTS studies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL,
    faculty VARCHAR,
    description TEXT,
    type VARCHAR,
    duration INTEGER,
    admission TEXT,
    career_opportunities TEXT,
    keywords TEXT,
    source VARCHAR,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_studies_institution_id ON studies(institution_id);
CREATE INDEX idx_studies_title ON studies(title);
CREATE INDEX idx_studies_type ON studies(type);

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID REFERENCES institutions(id) ON DELETE SET NULL,
    title VARCHAR NOT NULL,
    type VARCHAR,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    description TEXT,
    source VARCHAR,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_events_institution_id ON events(institution_id);
CREATE INDEX idx_events_date ON events(date);
CREATE INDEX idx_events_type ON events(type);

-- === User Management Tables ===

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    settings JSONB
);

CREATE INDEX idx_users_email ON users(email);

-- Conversations table (replaces sessions)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL DEFAULT 'New Conversation',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    archived BOOLEAN DEFAULT FALSE,
    metadata JSONB
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
CREATE INDEX idx_conversations_archived ON conversations(archived);

-- Messages table
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    feedback VARCHAR CHECK (feedback IN ('like', 'dislike')),
    feedback_timestamp TIMESTAMP WITH TIME ZONE,
    is_streaming BOOLEAN DEFAULT FALSE,
    is_error BOOLEAN DEFAULT FALSE,
    metadata JSONB
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_messages_role ON messages(role);

-- === Onboarding Tables ===

-- Onboarding table
CREATE TABLE IF NOT EXISTS onboarding (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    current_step INTEGER DEFAULT 0,
    interests JSONB,
    skills JSONB,
    goals JSONB,
    personality VARCHAR,
    quiz_results JSONB,
    suggested_paths JSONB,
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_onboarding_session_id ON onboarding(session_id);
CREATE INDEX idx_onboarding_user_id ON onboarding(user_id);
CREATE INDEX idx_onboarding_completed ON onboarding(completed);

-- Onboarding Questions table
CREATE TABLE IF NOT EXISTS onboarding_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    question TEXT NOT NULL,
    options JSONB,
    category VARCHAR,
    order_num INTEGER NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_onboarding_questions_category ON onboarding_questions(category);
CREATE INDEX idx_onboarding_questions_order_num ON onboarding_questions(order_num);

-- Onboarding Answers table
CREATE TABLE IF NOT EXISTS onboarding_answers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    onboarding_id UUID NOT NULL REFERENCES onboarding(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES onboarding_questions(id) ON DELETE CASCADE,
    selected_option TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_onboarding_answers_onboarding_id ON onboarding_answers(onboarding_id);
CREATE INDEX idx_onboarding_answers_question_id ON onboarding_answers(question_id);

-- === Reminders Table ===

CREATE TABLE IF NOT EXISTS reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    event_id UUID REFERENCES events(id) ON DELETE SET NULL,
    title VARCHAR NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_reminders_user_id ON reminders(user_id);
CREATE INDEX idx_reminders_event_id ON reminders(event_id);
CREATE INDEX idx_reminders_date ON reminders(date);
CREATE INDEX idx_reminders_sent ON reminders(sent, date);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Run the RLS policies from prisma/rls_policies.sql';
    RAISE NOTICE '2. Test connection with: python manage_db.py test';
    RAISE NOTICE '3. Seed data with: python manage_db.py seed';
END $$;
