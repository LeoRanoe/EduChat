# 📊 EduChat Database Functionaliteiten - Volledig Overzicht

## ✅ Status: Alle functionaliteiten gebruiken de database!

Deze applicatie is **volledig geïntegreerd** met Supabase PostgreSQL database. Alle belangrijke functionaliteiten slaan data op en halen data op uit de database.

---

## 🗄️ Database Architectuur

### Database Provider
- **Supabase** (PostgreSQL)
- Locatie: `educhat/services/supabase_client.py`
- Configuratie: `.env` bestand

### Verbinding
```python
from educhat.services.supabase_client import get_client, get_service

# Get database client
client = get_client()

# Get service instance with helper methods
db = get_service()
```

---

## 📋 Database Tabellen

### 1. **Institutions** (Onderwijsinstellingen)
```sql
- id (UUID)
- name (VARCHAR)
- short_name (VARCHAR)
- description (TEXT)
- location (VARCHAR)
- website (VARCHAR)
- contact (JSONB)
- enrollment_process (TEXT)
- last_updated (TIMESTAMP)
```

**Functionaliteiten:**
- ✅ Alle instellingen ophalen: `db.get_all_institutions()`
- ✅ Instelling zoeken op ID: `db.get_institution_by_id(institution_id)`
- ✅ Instellingen zoeken op naam: `db.search_institutions(query)`
- ✅ Nieuwe instelling aanmaken: `db.create_institution(data)`

**Gebruikt in:**
- AI Service voor context bij vragen over instellingen
- Education Service voor zoekfunctionaliteit
- Onboarding voor instelling-suggesties

---

### 2. **Studies** (Opleidingen)
```sql
- id (UUID)
- institution_id (UUID, FK -> institutions)
- title (VARCHAR)
- faculty (VARCHAR)
- description (TEXT)
- type (VARCHAR)
- duration (INTEGER)
- admission (TEXT)
- career_opportunities (TEXT)
- keywords (TEXT)
- source (VARCHAR)
- last_updated (TIMESTAMP)
```

**Functionaliteiten:**
- ✅ Studies per instelling: `db.get_studies_by_institution(institution_id)`
- ✅ Studies zoeken: `db.search_studies(query, study_type, institution_id)`
- ✅ Nieuwe opleiding aanmaken: `db.create_study(data)`

**Gebruikt in:**
- AI Service voor context bij vragen over opleidingen
- Education Service voor studie-vergelijking
- Onboarding voor study-path suggesties

---

### 3. **Events** (Evenementen & Deadlines)
```sql
- id (UUID)
- institution_id (UUID, FK -> institutions)
- title (VARCHAR)
- type (VARCHAR)
- date (TIMESTAMP)
- description (TEXT)
- source (VARCHAR)
- last_updated (TIMESTAMP)
```

**Functionaliteiten:**
- ✅ Aankomende events: `db.get_upcoming_events(limit=10)`
- ✅ Nieuw event aanmaken: `db.create_event(data)`

**Gebruikt in:**
- Events Panel (zijpaneel met aankomende evenementen)
- AuthState: `load_upcoming_events()` functie
- Herinneringen aanmaken vanuit events

---

### 4. **Conversations** (Chat Geschiedenis)
```sql
- id (UUID)
- user_id (UUID, FK -> auth.users)
- title (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- archived (BOOLEAN)
- metadata (JSONB)
```

**Functionaliteiten:**
- ✅ Nieuwe conversatie: `db.create_conversation(user_id, title)`
- ✅ Conversaties van user: `db.get_user_conversations(user_id, include_archived, limit)`
- ✅ Specifieke conversatie: `db.get_conversation_by_id(conversation_id)`
- ✅ Conversatie updaten: `db.update_conversation(conversation_id, title, archived)`
- ✅ Conversatie verwijderen: `db.delete_conversation(conversation_id)`
- ✅ Aantal conversaties: `db.get_conversation_count(user_id)`

**Gebruikt in:**
- AppState: 
  - `save_conversation_to_db()` - Slaat huidige chat op
  - `load_conversations_from_db()` - Laadt alle conversaties
  - `load_conversation_messages()` - Laadt berichten van een conversatie
  - `archive_conversation()` - Archiveert een conversatie
  - `delete_conversation()` - Verwijdert een conversatie
- Sidebar component - Toont alle conversaties
- Chat persistentie voor ingelogde gebruikers

---

