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

# CRITICAL: Start a placeholder HTTP server IMMEDIATELY to satisfy Render's port check
# Then start Reflex which will take over the port after compilation
echo "Starting immediate port listener on $PORT..."

# Create a simple Python server that starts instantly
python3 << 'PYEOF' &
import os
import sys
import time
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get('PORT', 10000))

class QuickHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<html><body><h1>EduChat is starting...</h1><p>Initializing application, please wait...</p></body></html>')

print(f"Quick server starting on port {PORT}")
server = HTTPServer(('0.0.0.0', PORT), QuickHandler)

# Start Reflex in a subprocess
print("Starting Reflex...")
reflex_process = subprocess.Popen(
    ['reflex', 'run', '--env', 'prod', '--loglevel', 'info', 
     '--backend-host', '0.0.0.0', '--backend-port', str(PORT)],
    stdout=sys.stdout,
    stderr=sys.stderr
)

# Serve for 90 seconds to give Reflex time to compile and start
print("Placeholder server running, waiting for Reflex to take over...")
server.timeout = 1
for i in range(90):
    server.handle_request()
    if reflex_process.poll() is not None:
        print("Reflex process exited unexpectedly!")
        break

print("Shutting down placeholder server...")
server.server_close()

# Wait for Reflex to continue running
reflex_process.wait()
PYEOF

# Wait for everything to complete
wait
