# EduChat Render Deployment Checklist

## Pre-Deployment Checklist

### 1. Code Changes (All Done ✅)
- [x] `rxconfig.py` - Production mode configuration
- [x] `render.yaml` - Optimized build and start commands
- [x] `start.sh` - Production startup with `--env prod` flag
- [x] All files use `--env prod` to avoid memory issues

### 2. Push to GitHub
```bash
git add .
git commit -m "Fix Render deployment - use production mode to avoid memory issues"
git push origin experiment
```

### 3. Render Environment Variables (CRITICAL!)

Go to your Render dashboard → educhat service → Environment tab and set:

**Required Variables:**
```
DATABASE_URL=postgresql://postgres:[admin123]@db.yeqfvvekdwtawbpusluu.supabase.co:5432/postgres
SUPABASE_URL=https://yeqfvvekdwtawbpusluu.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllcWZ2dmVrZHd0YXdicHVzbHV1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjI1NDQ3OTcsImV4cCI6MjA3ODEyMDc5N30.KgMFbSwq0_BctdXn6JYwL297Ag9M1MLyFOoT7rJSpr8
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InllcWZ2dmVrZHd0YXdicHVzbHV1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MjU0NDc5NywiZXhwIjoyMDc4MTIwNzk3fQ.MtnnhwEDEUap_yiMO0pxRW0aSsMngFgW8qdFaDm1CFI
GOOGLE_AI_API_KEY=AIzaSyAdq6OhcBZaZ_G378foQBLwZ6NxtzXVf3M
```

**Auto-configured (already in render.yaml):**
- `PORT=10000` (Render sets this automatically)
- `RENDER=true` (Render sets this automatically)
- `PYTHON_VERSION=3.11`
- `APP_ENV=production`
- `DEBUG=False`

### 4. Deploy

**Option A: Automatic (Recommended)**
- Push to GitHub → Render auto-deploys

**Option B: Manual**
- Go to Render dashboard → educhat service
- Click "Manual Deploy" → Deploy latest commit

## Expected Deployment Flow

### Build Phase (~2-3 minutes)
```
Installing Python 3.11...
Installing dependencies from requirements.txt...
Running: reflex init
Initialized educhat.
Build complete!
```

### Start Phase (~1-2 minutes)
```
🚀 Starting EduChat on Render...
📋 Checking environment variables...
✅ Environment variables OK
🔌 Testing Supabase connection...
✅ Supabase connection successful
✅ Startup checks complete!
🌐 Starting Reflex application...
Port: 10000
Starting Reflex backend on 0.0.0.0:10000...
Compiling: ━━━━━━━━━━━━━━━━ 100%
Backend running at: http://0.0.0.0:10000
```

### Success Indicators
- ✅ "App available at https://educhat-dgxn.onrender.com"
- ✅ Logs show "Backend running at: http://0.0.0.0:10000"
- ✅ No "out of memory" errors
- ✅ No "no open ports detected" errors

## Troubleshooting

### Issue: "No open ports detected"
**Solution**: This was the main issue - now fixed with `--env prod` flag

**What to check**:
1. Logs show "Starting Reflex backend on 0.0.0.0:10000"
2. No "out of memory" or "heap" errors
3. Build phase completed successfully
4. All environment variables are set

### Issue: "Out of memory" or "JavaScript heap"
**Solution**: Should NOT happen anymore - we're using production mode

**If it still happens**:
1. Check that `start.sh` has `--env prod` flag
2. Verify `APP_ENV=production` is set in Render
3. Check that `NODE_OPTIONS="--max-old-space-size=512"` is in start.sh

### Issue: "Supabase connection failed"
**Solution**: Check environment variables

**Fix**:
1. Verify `SUPABASE_URL` is set correctly
2. Verify `SUPABASE_ANON_KEY` is set correctly
3. Check Supabase database is accessible

### Issue: Build succeeds but app crashes on startup
**Check**:
1. View logs in Render dashboard
2. Look for Python errors in startup script
3. Verify all required dependencies are in requirements.txt

## Monitoring

### View Logs
1. Go to Render dashboard → educhat service
2. Click "Logs" tab
3. Look for startup messages and errors

### Check Service Health
1. Visit: https://educhat-dgxn.onrender.com
2. Should show your EduChat app
3. Test chat functionality

### Performance
- First request may be slow (~10-30s on free tier due to cold start)
- Subsequent requests should be fast (<1s)
- Free tier spins down after 15 minutes of inactivity

## Post-Deployment

### Verify Everything Works
- [ ] App loads at https://educhat-dgxn.onrender.com
- [ ] Chat interface appears
- [ ] Can send messages
- [ ] AI responds correctly
- [ ] Onboarding page works
- [ ] Database queries work

### Optional: Upgrade Plan
If free tier is too slow or spins down too often:
- Upgrade to "Starter" plan ($7/month)
- Keeps app always running
- More RAM and CPU
- No cold starts

---

**Status**: Ready to deploy! 🚀

The memory issue is fixed by using production mode (`--env prod`) which compiles the frontend only once instead of on every request.
