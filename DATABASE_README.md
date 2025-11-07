# 🗄️ EduChat Database with Supabase + Prisma

This directory contains the complete database implementation for EduChat using **Supabase** (PostgreSQL) and **Prisma ORM**.

## 📁 Structure

```
prisma/
├── schema.prisma          # Database schema definition
└── rls_policies.sql       # Row-Level Security policies

educhat/services/
└── supabase.py            # Service layer with CRUD operations

tests/
└── test_supabase.py       # Comprehensive test suite

Documents/
├── SUPABASE_SETUP.md      # Detailed setup guide
├── SUPABASE_QUICKREF.md   # Quick reference
└── SUPABASE_IMPLEMENTATION.md  # Implementation summary
```

## 🚀 Quick Setup

### 1. Prerequisites
```powershell
# Install Node.js (for Prisma CLI)
# Download from: https://nodejs.org/

# Install Prisma globally
npm install -g prisma
```

### 2. Install Dependencies
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Python packages
pip install -r requirements.txt
```

### 3. Configure Supabase
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Get connection string from **Settings → Database**
4. Update `.env`:
```bash
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
```

### 4. Initialize Database
```powershell
# Run automated setup
python manage_db.py setup

# Apply RLS policies manually in Supabase Dashboard:
# 1. Go to SQL Editor
# 2. Copy content from prisma/rls_policies.sql
# 3. Paste and Run
```

### 5. Seed Sample Data
```powershell
python manage_db.py seed
```

### 6. Verify
```powershell
# Test connection
python manage_db.py test

# Run test suite
pytest tests/test_supabase.py -v
```

## 📊 Database Schema

### Tables Overview

| Table | Purpose | Access |
|-------|---------|--------|
| institutions | Educational institutions | Public read |
| studies | Study programs | Public read |
| events | Important dates | Public read |
| users | User accounts | Private (own data) |
| sessions | Chat sessions | Private (own data) |
| messages | Chat messages | Private (own data) |
| onboarding | User onboarding | Private (own data) |
| onboarding_questions | Quiz questions | Public read |
| onboarding_answers | Quiz answers | Private (own data) |
| reminders | User reminders | Private (own data) |

### Relationships
- institutions → studies (one-to-many)
- institutions → events (one-to-many)
- users → sessions (one-to-many)
- users → reminders (one-to-many)
- sessions → messages (one-to-many)
- sessions → onboarding (one-to-many)
- events → reminders (one-to-many)

## 💻 Usage Examples

### Using the Service Layer
```python
from educhat.services.supabase import SupabaseService

# Initialize service
service = SupabaseService()

# Search institutions
institutions = await service.search_institutions("Universiteit")

# Create session
session = await service.create_session(user_id="...")

# Send message
message = await service.create_message(
    session_id=session.id,
    role="user",
    content="Welke opleidingen zijn er?"
)

# Get AI response and save
response = await service.create_message(
    session_id=session.id,
    role="assistant",
    content="Hier zijn de beschikbare opleidingen...",
    metadata={"response_time": 1.5}
)
```

### Direct Prisma Usage
```python
from educhat.services.supabase import get_db

db = await get_db()

# Complex queries
studies = await db.study.find_many(
    where={
        'type': 'Bachelor',
        'institution': {
            'location': 'Paramaribo'
        }
    },
    include={'institution': True},
    order={'title': 'asc'}
)
```

## 🔧 Management Commands

```powershell
python manage_db.py setup      # Initial setup
python manage_db.py test       # Test connection
python manage_db.py seed       # Seed sample data
python manage_db.py migrate    # Create migration
python manage_db.py studio     # Visual DB editor
python manage_db.py reset      # Reset database (⚠️ destructive!)
```

## 🔒 Security

### Row-Level Security (RLS)
- ✅ Enabled on all tables
- ✅ Public read for knowledge base
- ✅ User-specific access for private data
- ✅ Service role bypass for backend

### Performance Optimization
- ✅ GIN indexes for full-text search
- ✅ Composite indexes for common queries
- ✅ Connection pooling via Prisma
- ✅ Async operations throughout

## 📚 Service Methods

### Complete API

**Institutions**
- `get_all_institutions()`, `get_institution_by_id()`, `search_institutions()`, `create_institution()`

**Studies**
- `get_studies_by_institution()`, `search_studies()`, `create_study()`

**Events**
- `get_upcoming_events()`, `create_event()`

**Users**
- `create_user()`, `get_user_by_email()`, `get_user_by_id()`

**Sessions**
- `create_session()`, `get_session_by_id()`, `get_user_sessions()`, `update_session_activity()`

**Messages**
- `create_message()`, `get_session_messages()`, `update_message_feedback()`

**Onboarding**
- `create_onboarding()`, `get_onboarding_by_session()`, `update_onboarding()`, `get_onboarding_questions()`, `save_onboarding_answer()`

**Reminders**
- `create_reminder()`, `get_user_reminders()`, `get_pending_reminders()`, `mark_reminder_sent()`

## 🧪 Testing

```powershell
# Run all tests
pytest tests/test_supabase.py -v

# Run specific test class
pytest tests/test_supabase.py::TestInstitutions -v

# Run with coverage
pytest tests/test_supabase.py --cov=educhat.services.supabase
```

## 📖 Documentation

- **Setup Guide**: `Documents/SUPABASE_SETUP.md` - Complete setup instructions
- **Quick Reference**: `Documents/SUPABASE_QUICKREF.md` - Quick lookup
- **Implementation**: `Documents/SUPABASE_IMPLEMENTATION.md` - Technical details

## 🐛 Troubleshooting

### "prisma not found"
```powershell
npm install -g prisma
```

### "Cannot connect to database"
- Check DATABASE_URL in `.env`
- Verify Supabase project is running
- Test connection: `python manage_db.py test`

### Import errors for prisma.models
```powershell
prisma generate
```

### Table does not exist
```powershell
prisma db push
```

## 🔗 Resources

- **Prisma Python Docs**: https://prisma-client-py.readthedocs.io/
- **Supabase Docs**: https://supabase.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## ✅ Checklist

- [x] Prisma schema created
- [x] Service layer implemented
- [x] RLS policies defined
- [x] Tests written
- [x] Documentation complete
- [ ] Supabase project created (you do this)
- [ ] Database initialized (run `python manage_db.py setup`)
- [ ] RLS policies applied (via Supabase SQL Editor)
- [ ] Tests passing (run `pytest`)

---

**Ready to integrate with Reflex!** 🎉

See service methods in `educhat/services/supabase.py` and integration examples in documentation.
