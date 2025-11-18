# Supabase Integration Summary

## Overview
Complete integration of Supabase for authentication and chat history persistence with support for both logged-in and guest users.

---

## Database Schema

### Tables Created

#### 1. **conversations**
Stores user conversation metadata.

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    title VARCHAR NOT NULL DEFAULT 'New Conversation',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    archived BOOLEAN DEFAULT FALSE,
    metadata JSONB
);
```

**Indexes:**
- `idx_conversations_user_id` - Fast user lookup
- `idx_conversations_created_at` - Chronological ordering
- `idx_conversations_archived` - Filter active conversations

#### 2. **messages**
Stores individual chat messages.

```sql
CREATE TABLE messages (
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
```

**Indexes:**
- `idx_messages_conversation_id` - Fast conversation lookup
- `idx_messages_timestamp` - Chronological ordering
- `idx_messages_role` - Filter by role

---

## Row Level Security (RLS)

### Conversations Policies

1. **SELECT**: Users can view their own conversations
2. **INSERT**: Users can create conversations for themselves
3. **UPDATE**: Users can update their own conversations
4. **DELETE**: Users can delete their own conversations

### Messages Policies

1. **SELECT**: Users can view messages from their conversations
2. **INSERT**: Users can create messages in their conversations
3. **UPDATE**: Users can update messages in their conversations
4. **DELETE**: Users can delete messages in their conversations

All policies enforce user ownership through `auth.uid()`.

---

## Supabase Service Methods

### Chat History Methods (`educhat/services/supabase_client.py`)

#### Conversation Management

**`create_conversation(user_id, title)`**
- Creates new conversation for user
- Returns conversation data with UUID

**`get_user_conversations(user_id, include_archived, limit)`**
- Retrieves all user conversations
- Ordered by updated_at DESC
- Default limit: 100

**`get_conversation_by_id(conversation_id)`**
- Gets specific conversation
- Returns None if not found

**`update_conversation(conversation_id, title, archived)`**
- Updates conversation metadata
- Updates updated_at timestamp

**`delete_conversation(conversation_id)`**
- Deletes conversation and all messages (CASCADE)
- Returns True on success

**`get_conversation_count(user_id)`**
- Returns count of active conversations
- Used for enforcing limits

#### Message Management

**`save_message(conversation_id, role, content, ...)`**
- Saves message to conversation
- Supports feedback, streaming status, errors
- Auto-updates conversation timestamp

**`get_conversation_messages(conversation_id, limit, offset)`**
- Retrieves messages for conversation
- Ordered by timestamp ASC
- Supports pagination

**`update_message_feedback(message_id, feedback)`**
- Updates message feedback (like/dislike)
- Records feedback timestamp

---

## Application Integration

### AppState Updates (`educhat/state/app_state.py`)

#### New Methods

**`save_conversation_to_db()`**
- Saves current conversation and messages
- Only for logged-in users
- Auto-creates conversation if needed
- Syncs messages with database

**`load_conversations_from_db()`**
- Loads user's conversation history
- Converts to app format
- Only for logged-in users

**`load_conversation_messages(conversation_id)`**
- Loads specific conversation messages
- Converts timestamps to display format
- Updates local state

**`create_new_conversation()` [UPDATED]**
- Now async
- Creates in database for logged-in users
- Enforces conversation limits
- Handles guest vs logged-in logic

**`load_conversation(conversation_id)` [UPDATED]**
- Now async
- Loads messages from database
- Handles guest vs logged-in logic

**`delete_conversation(conversation_id)` [UPDATED]**
- Now async
- Deletes from database
- Updates local state

**`archive_conversation(conversation_id)` [UPDATED]**
- Now async
- Archives in database
- Filters from UI

#### Permission Methods

**`can_save_conversations()`**
- Returns True for logged-in users only
- False for guests

**`can_access_history()`**
- Returns True for logged-in users only
- False for guests

**`get_max_conversations()`**
- Returns 1 for guests
- Returns 100 for logged-in users

**`is_at_conversation_limit()`**
- Checks if user reached limit
- Different limits for guest/logged-in

#### Message Handling Updates

**`send_message()` [UPDATED]**
- Auto-saves to database after AI response
- Only for logged-in users
- Handles conversation creation

---

## Authentication Integration

### AuthState Updates (`educhat/state/auth_state.py`)

**`login()` [UPDATED]**
- Loads conversations after successful login
- Uses `yield` for redirect in async generator

**`signup()` [UPDATED]**
- Loads conversations (empty for new users)
- Uses `yield` for redirect

**`logout()` [UPDATED]**
- Clears all user data
- Uses `yield` for redirect

**`continue_as_guest()` [UPDATED]**
- Non-async (no DB operations)
- Immediate redirect

---

## Data Flow

### Login Flow
```
1. User enters credentials
2. AuthService validates with Supabase Auth
3. On success:
   - Set user_id, email, name
   - Load conversations from DB
   - Redirect to /chat
4. On failure:
   - Show error message
```

### New Message Flow (Logged-in User)
```
1. User sends message
2. Add to local state
3. Stream AI response
4. Update local state with chunks
5. Mark streaming complete
6. Save to database:
   - Create conversation if needed
   - Save user message
   - Save assistant message
7. Update conversation timestamp
```

### New Message Flow (Guest)
```
1. User sends message
2. Add to local state
3. Stream AI response
4. Update local state with chunks
5. Mark streaming complete
6. Skip database save
7. Data only in memory
```

### Load Conversation Flow
```
1. User clicks conversation in sidebar
2. Set current_conversation_id
3. If logged-in:
   - Load messages from DB
   - Convert to app format
   - Update local state
4. If guest:
   - Clear messages (no history)
```

---

## User Types Comparison

| Feature | Guest User | Logged-in User |
|---------|-----------|----------------|
| **Authentication** | None | Supabase Auth |
| **Max Conversations** | 1 | 100 |
| **History Persistence** | ❌ No | ✅ Yes |
| **Database Saves** | ❌ No | ✅ Yes |
| **Conversation Load** | ❌ No | ✅ Yes |
| **Session Restore** | ❌ No | ✅ Yes (future) |
| **Cross-device Sync** | ❌ No | ✅ Yes |
| **Data Export** | ❌ No | ✅ Yes (future) |

---

## Error Handling

### Database Errors
- Wrapped in try-except blocks
- Errors logged to console
- Graceful degradation
- User can continue using app

### Authentication Errors
- Clear error messages
- Form validation
- No data loss
- Retry capability

### Network Errors
- Timeout handling
- Error message display
- Retry mechanisms
- Offline detection (future)

---

## Performance Optimizations

### Database Queries
1. **Indexes** on frequently queried columns
2. **Pagination** support for messages
3. **Limited queries** (default 100 conversations)
4. **Selective loading** (messages only when needed)

### State Management
1. **Lazy loading** of conversations
2. **Incremental sync** of messages
3. **Local caching** in state
4. **Batch updates** where possible

### Network
1. **Streaming responses** for AI
2. **Async operations** throughout
3. **Non-blocking UI** updates
4. **Optimistic updates** (local first)

---

## Security Features

### Authentication
- Supabase Auth with JWT tokens
- Secure password hashing
- Session management
- Auto token refresh (Supabase handles)

### Authorization
- Row Level Security (RLS)
- User can only access own data
- Enforced at database level
- No data leakage between users

### Data Protection
- HTTPS for all requests
- No sensitive data in logs
- Parameterized queries
- SQL injection prevention

---

## Migration Steps

### 1. Database Setup
```bash
# In Supabase SQL Editor
# Execute: prisma/migration_chat_history.sql
```

### 2. Environment Variables
```env
SUPABASE_URL=your_url
SUPABASE_ANON_KEY=your_key
SUPABASE_SERVICE_ROLE_KEY=your_key
```

### 3. Test Connection
```python
from educhat.services.supabase_client import get_client
client = get_client()
# Should connect without errors
```

---

## Future Enhancements

### Short Term
1. **Session Persistence** - localStorage/cookies
2. **Message Search** - Full-text search in DB
3. **Conversation Folders** - Organize conversations
4. **Export Conversations** - Download as JSON/PDF

### Medium Term
1. **Real-time Sync** - Supabase Realtime
2. **Collaboration** - Share conversations
3. **Message Editing** - Edit/delete messages
4. **Advanced Search** - Filters, date ranges

### Long Term
1. **Analytics Dashboard** - Usage statistics
2. **AI Training** - Use feedback for improvement
3. **Custom Models** - Per-user AI preferences
4. **Multi-modal** - Images, files, voice

---

## Monitoring & Maintenance

### Database Metrics to Monitor
- Table sizes (conversations, messages)
- Query performance
- Index usage
- Connection pool usage

### Application Metrics
- User registration rate
- Active users
- Messages per conversation
- Average conversation length

### Maintenance Tasks
- Regular backups
- Index optimization
- Old data archival
- Performance tuning

---

## Troubleshooting

### Common Issues

**1. "User can't see their conversations"**
- Check RLS policies enabled
- Verify user_id matches auth.uid()
- Check user is logged in (not guest)

**2. "Messages not saving"**
- Check conversation exists first
- Verify user permissions
- Check database logs
- Ensure user is logged in

**3. "Slow conversation loading"**
- Check indexes exist
- Monitor query performance
- Consider pagination
- Check network latency

**4. "Authentication fails"**
- Verify Supabase keys
- Check Auth settings
- Verify email confirmation settings
- Check error messages

---

## Files Modified/Created

### Created
- `educhat/services/auth_service.py` - Authentication service
- `educhat/state/auth_state.py` - Auth state management
- `educhat/components/auth/auth_modal.py` - Login/signup UI
- `educhat/pages/landing.py` - Landing page
- `educhat/utils/auth_guards.py` - Route protection
- `prisma/migration_chat_history.sql` - Database schema
- `Documents/authentication-system.md` - Auth documentation
- `Documents/testing-guide.md` - Testing procedures

### Modified
- `educhat/state/app_state.py` - Added DB integration
- `educhat/services/supabase_client.py` - Added chat methods
- `educhat/educhat.py` - Added landing route
- `educhat/pages/index.py` - Added auth checks
- `educhat/components/chat/sidebar.py` - Added logout
- `prisma/create_tables.sql` - Updated schema

---

## Deployment Checklist

- [ ] Run database migration
- [ ] Set environment variables
- [ ] Test authentication flow
- [ ] Test guest user flow
- [ ] Test chat persistence
- [ ] Verify RLS policies
- [ ] Test on production Supabase
- [ ] Monitor error logs
- [ ] Set up backups
- [ ] Document for team

---

## Support & Resources

- **Supabase Docs**: https://supabase.com/docs
- **Reflex Docs**: https://reflex.dev/docs
- **Project Repo**: Your repository
- **Issues**: Report in GitHub Issues
