# EduChat Testing Guide

## Prerequisites

### 1. Environment Setup
Ensure you have the following environment variables set in `.env`:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

### 2. Database Setup
Run the migration SQL in your Supabase SQL Editor:
1. Open Supabase Dashboard → SQL Editor
2. Execute `prisma/migration_chat_history.sql`
3. Verify tables created: `conversations`, `messages`
4. Check RLS policies are enabled

### 3. Start Application
```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Run Reflex app
reflex run
```

---

## Test Scenarios

### Test 1: Guest User Flow
**Objective:** Verify guest users can use chat with limited features

#### Steps:
1. Navigate to `http://localhost:3000/`
2. Click "Continue as Guest"
3. Verify redirected to `/chat`
4. Verify guest banner appears at top
5. Send a test message: "What is EduChat?"
6. Verify AI responds
7. Try to create a new conversation
8. Verify only 1 conversation allowed (guest limit)
9. Check sidebar shows "Guest" badge
10. Refresh page - verify conversation NOT persisted

**Expected Results:**
- ✅ Guest can access chat immediately
- ✅ Guest banner visible
- ✅ Limited to 1 conversation
- ✅ No data persistence
- ✅ Sidebar shows guest status

---

### Test 2: User Signup Flow
**Objective:** Verify new users can create accounts

#### Steps:
1. Navigate to `http://localhost:3000/`
2. Click "Get Started"
3. Switch to "Sign Up" tab
4. Fill form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Password: "password123"
   - Confirm: "password123"
5. Click "Create Account"
6. Verify redirected to `/chat`
7. Verify no guest banner
8. Check sidebar shows user name and email
9. Send a message: "Hello EduChat"
10. Verify message saved

**Expected Results:**
- ✅ Signup form validates correctly
- ✅ Account created in Supabase Auth
- ✅ User redirected to chat
- ✅ User info displays in sidebar
- ✅ No conversation limit message

---

### Test 3: User Login Flow
**Objective:** Verify existing users can log in

#### Steps:
1. Log out if logged in
2. Navigate to `http://localhost:3000/`
3. Click "Get Started"
4. Stay on "Login" tab
5. Enter credentials from Test 2
6. Click "Login"
7. Verify redirected to `/chat`
8. Verify previous conversations loaded
9. Click on previous conversation
10. Verify messages loaded

**Expected Results:**
- ✅ Login successful
- ✅ User conversations restored
- ✅ Messages loaded correctly
- ✅ User info shows in sidebar

---

### Test 4: Chat History Persistence
**Objective:** Verify conversations save to database

#### Steps:
1. Log in as test user
2. Create new conversation
3. Send message: "What is machine learning?"
4. Wait for AI response
5. Check Supabase Dashboard → Table Editor → conversations
6. Verify new row with conversation
7. Check messages table
8. Verify 2 rows (user + assistant)
9. Refresh browser
10. Verify conversation still exists
11. Click conversation
12. Verify messages load

**Expected Results:**
- ✅ Conversation in database
- ✅ Messages in database
- ✅ Data persists after refresh
- ✅ Messages load correctly

---

### Test 5: Multiple Conversations
**Objective:** Verify users can manage multiple conversations

#### Steps:
1. Log in as test user
2. Create conversation 1: "Tell me about Python"
3. Wait for response
4. Create conversation 2: "What is JavaScript?"
5. Wait for response
6. Create conversation 3: "Explain databases"
7. Verify all 3 in sidebar
8. Click conversation 1
9. Verify correct messages load
10. Click conversation 2
11. Verify correct messages load

**Expected Results:**
- ✅ Multiple conversations created
- ✅ All visible in sidebar
- ✅ Clicking loads correct messages
- ✅ Conversations stay separate

---

### Test 6: Conversation Management
**Objective:** Test delete and archive features

#### Steps:
1. Log in with multiple conversations
2. Hover over a conversation
3. Click archive icon
4. Verify conversation removed from list
5. Check database - archived flag = true
6. Hover over another conversation
7. Click delete icon
8. Verify conversation removed
9. Check database - conversation deleted
10. Verify messages also deleted (CASCADE)

**Expected Results:**
- ✅ Archive sets flag in database
- ✅ Delete removes from database
- ✅ Messages deleted with conversation
- ✅ UI updates immediately

---

### Test 7: Logout Flow
**Objective:** Verify logout clears session

#### Steps:
1. Log in as test user
2. Send a few messages
3. Click "Logout" in sidebar
4. Verify redirected to landing page
5. Try navigating to `/chat`
6. Verify redirected back to `/`
7. Log in again
8. Verify conversations still exist

