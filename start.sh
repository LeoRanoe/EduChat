#!/usr/bin/env bash
# Render startup script for EduChat
# This script runs on Render after the build command completes

set -e  # Exit on error

echo "🚀 Starting EduChat on Render..."
echo "================================"

# Check required environment variables
echo "📋 Checking environment variables..."
if [ -z "$SUPABASE_URL" ]; then
    echo "❌ ERROR: SUPABASE_URL is not set"
    exit 1
fi

if [ -z "$SUPABASE_ANON_KEY" ] && [ -z "$SUPABASE_SERVICE_ROLE_KEY" ]; then
    echo "❌ ERROR: Neither SUPABASE_ANON_KEY nor SUPABASE_SERVICE_ROLE_KEY is set"
    exit 1
fi

echo "✅ Environment variables OK"

# Test database connection
echo "🔌 Testing Supabase connection..."
python -c "
from educhat.services.supabase_client import get_client
try:
    client = get_client()
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
    exit(1)
"

# Run any database migrations/setup if needed
# echo "🔄 Running database setup..."
# python seed_data.py  # Uncomment if you want to seed on startup

echo "================================"
echo "✅ Startup checks complete!"
echo "🌐 Starting Reflex application..."
echo "Port: $PORT"
echo "================================"

# Set environment variables for production
export REFLEX_ENV=prod
export APP_ENV=production
export NODE_OPTIONS="--max-old-space-size=512"

# Start Reflex in production mode
# Production mode uses much less memory than dev mode
echo "Starting Reflex backend on 0.0.0.0:$PORT..."
exec reflex run --env prod --loglevel warning --backend-host 0.0.0.0 --backend-port $PORT