### 5. **Messages** (Chat Berichten)
```sql
- id (UUID)
- conversation_id (UUID, FK -> conversations)
- role (VARCHAR: 'user' | 'assistant')
- content (TEXT)
- timestamp (TIMESTAMP)
- feedback (VARCHAR: 'like' | 'dislike')
- feedback_timestamp (TIMESTAMP)
- is_streaming (BOOLEAN)
- is_error (BOOLEAN)
- metadata (JSONB)
```

**Functionaliteiten:**
- ✅ Bericht opslaan: `db.save_message(conversation_id, role, content, feedback, ...)`
- ✅ Berichten ophalen: `db.get_conversation_messages(conversation_id, limit, offset)`
- ✅ Feedback updaten: `db.update_message_feedback(message_id, feedback)`

**Gebruikt in:**
- AppState:
  - `save_conversation_to_db()` - Slaat alle berichten op
  - `load_conversation_messages()` - Laadt berichten
  - `handle_message_feedback()` - Slaat likes/dislikes op
- Chat interface voor persistente berichten

---

### 6. **Onboarding** (Gebruikers Quiz)
```sql
- id (UUID)
- user_id (UUID, FK -> auth.users)
- completed (BOOLEAN)
- completed_at (TIMESTAMP)
- current_step (INTEGER)
- answers (JSONB)
- interests (JSONB)
- skills (JSONB)
- goals (JSONB)
- personality (VARCHAR)
- quiz_results (JSONB)
- suggested_paths (JSONB)
- feedback (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

**Functionaliteiten:**
- ✅ Onboarding aanmaken: `db.create_onboarding(user_id)`
- ✅ Onboarding updaten: `db.update_onboarding(onboarding_id, data)`
- ✅ Vragen ophalen: `db.get_onboarding_questions(active_only)`
- ✅ Antwoord opslaan: `db.save_onboarding_answer(onboarding_id, question_id, selected_option)`

**Gebruikt in:**
- OnboardingState:
  - `complete_quiz()` - Slaat quiz resultaten op
  - `load_user_preferences(user_id)` - Laadt opgeslagen voorkeuren
  - `get_user_context()` - Context voor AI personalisatie
- AppState:
  - `load_onboarding_preferences()` - Laadt voorkeuren bij chat init
  - `get_ai_context_string()` - Voegt context toe aan AI prompts

---

### 7. **Reminders** (Herinneringen)
```sql
- id (UUID)
- user_id (UUID, FK -> auth.users)
- event_id (UUID, FK -> events)
- title (VARCHAR)
- date (TIMESTAMP)
- sent (BOOLEAN)
- created_at (TIMESTAMP)
```

**Functionaliteiten:**
- ✅ Herinnering aanmaken: `db.create_reminder(user_id, title, date, event_id)`
- ✅ Herinneringen ophalen: `db.get_user_reminders(user_id, include_sent)`
- ✅ Pending herinneringen: `db.get_pending_reminders(before_date)`
- ✅ Markeren als verzonden: `db.mark_reminder_sent(reminder_id)`

**Gebruikt in:**
- AuthState:
  - `create_reminder()` - Maakt nieuwe herinnering
  - `create_reminder_from_event()` - Maakt herinnering vanuit event
  - `load_reminders_from_db()` - Laadt alle herinneringen
  - `delete_reminder()` - Verwijdert herinnering
- Reminders Modal component

---

## 🔐 Authenticatie (Supabase Auth)

### Gebruikt Supabase Auth Service
Locatie: `educhat/services/auth_service.py`

**Functionaliteiten:**
- ✅ Registratie: `auth_service.signup(email, password, name)`
- ✅ Login: `auth_service.login(email, password)`
- ✅ Logout: `auth_service.logout()`
- ✅ Sessie ophalen: `auth_service.get_current_user()`
- ✅ Sessie vernieuwen: `auth_service.refresh_session(refresh_token)`
- ✅ Wachtwoord reset: `auth_service.reset_password(email)`
- ✅ Email bevestiging opnieuw verzenden: `auth_service.resend_confirmation(email)`

**Gebruikt in:**
- AuthState (base state voor authenticatie)
- Landing page voor login/signup
- Automatische sessie herstel bij page load

**User reference:**
- Alle user-gerelateerde foreign keys verwijzen naar `auth.users(id)`
- Supabase Auth beheert users automatisch
- User metadata (naam, email) wordt opgeslagen in Supabase Auth

---

## 🎯 State Management & Database Integratie

### AppState (`educhat/state/app_state.py`)

**Database operaties:**
1. **Chat Persistentie**
   - `save_conversation_to_db()` - Slaat huidige conversatie op na elk bericht
   - `load_conversations_from_db()` - Laadt alle conversaties bij startup
   - `load_conversation_messages()` - Laadt specifieke conversatie

2. **Sessie Management**
   - `check_and_restore_session()` - Herstelt gebruiker bij page load
   - Automatische sessie check in `initialize_chat()`

3. **Onboarding Context**
   - `load_onboarding_preferences()` - Laadt quiz resultaten voor AI personalisatie
   - `get_ai_context_string()` - Gebruikt opgeslagen voorkeuren in AI prompts

4. **Feedback Tracking**
   - `handle_message_feedback()` - Slaat likes/dislikes op in database

### AuthState (`educhat/state/auth_state.py`)

**Database operaties:**
1. **Authenticatie**
   - `handle_login()` - Gebruikt Supabase Auth
   - `handle_signup()` - Registreert nieuwe gebruiker
   - `handle_logout()` - Log uit via Supabase

2. **Events**
   - `load_upcoming_events()` - Haalt events uit database
   - `_load_events_from_local()` - Fallback naar lokale data

3. **Herinneringen**
   - `create_reminder()` - Slaat herinnering op in DB
   - `create_reminder_from_event()` - Maakt herinnering vanuit event
   - `load_reminders_from_db()` - Laadt alle herinneringen
   - `delete_reminder()` - Verwijdert uit database

### OnboardingState (`educhat/state/onboarding_state.py`)

**Database operaties:**
1. **Quiz Resultaten**
   - `complete_quiz()` - Slaat alle antwoorden op in JSONB field
   - `load_user_preferences()` - Laadt opgeslagen voorkeuren

2. **AI Context**
   - `get_user_context()` - Genereert context dict voor AI
   - `get_context_summary()` - Human-readable samenvatting

---

## 🤖 AI Service & Database Context

Locatie: `educhat/services/ai_service.py`

**Database integratie:**
- AI krijgt automatisch context uit database:
  - User onboarding voorkeuren
  - Instellingen en studies data
  - Education system informatie

**EducationDataService** (`educhat/services/education_service.py`):
- Combineert lokale JSON data met Supabase data
- `get_all_institutions()` - Merged local + database
- `search_institutions_supabase()` - Zoekt in database
- `get_context_for_query()` - Voegt database context toe aan AI prompts

---

## 📊 Database Flows - Stap voor Stap

### 1. **Nieuwe Gebruiker Registratie**
```
1. User vult signup form in
2. AuthState.handle_signup() roept aan:
   -> auth_service.signup(email, password, name)