**Expected Results:**
- ✅ Logout clears session
- ✅ Redirects to landing
- ✅ Chat protected when logged out
- ✅ Data persists in database

---

### Test 8: Guest to User Conversion
**Objective:** Verify guest can upgrade to full account

#### Steps:
1. Start as guest
2. Send a test message
3. Click "Sign up" in guest banner
4. Complete signup form
5. Verify account created
6. Note: Guest conversation NOT transferred (expected)
7. Verify new user has empty history
8. Send new message
9. Verify it saves to database

**Expected Results:**
- ✅ Guest can access signup
- ✅ Account created successfully
- ✅ Guest data not transferred (by design)
- ✅ New messages save correctly

---

### Test 9: Concurrent Sessions
**Objective:** Test same user in multiple browsers

#### Steps:
1. Log in on Browser 1
2. Create conversation A
3. Send message in conversation A
4. Open Browser 2 (incognito)
5. Log in with same credentials
6. Verify conversation A appears
7. Create conversation B in Browser 2
8. Send message in conversation B
9. Refresh Browser 1
10. Verify conversation B appears

**Expected Results:**
- ✅ Changes sync via database
- ✅ Both browsers see all conversations
- ✅ No data conflicts
- ✅ Proper user isolation

---

### Test 10: Error Handling
**Objective:** Test error scenarios

#### Steps:
1. **Invalid Login:**
   - Try login with wrong password
   - Verify error message shows
   - Verify no redirect

2. **Signup Validation:**
   - Try passwords that don't match
   - Verify error message
   - Try short password (< 8 chars)
   - Verify error message

3. **Database Offline:**
   - Stop Supabase (or use invalid URL)
   - Try to send message
   - Verify graceful error handling
   - Verify app doesn't crash

4. **Network Timeout:**
   - Send very long message
   - Verify timeout handling
   - Verify error message displayed

**Expected Results:**
- ✅ Clear error messages
- ✅ No app crashes
- ✅ User can retry actions
- ✅ Graceful degradation

---

## Database Verification Queries

### Check Users
```sql
SELECT id, email, created_at 
FROM auth.users 
ORDER BY created_at DESC;
```

### Check Conversations
```sql
SELECT c.id, c.title, c.created_at, u.email 
FROM conversations c
JOIN auth.users u ON c.user_id = u.id
ORDER BY c.created_at DESC;
```

### Check Messages
```sql
SELECT m.id, m.role, LEFT(m.content, 50) as content_preview, m.timestamp, c.title
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
ORDER BY m.timestamp DESC
LIMIT 20;
```

### Check Conversation Count by User
```sql
SELECT u.email, COUNT(c.id) as conversation_count
FROM auth.users u
LEFT JOIN conversations c ON u.id = c.user_id AND c.archived = false
GROUP BY u.email
ORDER BY conversation_count DESC;
```

---

## Performance Testing

### Test Large Conversation
1. Create conversation with 50+ messages
2. Verify load time < 2 seconds
3. Check pagination if implemented
4. Verify scrolling is smooth

### Test Many Conversations
1. Create 20+ conversations
2. Verify sidebar scrolls properly
3. Check load time for conversation list
4. Verify search/filter works

---

## Security Testing

### Test RLS Policies
1. Log in as User A
2. Create conversation
3. Note conversation ID
4. Log out
5. Log in as User B
6. Try to access User A's conversation directly
7. Verify access denied

### Test Authentication
1. Try accessing `/chat` without auth
2. Verify redirect to landing
3. Try API calls without token
4. Verify rejected

---

## Mobile Testing

### Responsive Design
1. Open on mobile device
2. Verify landing page displays correctly
3. Test auth modal on mobile
4. Verify chat interface adapts
5. Test sidebar toggle
6. Verify all buttons accessible

---

## Browser Compatibility

Test on:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

---

## Cleanup After Testing

```sql
-- Delete test conversations
DELETE FROM conversations WHERE user_id IN (
  SELECT id FROM auth.users WHERE email LIKE '%test%'
);

-- Delete test users (be careful!)
-- Do this in Supabase Auth dashboard instead
```

---

## Known Limitations

1. **Guest Conversations:** Not persisted between sessions (by design)
2. **Session Storage:** Not yet implemented (cookies/localStorage)
3. **Password Reset:** UI not yet implemented
4. **Profile Editing:** Not yet implemented
5. **Message Search:** Not yet implemented

---

## Bug Reporting

If you find issues, report with:
- Steps to reproduce
- Expected vs actual behavior
- Browser and OS
- Screenshots if applicable
- Console errors
