# 🚀 Quick Start Guide - EduChat with Supabase

## Step 1: Database Setup (⏱️ 5 minutes)

### Option A: Supabase Dashboard
1. Open your Supabase project: https://supabase.com/dashboard
2. Go to **SQL Editor**
3. Click **New Query**
4. Copy contents from `prisma/migration_chat_history.sql`
5. Paste and click **Run**
6. ✅ Verify tables created: **Table Editor** → See `conversations` and `messages`

### Option B: Command Line
```bash
# If you have Supabase CLI installed
supabase db push
```

---

## Step 2: Environment Check (⏱️ 2 minutes)

Verify your `.env` file has:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
```

**Get your keys:**
- Supabase Dashboard → Settings → API
- Copy `Project URL` and `anon/public` key
- Copy `service_role` key (⚠️ keep secret!)

---

## Step 3: Start the App (⏱️ 1 minute)

```powershell
# In PowerShell terminal
cd D:\EduChat

# Activate virtual environment
.venv\Scripts\Activate.ps1

# Start Reflex
reflex run
```

**Expected output:**
```
App running at:
  http://localhost:3000/
```

---

## Step 4: Test Guest Flow (⏱️ 2 minutes)

1. Open browser: `http://localhost:3000/`
2. Click **"Continue as Guest"**
3. You should see:
   - ✅ Redirected to `/chat`
   - ✅ Blue banner: "You're using EduChat as a guest"
   - ✅ Sidebar shows "Guest" badge
4. Send a message: **"Hello, EduChat!"**
5. Wait for AI response
6. Try creating new conversation → Should be blocked (limit: 1)
7. **Refresh page** → Conversation should be GONE (not persisted)

**✅ If all works: Guest mode is working!**

---

## Step 5: Test Signup (⏱️ 3 minutes)

1. Click **"Sign up"** in the guest banner (or go to landing)
2. Fill form:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm: `password123`
3. Click **"Create Account"**
4. You should see:
   - ✅ Redirected to `/chat`
   - ✅ No guest banner
   - ✅ Sidebar shows your name and email
   - ✅ Empty conversation list
5. Send a message: **"What is Python?"**
6. Wait for AI response
7. **Refresh page** → Message should STILL BE THERE!

**✅ If messages persist: Signup and persistence working!**

---

## Step 6: Test Database (⏱️ 2 minutes)

### In Supabase Dashboard:

**Check Conversations:**
1. Go to **Table Editor** → `conversations`
2. You should see 1 row:
   - Your conversation
   - Your user_id
   - Title: "What is Python?"

**Check Messages:**
1. Go to **Table Editor** → `messages`
2. You should see 2 rows:
   - Your message (role: `user`)
   - AI response (role: `assistant`)

**✅ If data is there: Database integration working!**

---

## Step 7: Test Multiple Conversations (⏱️ 3 minutes)

1. Click **"Nieuw gesprek"** (New conversation)
2. Send: **"Explain JavaScript"**
3. Wait for response
4. Create another: **"What is AI?"**
5. Wait for response
6. Check sidebar → Should show 3 conversations
7. Click on first conversation
8. Verify correct messages load
9. **Refresh page** → All 3 should still be there

**✅ If all conversations work: Multi-conversation working!**

---

## Step 8: Test Logout (⏱️ 1 minute)

1. In sidebar, click **"Logout"**
2. You should:
   - ✅ Be redirected to landing page
   - ✅ Session cleared
3. Try going to `http://localhost:3000/chat`
4. Should redirect back to landing
5. Click **"Get Started"** → Login with same credentials
6. All conversations should be back!

**✅ If logout/login works: Authentication complete!**

---

## Step 9: Test Delete/Archive (⏱️ 2 minutes)

1. Log in if not already
2. Hover over a conversation in sidebar
3. Two icons should appear:
   - Archive icon (box)
   - Delete icon (trash)
4. Click **archive** on one conversation
5. It should disappear from list
6. In Supabase → Check `conversations` → `archived` should be `true`
7. Click **delete** on another conversation
8. It should disappear
9. In Supabase → Check `conversations` → Should be deleted
10. Check `messages` → Associated messages should be deleted too

**✅ If delete/archive works: CRUD operations complete!**

---

## Common Issues & Fixes

### ❌ "Module not found"
```bash
pip install -r requirements.txt
```

### ❌ "Supabase connection failed"
- Check `.env` has correct URLs and keys
- Verify Supabase project is active
- Check firewall/network settings

### ❌ "Table doesn't exist"
- Run migration SQL in Supabase SQL Editor
- Check Tables were created
- Verify RLS policies enabled

### ❌ "Can't save messages"
- Check user is logged in (not guest)
- Verify conversation exists
- Check browser console for errors
- Check Supabase logs

### ❌ "Login fails"
- Check email confirmation settings in Supabase
- Verify Auth is enabled
- Check password requirements
- See error message in UI

---

## Success Checklist

Before considering this complete, verify:

- [ ] Database tables created
- [ ] Environment variables set
- [ ] App starts without errors
- [ ] Guest mode works
- [ ] Signup creates account
- [ ] Login authenticates
- [ ] Messages persist after refresh
- [ ] Multiple conversations work
- [ ] Conversations load correctly
- [ ] Delete removes from DB
- [ ] Archive sets flag
- [ ] Logout clears session
- [ ] Data visible in Supabase

---

## Next Steps

### For Development:
1. Test all flows thoroughly
2. Try edge cases (bad passwords, long messages, etc.)
3. Check performance with many conversations
4. Test on different browsers
5. Test mobile responsive

### For Production:
1. Change to production Supabase project
2. Update environment variables
3. Enable email verification
4. Set up monitoring
5. Configure backups
6. Set up error tracking (Sentry, etc.)

---

## Get Help

### Check Logs:
- **Browser Console**: F12 → Console
- **Terminal**: Where `reflex run` is running
- **Supabase Logs**: Dashboard → Logs

### Documentation:
- `Documents/testing-guide.md` - Full test scenarios
- `Documents/supabase-integration.md` - Technical details
- `Documents/authentication-system.md` - Auth architecture

### Debug Commands:
```python
# Test Supabase connection
python -c "from educhat.services.supabase_client import get_client; print(get_client())"

# Check user conversations
python -c "from educhat.services.supabase_client import get_service; print(get_service().get_user_conversations('user-id-here'))"
```

---

## Time Estimate

**Total setup time: 15-20 minutes**
- Database: 5 min
- Environment: 2 min
- App start: 1 min
- Testing: 10-15 min

---

## 🎉 Success!

If all steps passed, you have a fully functional EduChat with:
- ✅ Authentication system
- ✅ Guest and user modes
- ✅ Persistent chat history
- ✅ Supabase integration
- ✅ Secure data isolation

**Ready for production! 🚀**