3. Supabase Auth maakt user aan in auth.users table
4. User krijgt verificatie email
5. Na verificatie kan user inloggen
```

### 2. **Login & Sessie Herstel**
```
1. User bezoekt site
2. AppState.check_and_restore_session() checkt:
   -> auth_service.get_current_user()
3. Als sessie geldig:
   - Herstel user_id, email, name in state
   - Laad conversaties: load_conversations_from_db()
   - Laad onboarding: load_onboarding_preferences()
   - Laad events: load_upcoming_events()
4. User kan verder waar ze gestopt zijn
```

### 3. **Chat Bericht Flow**
```
1. User typt bericht
2. AppState.send_message():
   - Voeg user bericht toe aan messages lijst
   - Call AI met context uit onboarding
   - Stream AI response
3. Na response:
   - Update conversation metadata (title, timestamp)
   - Call save_conversation_to_db():
     a. Check of conversation al in DB bestaat
     b. Zo niet: create_conversation()
     c. Save alle nieuwe messages met save_message()
4. Berichten zijn nu persistent
```

### 4. **Onboarding Quiz Flow**
```
1. User doorloopt quiz
2. Bij elke vraag: antwoord opslaan in state
3. OnboardingState.complete_quiz():
   - Verzamel alle antwoorden in JSONB object
   - Als edit mode: update_onboarding()
   - Anders: create_onboarding() -> update_onboarding()
4. Bij volgende login:
   - load_user_preferences() haalt antwoorden op
   - Context wordt toegevoegd aan AI prompts
```

### 5. **Event Herinnering Flow**
```
1. User ziet event in Events Panel
2. Klikt "Herinnering maken"
3. AuthState.create_reminder_from_event():
   - Haal event data
   - Call db.create_reminder(user_id, title, date)
   - Voeg toe aan reminders lijst
