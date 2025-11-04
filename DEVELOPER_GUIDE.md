# 🛠️ EduChat Developer Guide

**Version:** 1.0  
**Last Updated:** November 4, 2025  
**Target Audience:** Developers joining or working on the EduChat project

---

## 📚 Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Project Structure](#project-structure)
5. [Setup & Installation](#setup--installation)
6. [Development Workflow](#development-workflow)
7. [Key Libraries & Tools](#key-libraries--tools)
8. [State Management](#state-management)
9. [Styling & Theming](#styling--theming)
10. [Database Integration](#database-integration)
11. [AI Services](#ai-services)
12. [Testing Strategy](#testing-strategy)
13. [Deployment](#deployment)
14. [Best Practices](#best-practices)
15. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**EduChat** is an AI-powered educational chatbot specifically designed for the Surinamese education system. It helps students discover educational programs, admission requirements, deadlines, and provides personalized study guidance.

### Key Features
- Natural conversational interface using AI (OpenAI/Gemini)
- Personalized onboarding quiz
- Conversation history and context management
- Real-time chat with AI-generated responses
- MongoDB-based data persistence
- Responsive design (mobile-first)

### Development Phases
- **Phase 1 (MVP):** Basic chat interface, AI integration, database logging
- **Phase 2:** Onboarding quiz, feedback system, error handling
- **Phase 3:** Program comparison, analytics dashboard
- **Phase 4:** User accounts, reminders, multilingual support

---

## 🔧 Technology Stack

### Core Framework
**Reflex (Python)**
- **Version:** ≥0.5.0
- **Why:** Full-stack web framework that allows you to build both frontend and backend in pure Python
- **Key Features:**
  - Reactive state management
  - Component-based UI
  - Built-in routing
  - WebSocket support for real-time updates
  - Compiles to Next.js under the hood

### Database
**MongoDB Atlas**
- **Driver:** `pymongo` ≥4.6.0 (sync) and `motor` ≥3.3.0 (async)
- **Why:** 
  - Flexible document structure for varied educational data
  - Free tier available (512MB)
  - Easy to scale
  - JSON-like documents perfect for chat messages and user data

### AI/ML Services
**OpenAI API**
- **Library:** `openai` ≥1.12.0
- **Model:** GPT-4 (configurable)
- **Alternative:** Google Gemini (`google-generativeai` ≥0.3.0)
- **Purpose:** Natural language understanding and response generation

### Additional Libraries
- **python-dotenv** ≥1.0.0 - Environment variable management
- **pydantic** ≥2.5.0 - Data validation and settings management
- **pytest** ≥7.4.0 - Testing framework
- **black** ≥23.12.0 - Code formatting
- **ruff** ≥0.1.0 - Linting

### Deployment
- **Platform:** Render
- **CI/CD:** GitHub Actions
- **Branching:** dev → staging → main

---

## 🏗️ Architecture & Design Patterns

### Application Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser (User)                    │
└─────────────────────┬───────────────────────────────┘
                      │ HTTP/WebSocket
┌─────────────────────▼───────────────────────────────┐
│              Reflex Frontend (React)                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Pages   │  │Components│  │  Styles  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │ State Updates
┌─────────────────────▼───────────────────────────────┐
│            Reflex Backend (FastAPI)                 │
│  ┌─────────────────────────────────────────────┐   │
│  │           State Management (rx.State)       │   │
│  └─────────────────────┬───────────────────────┘   │
│                        │                            │
│  ┌────────────────────▼──────────────────────┐     │
│  │         Services Layer                    │     │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────┐ │     │
│  │  │ Database │  │AI Service│  │   RAG   │ │     │
│  │  │ Service  │  │          │  │ Service │ │     │
│  │  └──────────┘  └──────────┘  └─────────┘ │     │
│  └──────────────────────────────────────────┘     │
└───────────────┬──────────────────┬─────────────────┘
                │                  │
        ┌───────▼──────┐   ┌──────▼──────┐
        │   MongoDB    │   │  OpenAI API │
        │    Atlas     │   │             │
        └──────────────┘   └─────────────┘
```

### Design Patterns Used

1. **Component Pattern** - Reusable UI components
2. **State Management Pattern** - Centralized state with Reflex State
3. **Service Layer Pattern** - Business logic separated from UI
4. **Repository Pattern** - Database access abstraction
5. **Factory Pattern** - For creating AI service instances

---

## 📁 Project Structure

### Detailed Folder Breakdown

```
EduChat/
├── .github/
│   └── workflows/              # CI/CD automation
│       ├── dev.yml            # Deploy to dev on push to dev branch
│       ├── staging.yml        # Deploy to staging on push to staging
│       └── production.yml     # Deploy to main on push to main
│
├── educhat/                    # Main application package
│   ├── __init__.py            # Package initialization
│   ├── educhat.py             # Application entry point (app creation)
│   │
│   ├── components/            # Reusable UI components
│   │   ├── __init__.py
│   │   ├── shared/            # Shared components across pages
│   │   │   ├── __init__.py
│   │   │   ├── button.py      # Custom button components
│   │   │   ├── input.py       # Input field components
│   │   │   ├── card.py        # Card/container components
│   │   │   └── loader.py      # Loading indicators
│   │   ├── sidebar.py         # Conversation history sidebar
│   │   ├── chat_container.py  # Main chat display area
│   │   ├── message_bubble.py  # Individual message UI
│   │   └── onboarding_quiz.py # Quiz component
│   │
│   ├── pages/                 # Application pages (routes)
│   │   ├── __init__.py
│   │   ├── index.py           # Main chat page (/)
│   │   ├── onboarding.py      # Onboarding quiz (/onboarding)
│   │   └── admin.py           # Analytics dashboard (/admin)
│   │
│   ├── services/              # Backend business logic
│   │   ├── __init__.py
│   │   ├── database.py        # MongoDB connection and queries
│   │   ├── ai_service.py      # OpenAI/Gemini integration
│   │   ├── rag_service.py     # RAG implementation for context
│   │   └── feedback_service.py # User feedback handling
│   │
│   ├── state/                 # State management
│   │   ├── __init__.py
│   │   ├── app_state.py       # Main chat state
│   │   ├── onboarding_state.py # Quiz state
│   │   └── admin_state.py     # Admin dashboard state
│   │
│   ├── utils/                 # Helper functions
│   │   ├── __init__.py
│   │   ├── constants.py       # Application constants
│   │   ├── helpers.py         # Utility functions
│   │   └── validators.py      # Input validation
│   │
│   └── styles/                # Styling and theming
│       ├── __init__.py
│       ├── theme.py           # Color palette, fonts, spacing
│       └── components.py      # Component-specific styles
│
├── data/                      # Data files and import scripts
│   ├── instellingen.json      # Surinamese educational institutions
│   ├── opleidingen.json       # Programs and courses
│   └── scripts/
│       └── import_data.py     # Script to import data to MongoDB
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration
│   ├── test_services/         # Service layer tests
│   ├── test_state/            # State management tests
│   └── test_components/       # Component tests
│
├── Documents/                 # Project documentation
│   ├── design-requirements.md # UI/UX specifications
│   ├── project-checklist.md   # Development checklist
│   └── render-deployment.md   # Deployment guide
│
├── assets/                    # Static assets
│   ├── logo.png
│   ├── favicon.ico
│   └── images/
│
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── rxconfig.py                # Reflex configuration
├── render.yaml                # Render deployment config
├── README.md                  # Project overview
└── DEVELOPER_GUIDE.md         # This file
```

### Folder Responsibilities

| Folder | Purpose | When to Use |
|--------|---------|-------------|
| `components/` | Reusable UI elements | Creating buttons, inputs, cards, chat bubbles |
| `pages/` | Route definitions | Adding new pages/screens |
| `services/` | Business logic & external APIs | Database operations, AI calls, data processing |
| `state/` | Application state | Managing user interactions, chat history, UI state |
| `utils/` | Helper functions | Constants, validators, formatters |
| `styles/` | Design system | Colors, fonts, spacing, component styles |
| `tests/` | Test files | Writing unit and integration tests |

---

## 🚀 Setup & Installation

### Prerequisites

- **Python:** 3.11+ (recommended 3.11 or 3.12)
- **Node.js:** 16+ (for Reflex's frontend compilation)
- **Git:** For version control
- **MongoDB Atlas Account:** Free tier
- **OpenAI API Key:** Or Google AI API key

### Initial Setup

```powershell
# 1. Clone the repository
git clone https://github.com/LeoRanoe/EduChat.git
cd EduChat

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment template
copy .env.example .env

# 5. Edit .env with your credentials
# - MONGODB_URI=your_mongodb_connection_string
# - OPENAI_API_KEY=your_openai_api_key
# - GEMINI_API_KEY=your_gemini_api_key (optional)

# 6. Initialize Reflex
reflex init

# 7. Run the development server
reflex run
```

### Environment Variables

Create a `.env` file with:

```env
# Database
MONGODB_URI=mongodb+srv://<user>:<password>@cluster.mongodb.net/educhat
MONGODB_DB_NAME=educhat

# AI Services
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=...  # Optional

# Application
ENV=development
DEBUG=True
LOG_LEVEL=INFO

# Deployment (for production)
RENDER_EXTERNAL_URL=https://educhat.onrender.com
```

---

## 💻 Development Workflow

### Branch Strategy

```
main (production)
  ↑
staging (pre-production testing)
  ↑
dev (active development)
  ↑
feature/feature-name (individual features)
```

### Development Process

1. **Start from dev branch**
   ```powershell
   git checkout dev
   git pull origin dev
   ```

2. **Create feature branch**
   ```powershell
   git checkout -b feature/chat-interface
   ```

3. **Make changes and test locally**
   ```powershell
   reflex run  # Test in browser
   pytest      # Run tests
   ```

4. **Commit with clear messages**
   ```powershell
   git add .
   git commit -m "feat: implement chat message display"
   ```

5. **Push and create PR**
   ```powershell
   git push origin feature/chat-interface
   # Create Pull Request to dev branch on GitHub
   ```

6. **Code review → Merge to dev → Test → Merge to staging → Test → Merge to main**

### Running the Application

```powershell
# Development mode (with hot reload)
reflex run

# Production mode
reflex run --env prod

# Export static build
reflex export

# Run tests
pytest

# Format code
black educhat/

# Lint code
ruff check educhat/
```

---

## 📦 Key Libraries & Tools

### Reflex Framework

**What it is:** A Python web framework that lets you build interactive web apps using only Python.

**How it works:**
- Write components in Python
- Reflex compiles to React (Next.js) for the frontend
- Backend runs on FastAPI
- Real-time state synchronization via WebSocket

**Example Component:**

```python
import reflex as rx

def chat_bubble(message: str, is_user: bool) -> rx.Component:
    """Render a chat message bubble."""
    return rx.box(
        rx.text(message),
        background_color=rx.cond(
            is_user, 
            "#D4F1D4",  # User message (light green)
            "#FFFFFF"   # Bot message (white)
        ),
        padding="12px 16px",
        border_radius="12px",
        max_width="70%",
        align_self=rx.cond(is_user, "flex-end", "flex-start"),
    )
```

### MongoDB with PyMongo

**What it is:** Document database for storing conversations, user data, and educational information.

**Collections used:**
- `instellingen` - Educational institutions
- `vragen` - User questions
- `sessies` - Chat sessions
- `kennisbank` - Knowledge base for RAG
- `feedback` - User feedback

**Example Usage:**

```python
from pymongo import MongoClient
from educhat.utils.constants import COLLECTIONS

# In services/database.py
class DatabaseService:
    def __init__(self, connection_string: str):
        self.client = MongoClient(connection_string)
        self.db = self.client.educhat
    
    def save_message(self, conversation_id: str, message: dict):
        """Save a chat message to database."""
        return self.db[COLLECTIONS["questions"]].insert_one({
            "conversation_id": conversation_id,
            "message": message,
            "timestamp": datetime.utcnow()
        })
```

### OpenAI API

**What it is:** AI service for generating natural language responses.

**Configuration:**
- Model: GPT-4 (or GPT-3.5-turbo for cost savings)
- Temperature: 0.7 (balanced creativity)
- Max tokens: 1000

**Example Usage:**

```python
from openai import OpenAI

class AIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def generate_response(self, user_message: str, context: list) -> str:
        """Generate AI response based on user message and context."""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an educational assistant for Surinamese students."},
                *context,
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
```

---

## 🔄 State Management

### Reflex State Pattern

Reflex uses a reactive state management system where:
- State is defined as Python classes inheriting from `rx.State`
- State variables are class attributes
- Methods modify state and trigger UI updates
- State is automatically synchronized between backend and frontend

### Main State: AppState

**Location:** `educhat/state/app_state.py`

**Responsibilities:**
- Managing chat messages
- Handling user input
- Conversation history
- Loading states
- AI interaction coordination

**Key Variables:**

```python
class AppState(rx.State):
    """Main application state."""
    
    # Chat data
    messages: List[Dict] = []              # Current conversation messages
    conversations: List[Dict] = []         # All user conversations
    current_conversation_id: str = ""     # Active conversation ID
    
    # UI state
    user_input: str = ""                   # Current input field value
    is_loading: bool = False              # Loading indicator
    error_message: str = ""               # Error display
    
    # User context
    user_preferences: Dict = {}            # From onboarding quiz
```

**Key Methods:**

```python
async def send_message(self):
    """Handle sending a message to AI."""
    if not self.user_input.strip():
        return
    
    # Add user message to UI
    self.messages.append({
        "role": "user",
        "content": self.user_input,
        "timestamp": datetime.now()
    })
    
    # Clear input and show loading
    user_query = self.user_input
    self.user_input = ""
    self.is_loading = True
    
    try:
        # Get AI response
        ai_service = AIService()
        response = await ai_service.generate_response(
            user_query, 
            self.messages
        )
        
        # Add AI response
        self.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        
        # Save to database
        db_service = DatabaseService()
        await db_service.save_message(
            self.current_conversation_id,
            self.messages[-2:]  # Save last 2 messages
        )
        
    except Exception as e:
        self.error_message = "Sorry, something went wrong. Please try again."
    finally:
        self.is_loading = False
```

### State Best Practices

1. **Keep state minimal** - Only store what's necessary
2. **Use computed properties** for derived data
3. **Async methods** for I/O operations
4. **Clear naming** - Descriptive variable and method names
5. **Error handling** - Always wrap external calls in try/except

---

## 🎨 Styling & Theming

### Design System

**Location:** `educhat/styles/theme.py`

### Color Palette

```python
COLORS = {
    # Primary
    "primary_green": "#228B22",      # Main brand color
    "light_green": "#90EE90",        # Hover states
    "dark_green": "#006400",         # Active states
    
    # Neutrals
    "white": "#FFFFFF",
    "light_gray": "#F5F5F5",        # Backgrounds
    "gray": "#808080",              # Secondary text
    "dark_gray": "#333333",         # Primary text
    "border_gray": "#E0E0E0",       # Borders
    
    # Chat bubbles
    "user_bubble": "#D4F1D4",       # User messages
    "bot_bubble": "#FFFFFF",         # Bot messages
}
```

### Typography

```python
FONTS = {
    "heading": "Inter, sans-serif",
    "body": "Inter, sans-serif",
}

FONT_SIZES = {
    "h1": "48px",      # Welcome screens
    "h2": "32px",      # Section titles
    "h3": "24px",      # Subsections
    "body": "16px",    # Normal text
    "small": "14px",   # Secondary text
}
```

### Component Styling

**Using theme variables:**

```python
import reflex as rx
from educhat.styles.theme import COLORS, SPACING, RADIUS

def primary_button(text: str, on_click) -> rx.Component:
    """Primary action button."""
    return rx.button(
        text,
        on_click=on_click,
        background_color=COLORS["primary_green"],
        color=COLORS["white"],
        padding=f"{SPACING['sm']} {SPACING['lg']}",
        border_radius=RADIUS["full"],
        _hover={
            "background_color": COLORS["dark_green"],
        },
    )
```

### Responsive Design

```python
def chat_container() -> rx.Component:
    """Responsive chat container."""
    return rx.box(
        # Content here
        width=["100%", "100%", "80%", "60%"],  # Mobile, tablet, desktop, large
        padding=[SPACING["sm"], SPACING["md"], SPACING["lg"]],
    )
```

---

## 💾 Database Integration

### MongoDB Collections

| Collection | Purpose | Key Fields |
|------------|---------|------------|
| `instellingen` | Educational institutions | `name`, `location`, `programs`, `contact` |
| `vragen` | User questions | `conversation_id`, `question`, `answer`, `timestamp` |
| `sessies` | Chat sessions | `session_id`, `user_id`, `created_at`, `messages` |
| `kennisbank` | RAG knowledge base | `content`, `embedding`, `metadata` |
| `feedback` | User feedback | `message_id`, `rating`, `comment` |

### Database Service

**Location:** `educhat/services/database.py`

```python
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Optional

class DatabaseService:
    """Handle all database operations."""
    
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_URI"))
        self.db = self.client[os.getenv("MONGODB_DB_NAME", "educhat")]
    
    async def create_conversation(self, user_preferences: Dict) -> str:
        """Create a new conversation and return its ID."""
        conversation = {
            "created_at": datetime.utcnow(),
            "user_preferences": user_preferences,
            "messages": []
        }
        result = self.db.sessies.insert_one(conversation)
        return str(result.inserted_id)
    
    async def save_message(
        self, 
        conversation_id: str, 
        role: str, 
        content: str
    ) -> None:
        """Save a message to a conversation."""
        self.db.sessies.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$push": {
                    "messages": {
                        "role": role,
                        "content": content,
                        "timestamp": datetime.utcnow()
                    }
                }
            }
        )
    
    async def get_conversation_history(
        self, 
        conversation_id: str
    ) -> List[Dict]:
        """Retrieve all messages from a conversation."""
        conversation = self.db.sessies.find_one(
            {"_id": ObjectId(conversation_id)}
        )
        return conversation.get("messages", []) if conversation else []
    
    async def search_institutions(
        self, 
        query: str, 
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """Search educational institutions."""
        search_filter = {"$text": {"$search": query}}
        if filters:
            search_filter.update(filters)
        
        return list(self.db.instellingen.find(search_filter).limit(10))
```

---

## 🤖 AI Services

### AI Service Architecture

**Location:** `educhat/services/ai_service.py`

### OpenAI Integration

```python
from openai import AsyncOpenAI
from typing import List, Dict

class AIService:
    """Handle AI-powered responses."""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4"
        self.system_prompt = """
        You are EduChat, an educational assistant for Surinamese students.
        Your role is to help students find information about:
        - Educational institutions in Suriname
        - Admission requirements and procedures
        - Program details and career paths
        - Application deadlines
        
        Always be friendly, encouraging, and provide accurate information.
        If you don't know something, say so and suggest where they might find the information.
        """
    
    async def generate_response(
        self, 
        user_message: str,
        conversation_history: List[Dict],
        context: Optional[str] = None
    ) -> str:
        """Generate AI response with context."""
        
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add RAG context if available
        if context:
            messages.append({
                "role": "system",
                "content": f"Relevant information: {context}"
            })
        
        # Add conversation history (last 10 messages)
        messages.extend(conversation_history[-10:])
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"AI Service Error: {e}")
            raise
```

### RAG (Retrieval-Augmented Generation)

**Location:** `educhat/services/rag_service.py`

```python
class RAGService:
    """Retrieve relevant context from knowledge base."""
    
    def __init__(self, db_service: DatabaseService):
        self.db = db_service
    
    async def retrieve_context(self, query: str, top_k: int = 3) -> str:
        """Find relevant information for the query."""
        
        # Search institutions
        institutions = await self.db.search_institutions(query)
        
        # Format context
        context_parts = []
        for inst in institutions[:top_k]:
            context_parts.append(
                f"{inst['name']}: {inst.get('description', '')} "
                f"Programs: {', '.join(inst.get('programs', []))}"
            )
        
        return "\n".join(context_parts)
```

---

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── conftest.py              # Pytest fixtures
├── test_services/
│   ├── test_database.py     # Database operations
│   ├── test_ai_service.py   # AI integration
│   └── test_rag_service.py  # RAG functionality
├── test_state/
│   ├── test_app_state.py    # Chat state logic
│   └── test_onboarding.py   # Quiz state
└── test_integration/
    └── test_chat_flow.py    # End-to-end tests
```

### Writing Tests

**Example: Testing Database Service**

```python
import pytest
from educhat.services.database import DatabaseService

@pytest.fixture
def db_service():
    """Create database service for testing."""
    return DatabaseService()

@pytest.mark.asyncio
async def test_create_conversation(db_service):
    """Test conversation creation."""
    user_prefs = {"study_level": "HBO", "interest": "Technology"}
    conversation_id = await db_service.create_conversation(user_prefs)
    
    assert conversation_id is not None
    assert len(conversation_id) > 0

@pytest.mark.asyncio
async def test_save_and_retrieve_messages(db_service):
    """Test message persistence."""
    conversation_id = await db_service.create_conversation({})
    
    # Save messages
    await db_service.save_message(conversation_id, "user", "Hello")
    await db_service.save_message(conversation_id, "assistant", "Hi there!")
    
    # Retrieve
    messages = await db_service.get_conversation_history(conversation_id)
    
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "Hello"
```

### Running Tests

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=educhat --cov-report=html

# Run specific test file
pytest tests/test_services/test_database.py

# Run tests matching pattern
pytest -k "test_conversation"

# Verbose output
pytest -v
```

---

## 🚀 Deployment

### Render Deployment

**Configuration:** `render.yaml`

```yaml
services:
  - type: web
    name: educhat
    env: python
    buildCommand: pip install -r requirements.txt && reflex init && reflex export --frontend-only
    startCommand: reflex run --env prod
    envVars:
      - key: MONGODB_URI
        sync: false
      - key: OPENAI_API_KEY
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Deployment Steps

1. **Push to GitHub**
   ```powershell
   git push origin main
   ```

2. **Render auto-deploys** from main branch

3. **Set environment variables** in Render dashboard

4. **Monitor logs** during deployment

### Environment-Specific Configuration

```python
# rxconfig.py
import reflex as rx
import os

config = rx.Config(
    app_name="educhat",
    env=rx.Env.PROD if os.getenv("ENV") == "production" else rx.Env.DEV,
    backend_port=8000,
    frontend_port=3000,
    deploy_url=os.getenv("RENDER_EXTERNAL_URL"),
)
```

---

## ✅ Best Practices

### Code Style

1. **Follow PEP 8** - Use `black` for formatting
2. **Type hints** - Add type annotations to functions
3. **Docstrings** - Document all functions and classes
4. **Meaningful names** - Use descriptive variable/function names

```python
# Good
async def send_chat_message(self, message: str) -> Dict[str, Any]:
    """Send a message and get AI response.
    
    Args:
        message: The user's message text
        
    Returns:
        Dict containing the AI response and metadata
    """
    pass

# Bad
async def send(self, m):
    pass
```

### State Management

1. **Keep state flat** - Avoid nested state when possible
2. **Immutable updates** - Don't mutate state directly
3. **Async for I/O** - Use async methods for API calls
4. **Error boundaries** - Handle errors gracefully

### Performance

1. **Lazy loading** - Load data only when needed
2. **Pagination** - Limit database queries
3. **Caching** - Cache frequently accessed data
4. **Optimize images** - Compress assets

### Security

1. **Never commit secrets** - Use environment variables
2. **Validate inputs** - Sanitize user input
3. **Rate limiting** - Prevent API abuse
4. **HTTPS only** - Force secure connections in production

---

## 🔧 Troubleshooting

### Common Issues

#### Reflex won't start

```powershell
# Clear cache and reinstall
rm -rf .web
reflex init
reflex run
```

#### MongoDB connection fails

```powershell
# Check connection string
python -c "from pymongo import MongoClient; print(MongoClient('YOUR_URI').server_info())"
```

#### OpenAI API errors

```python
# Check API key
import openai
openai.api_key = "your_key"
print(openai.Model.list())
```

#### Module not found

```powershell
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Debug Mode

```python
# In educhat.py
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

1. **Check documentation:** [reflex.dev/docs](https://reflex.dev/docs)
2. **Project issues:** Check GitHub Issues
3. **Community:** Reflex Discord server
4. **Team:** Ask project maintainers

---

## 📝 Quick Reference

### Common Commands

```powershell
# Start dev server
reflex run

# Run tests
pytest

# Format code
black educhat/

# Lint code
ruff check educhat/

# Create component
# Add file to educhat/components/

# Create page
# Add file to educhat/pages/

# Install package
pip install package-name
pip freeze > requirements.txt
```

### File Templates

**Component Template:**

```python
"""Description of component."""
import reflex as rx
from educhat.styles.theme import COLORS

def my_component(prop: str) -> rx.Component:
    """Component description.
    
    Args:
        prop: Description of prop
        
    Returns:
        Reflex component
    """
    return rx.box(
        rx.text(prop),
        # Styling here
    )
```

**State Template:**

```python
"""Description of state."""
import reflex as rx
from typing import List, Dict

class MyState(rx.State):
    """State description."""
    
    # State variables
    data: List[Dict] = []
    is_loading: bool = False
    
    async def my_method(self):
        """Method description."""
        self.is_loading = True
        try:
            # Logic here
            pass
        finally:
            self.is_loading = False
```

---

## 📚 Additional Resources

- **Reflex Documentation:** https://reflex.dev/docs
- **Reflex Examples:** https://github.com/reflex-dev/reflex-examples
- **MongoDB Python:** https://pymongo.readthedocs.io/
- **OpenAI API:** https://platform.openai.com/docs
- **Python Best Practices:** https://docs.python-guide.org/

---

**Last Updated:** November 4, 2025  
**Maintainer:** Leo Ranoe  
**Project:** EduChat v1.0

For questions or issues, please create an issue on GitHub or contact the development team.
