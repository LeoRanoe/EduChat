# IMMEDIATE FIX FOR RENDER DEPLOYMENT

## The Problem
Your Render dashboard is using the **OLD start command**. The render.yaml file has the correct settings, but Render dashboard overrides need to be updated manually.

## SOLUTION - Update Render Dashboard Settings

### Step 1: Update Start Command
1. Go to your Render dashboard → educhat service
2. Click "Settings" (or the settings tab)
3. Find "Start Command"
4. **Change it from**:
   ```
   reflex run --env prod --loglevel info --backend-host 0.0.0.0 --backend-port $PORT
   ```
   **To**:
   ```
   bash start.sh
   ```
5. Click "Save Changes"

### Step 2: Update Build Command  
1. In the same Settings page
2. Find "Build Command"
3. **Make sure it says**:
   ```
   pip install --upgrade pip && pip install -r requirements.txt && reflex init
   ```
4. If different, update it and save

### Step 3: Verify Environment Variables
Make sure these are set in Environment tab:

**IMPORTANT**: Do NOT set `PORT` manually - Render sets it automatically!

Required variables:
- `RENDER` = `true`
- `APP_ENV` = `production`
- `DATABASE_URL` = (your Supabase connection string)
- `SUPABASE_URL` = (your Supabase URL)
- `SUPABASE_ANON_KEY` = (your key)
- `SUPABASE_SERVICE_ROLE_KEY` = (your key)
- `GOOGLE_AI_API_KEY` = (your key)

**If you manually set PORT, DELETE IT!** It should be auto-set by Render.

### Step 4: Manual Deploy
1. Click "Manual Deploy" → "Deploy latest commit"
2. Watch the logs

## Expected Result

You should see:
```
🚀 Starting EduChat on Render...
📋 Checking environment variables...
✅ Environment variables OK
🔌 Testing Supabase connection...
✅ Supabase connection successful
✅ Startup checks complete!
🌐 Starting Reflex application...
Port: 10000
Starting Reflex in production mode...
Compiling: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
Backend running at: http://0.0.0.0:10000
```

The compilation will take 30-60 seconds, but the port should open and Render should detect it.

## Alternative: Fresh Start

If updating settings doesn't work, delete the service and create fresh:

1. Delete the `educhat` service in Render
2. Go to Render dashboard → "New" → "Blueprint"
3. Connect your GitHub repo
4. Select the `render.yaml` file
5. Add all environment variables
6. Deploy

---

**The key issue**: The start command in Render dashboard doesn't match render.yaml. Fix that first!