4. Herinnering zichtbaar in Reminders Modal
5. Bij pagina refresh: load_reminders_from_db()
```

---

## ✅ Checklist: Wat gebruikt de database?

| Functionaliteit | Database? | Tabel(len) | Locatie in Code |
|----------------|-----------|-----------|-----------------|
| User Login/Signup | ✅ | auth.users | auth_service.py |
| Chat Berichten Opslaan | ✅ | conversations, messages | app_state.py: save_conversation_to_db() |
| Chat Geschiedenis | ✅ | conversations, messages | app_state.py: load_conversations_from_db() |
| Onboarding Quiz | ✅ | onboarding | onboarding_state.py: complete_quiz() |
| AI Personalisatie | ✅ | onboarding | app_state.py: load_onboarding_preferences() |
| Herinneringen | ✅ | reminders | auth_state.py: create_reminder() |
| Events/Deadlines | ✅ | events | auth_state.py: load_upcoming_events() |
| Instellingen Info | ✅ | institutions | education_service.py |
| Opleidingen Info | ✅ | studies | education_service.py |
| Message Feedback | ✅ | messages.feedback | app_state.py: handle_message_feedback() |
| Sessie Herstel | ✅ | auth session | app_state.py: check_and_restore_session() |

---

## 🚀 Setup Instructies

### 1. Database Setup (Supabase)
```bash
# 1. Maak Supabase project aan op supabase.com
# 2. Run SQL schema:
#    - Ga naar SQL Editor in Supabase dashboard
#    - Kopieer en run: prisma/create_tables.sql
# 3. Run RLS policies (optioneel maar aanbevolen):
#    - Kopieer en run: prisma/rls_policies.sql
```

### 2. Environment Variables
```bash
# Kopieer .env.example naar .env
cp .env.example .env

# Vul in:
# - SUPABASE_URL=https://[project].supabase.co
# - SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
# - SUPABASE_ANON_KEY=your_anon_key
# - OPENAI_API_KEY of GOOGLE_AI_API_KEY
```

### 3. Test Database Connectie
```python
# Test script
from educhat.services.supabase_client import get_client

client = get_client()
print("✅ Database connected!")

# Test query
from educhat.services.supabase_client import get_service
db = get_service()
institutions = db.get_all_institutions()
print(f"Found {len(institutions)} institutions")
```

---

## 📝 Database Schema Updates

Als je de database schema wilt updaten:

1. **Lokaal testen:**
   ```sql
   -- Voeg nieuwe kolom toe
   ALTER TABLE conversations ADD COLUMN tags JSONB;
   ```

2. **Update in code:**
   ```python
   # In supabase_client.py
   def save_conversation_with_tags(self, conv_id, tags):
       self.client.table('conversations').update({
           'tags': tags
       }).eq('id', conv_id).execute()
   ```

3. **Update create_tables.sql** voor nieuwe deployments

---

## 🔍 Debugging Database Issues

### Check connectie:
```python
from educhat.services.supabase_client import get_client
try:
    client = get_client()
    response = client.table('institutions').select('count').execute()
    print(f"✅ Connected! Count: {response.data}")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Check environment variables:
```python
import os
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_ANON_KEY:", os.getenv("SUPABASE_ANON_KEY")[:20] + "...")
```

### Enable SQL logging:
```python
# In supabase_client.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📈 Performance & Best Practices

### ✅ Wat er goed is:
1. **Connection pooling** - Singleton pattern voor database client
2. **Async operations** - asyncio voor non-blocking queries
3. **Indexed queries** - Alle FK's en search fields zijn geïndexeerd
4. **Batch updates** - Meerdere messages in één keer opslaan
5. **Lazy loading** - Database connect alleen wanneer nodig

### 💡 Optimalisatie tips:
1. **Pagination** gebruiken voor grote datasets:
   ```python
   messages = db.get_conversation_messages(conv_id, limit=50, offset=0)
   ```

2. **Caching** voor statische data:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=100)
   def get_institution_cached(inst_id):
       return db.get_institution_by_id(inst_id)
   ```

3. **Select only needed fields**:
   ```python
   # Instead of SELECT *
   query = client.table('messages').select('content, role, timestamp')
   ```

---

## ✨ Conclusie

**ALLE belangrijke functionaliteiten van EduChat gebruiken de database!**

- ✅ Authenticatie via Supabase Auth
- ✅ Chat persistentie voor ingelogde users
- ✅ Onboarding data voor AI personalisatie
- ✅ Herinneringen en events tracking
- ✅ Feedback op messages
- ✅ Education data (institutions, studies)

De applicatie is **volledig database-driven** en werkt seamless met Supabase PostgreSQL.
