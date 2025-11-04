# 🛠️ EduChat – Development Environment Setup Plan

**Project:** EduChat  
**Purpose:** Complete guide for setting up the development environment  
**Timeline:** 1-2 days for complete setup

---

## 📋 Prerequisites Checklist

### Required Software
- [ ] **Python 3.11 or higher** - [Download](https://www.python.org/downloads/)
  - Verify: `python --version`
- [ ] **Git** - [Download](https://git-scm.com/downloads)
  - Verify: `git --version`
- [ ] **Node.js 18+ and npm** (required by Reflex) - [Download](https://nodejs.org/)
  - Verify: `node --version` and `npm --version`
- [ ] **Visual Studio Code** or preferred IDE - [Download](https://code.visualstudio.com/)
- [ ] **MongoDB Compass** (optional, for database GUI) - [Download](https://www.mongodb.com/products/compass)

### Required Accounts
- [ ] **GitHub Account** - [Sign up](https://github.com/signup)
- [ ] **MongoDB Atlas Account** - [Sign up](https://www.mongodb.com/cloud/atlas/register)
- [ ] **OpenAI Account** - [Sign up](https://platform.openai.com/signup)
  - Alternative: Google AI Studio - [Sign up](https://makersuite.google.com/)
- [ ] **Render Account** - [Sign up](https://render.com/register)

---

## 🚀 Step-by-Step Setup

### Step 1: Create GitHub Repository

```bash
# Create new repository on GitHub.com
# Repository name: EduChat
# Visibility: Public (or Private)
# Initialize with: README

# Clone to local machine
git clone https://github.com/LeoRanoe/EduChat.git
cd EduChat

# Create branch structure
git checkout -b dev
git push origin dev
git checkout -b staging
git push origin staging
git checkout main
```

**Branch Strategy:**
- `main` - Production-ready code (deploy to Render)
- `staging` - QA testing environment
- `dev` - Active development branch

---

### Step 2: Set Up Python Virtual Environment

```bash
# Navigate to project directory
cd EduChat

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip
```

---

### Step 3: Install Reflex and Dependencies

```bash
# Install Reflex
pip install reflex

# Initialize Reflex project
reflex init

# When prompted:
# - App name: educhat
# - Template: blank (or choose a starter template)

# Install additional dependencies
pip install pymongo python-dotenv openai

# For Google AI (alternative to OpenAI):
# pip install google-generativeai

# Development dependencies
pip install pytest black flake8 python-dotenv

# Freeze dependencies
pip freeze > requirements.txt
```

**Expected Project Structure After Init:**
```
EduChat/
├── educhat/
│   ├── __init__.py
│   └── educhat.py          # Main app file
├── assets/
├── .web/                    # Reflex generated files (add to .gitignore)
├── rxconfig.py
└── requirements.txt
```

---

### Step 4: MongoDB Atlas Setup

#### 4.1 Create Cluster
1. Log in to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Click **"Build a Database"**
3. Choose **"Shared"** (Free tier - M0)
4. Select **Region** closest to Suriname (e.g., `us-east-1` or `eu-west-1`)
5. Cluster Name: `EduChat-Cluster`
6. Click **"Create"**

#### 4.2 Create Database User
1. Navigate to **Database Access**
2. Click **"Add New Database User"**
3. Authentication Method: **Password**
4. Username: `educhat_admin`
5. Password: Generate strong password (save securely!)
6. Database User Privileges: **Read and write to any database**
7. Click **"Add User"**

#### 4.3 Configure Network Access
1. Navigate to **Network Access**
2. Click **"Add IP Address"**
3. For development: Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - ⚠️ For production, restrict to specific IPs
4. Click **"Confirm"**

#### 4.4 Get Connection String
1. Go to **Database** → **Connect**
2. Choose **"Connect your application"**
3. Driver: **Python** | Version: **3.12 or later**
4. Copy connection string:
   ```
   mongodb+srv://educhat_admin:<password>@educhat-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
5. Replace `<password>` with your database user password
6. Save this connection string securely

#### 4.5 Create Database and Collections
```python
# Run this script once to initialize database structure
# File: data/scripts/init_database.py

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv('MONGODB_URI'))
db = client['educhat_db']

# Create collections
collections = [
    'instellingen',      # Educational institutions
    'vragen',            # Questions and answers log
    'sessies',           # User sessions
    'kennisbank',        # Knowledge base
    'feedback',          # User feedback
    'users'              # User accounts (Phase 4)
]

for collection_name in collections:
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"✅ Created collection: {collection_name}")
    else:
        print(f"ℹ️ Collection already exists: {collection_name}")

# Create indexes
db.vragen.create_index("timestamp")
db.sessies.create_index("session_id")
db.feedback.create_index([("message_id", 1), ("timestamp", -1)])

print("\n✅ Database initialization complete!")
client.close()
```

---

### Step 5: OpenAI API Setup

#### 5.1 Get API Key
1. Log in to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to **API Keys** section
3. Click **"Create new secret key"**
4. Name: `EduChat-Dev`
5. Copy the key immediately (you won't see it again!)
6. Save securely

#### 5.2 Test API Connection
```python
# File: services/test_openai.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

try:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Surinamese education."},
            {"role": "user", "content": "What is MINOV?"}
        ]
    )
    print("✅ OpenAI API connection successful!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Alternative: Google AI Setup**
```python
# If using Google AI instead
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_AI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("What is MINOV in Suriname?")
print(response.text)
```

---

### Step 6: Environment Variables Configuration

#### 6.1 Create `.env` file
```bash
# In project root
touch .env  # macOS/Linux
# or create manually on Windows
```

#### 6.2 Add Environment Variables
```env
# .env file content

# MongoDB Configuration
MONGODB_URI=mongodb+srv://educhat_admin:YOUR_PASSWORD@educhat-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=educhat_db

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-3.5-turbo
# For production, consider gpt-4 for better quality

# Alternative: Google AI Configuration
# GOOGLE_AI_API_KEY=your_google_ai_api_key_here
# GOOGLE_AI_MODEL=gemini-pro

# Application Configuration
APP_NAME=EduChat
APP_VERSION=1.0.0
ENVIRONMENT=development  # development, staging, production

# Security
SECRET_KEY=your_secret_key_here_generate_random_string
SESSION_TIMEOUT=3600  # 1 hour in seconds

# Render Configuration (for deployment)
RENDER_EXTERNAL_URL=https://educhat.onrender.com
```

#### 6.3 Create `.env.example` Template
```env
# .env.example - Template for environment variables
# Copy this to .env and fill in your actual values

MONGODB_URI=your_mongodb_connection_string
MONGODB_DB_NAME=educhat_db
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
APP_NAME=EduChat
APP_VERSION=1.0.0
ENVIRONMENT=development
SECRET_KEY=generate_random_secret_key
SESSION_TIMEOUT=3600
```

---

### Step 7: Configure `.gitignore`

```gitignore
# .gitignore

# Environment variables
.env
.env.local
.env.*.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# Reflex
.web/
*.db

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Build
dist/
build/
*.egg-info/

# MongoDB local
data/db/
```

---

### Step 8: Project Structure Setup

```bash
# Create directory structure
mkdir -p educhat/components/shared
mkdir -p educhat/pages
mkdir -p educhat/services
mkdir -p educhat/state
mkdir -p educhat/utils
mkdir -p educhat/styles
mkdir -p data/scripts
mkdir -p tests
mkdir -p docs
mkdir -p assets/images
mkdir -p assets/icons
mkdir -p assets/illustrations

# Create __init__.py files for Python packages
touch educhat/__init__.py
touch educhat/components/__init__.py
touch educhat/components/shared/__init__.py
touch educhat/pages/__init__.py
touch educhat/services/__init__.py
touch educhat/state/__init__.py
touch educhat/utils/__init__.py
touch educhat/styles/__init__.py
```

---

### Step 9: Create Core Configuration Files

#### 9.1 `rxconfig.py` - Reflex Configuration
```python
# rxconfig.py

import reflex as rx

config = rx.Config(
    app_name="educhat",
    api_url="http://localhost:8000",  # Development
    # For production on Render:
    # api_url=os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000"),
    db_url="sqlite:///reflex.db",  # Reflex's internal DB (not main app DB)
    env=rx.Env.DEV,
)
```

#### 9.2 `requirements.txt`
```txt
reflex>=0.4.0
pymongo>=4.6.0
python-dotenv>=1.0.0
openai>=1.0.0
# google-generativeai>=0.3.0  # Alternative to OpenAI

# Development
pytest>=7.4.0
black>=23.0.0
flake8>=6.0.0
```

#### 9.3 `services/database.py` - MongoDB Connection
```python
# educhat/services/database.py

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    """MongoDB connection handler with connection pooling"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            mongodb_uri = os.getenv('MONGODB_URI')
            db_name = os.getenv('MONGODB_DB_NAME', 'educhat_db')
            
            self._client = MongoClient(
                mongodb_uri,
                maxPoolSize=50,
                minPoolSize=10,
                serverSelectionTimeoutMS=5000
            )
            self._db = self._client[db_name]
            print("✅ MongoDB connected successfully")
    
    @property
    def db(self):
        """Get database instance"""
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            print("MongoDB connection closed")

# Singleton instance
db_instance = Database()
db = db_instance.db
```

#### 9.4 `services/ai_service.py` - AI Service
```python
# educhat/services/ai_service.py

import openai
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

class AIService:
    """OpenAI service for generating responses"""
    
    SYSTEM_PROMPT = """
    Je bent EduChat, een behulpzame AI-assistent gespecialiseerd in het Surinaamse onderwijssysteem.
    
    Je helpt studenten met:
    - Informatie over opleidingen en instellingen in Suriname
    - Toelatingseisen en inschrijvingsprocedures
    - Deadlines en belangrijke data
    - Vergelijkingen tussen studies
    - Algemene studie-advies
    
    Belangrijke richtlijnen:
    - Gebruik vriendelijke, toegankelijke taal in het Nederlands
    - Wees specifiek over Surinaamse context (MINOV, universiteiten, etc.)
    - Als je iets niet zeker weet, zeg dat eerlijk
    - Bied altijd constructieve en motiverende antwoorden
    - Verwijs naar officiële bronnen waar mogelijk
    """
    
    @staticmethod
    def generate_response(user_message: str, conversation_history: list = None) -> str:
        """
        Generate AI response based on user message and conversation history
        
        Args:
            user_message: The user's question
            conversation_history: Previous messages in format [{"role": "user/assistant", "content": "..."}]
        
        Returns:
            AI-generated response string
        """
        try:
            messages = [{"role": "system", "content": AIService.SYSTEM_PROMPT}]
            
            # Add conversation history (last 5 messages for context)
            if conversation_history:
                messages.extend(conversation_history[-5:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            return "Sorry, ik ondervind momenteel technische problemen. Probeer het later opnieuw."
```

---

### Step 10: Test Development Environment

#### 10.1 Run Reflex Development Server
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Run Reflex
reflex run

# Expected output:
# ─────────────────────────────────── Starting Reflex App ───────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────────────────
# App running at: http://localhost:3000
```

#### 10.2 Test Database Connection
```bash
python data/scripts/init_database.py
```

#### 10.3 Test AI Service
```bash
python educhat/services/test_openai.py
```

---

### Step 11: VS Code Extensions (Recommended)

Install these VS Code extensions for better development experience:

- **Python** (Microsoft) - Python language support
- **Pylance** (Microsoft) - Fast Python language server
- **Python Docstring Generator** - Auto-generate docstrings
- **GitLens** - Enhanced Git integration
- **MongoDB for VS Code** - MongoDB database viewer
- **Prettier** - Code formatter
- **ESLint** - JavaScript/TypeScript linting (for Reflex frontend)
- **Material Icon Theme** - Better file icons

---

### Step 12: Git Initial Commit

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial project setup with Reflex, MongoDB, and OpenAI integration"

# Push to dev branch
git checkout dev
git push origin dev

# Merge to staging
git checkout staging
git merge dev
git push origin staging

# When ready for production
git checkout main
git merge staging
git push origin main
```

---

## 🔍 Verification Checklist

- [ ] Python 3.11+ installed and verified
- [ ] Git installed and configured
- [ ] Node.js and npm installed
- [ ] GitHub repository created with branch structure (main, staging, dev)
- [ ] Virtual environment created and activated
- [ ] Reflex installed and initialized
- [ ] MongoDB Atlas cluster created
- [ ] Database user created with proper permissions
- [ ] MongoDB connection string obtained and tested
- [ ] OpenAI API key obtained and tested
- [ ] `.env` file created with all required variables
- [ ] `.gitignore` configured properly
- [ ] Project directory structure created
- [ ] Database connection module created and tested
- [ ] AI service module created and tested
- [ ] Reflex development server runs successfully
- [ ] Initial commit pushed to GitHub

---

## 🚨 Troubleshooting

### Issue: `reflex: command not found`
**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate  # Windows

# Reinstall Reflex
pip install --upgrade reflex
```

### Issue: MongoDB connection timeout
**Solution:**
- Check network access settings in MongoDB Atlas (whitelist your IP)
- Verify connection string format
- Check if MongoDB cluster is running (M0 free tier sleeps after inactivity)

### Issue: OpenAI API key invalid
**Solution:**
- Verify API key is correctly copied (no spaces)
- Check if billing is set up in OpenAI account
- Ensure API key has proper permissions

### Issue: Reflex won't start - Port already in use
**Solution:**
```bash
# Windows - Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# Change port in rxconfig.py
# api_url="http://localhost:8001"
```

---

## 📚 Additional Resources

- [Reflex Documentation](https://reflex.dev/docs/)
- [MongoDB Atlas Documentation](https://www.mongodb.com/docs/atlas/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [Git Branching Strategies](https://www.atlassian.com/git/tutorials/comparing-workflows)

---

## ✅ Next Steps After Setup

1. Review the **Project Checklist** (`project-checklist.md`)
2. Review the **Design Requirements Document** (`design-requirements.md`)
3. Start Phase 1 development:
   - Create core UI components
   - Implement chat interface
   - Connect AI service to chat
4. Regular commits to `dev` branch
5. Test on `staging` before merging to `main`

---

**Environment setup complete! Ready to start development. 🚀**
