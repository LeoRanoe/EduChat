# ⚡ EduChat - Quick Start Guide

**Start building EduChat in 5 steps! 🚀**

---

## 🎯 What You'll Build

A fully functional AI chatbot for Surinamese education that looks like this:

- ✅ Clean chat interface with sidebar
- ✅ AI-powered responses about Surinamese education
- ✅ MongoDB database for conversation logging
- ✅ Deployed and accessible online via Render
- ✅ Mobile-responsive design

**Timeline:** 2-3 weeks for MVP

---

## 📋 Prerequisites (30 minutes)

### Create These Accounts (All Free)
1. **GitHub** → [github.com/signup](https://github.com/signup)
2. **MongoDB Atlas** → [mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
3. **OpenAI** → [platform.openai.com/signup](https://platform.openai.com/signup)
4. **Render** → [render.com/register](https://render.com/register)

### Install These Tools
- **Python 3.11+** → [python.org/downloads](https://www.python.org/downloads/)
- **Node.js 18+** → [nodejs.org](https://nodejs.org/)
- **Git** → [git-scm.com/downloads](https://git-scm.com/downloads)
- **VS Code** → [code.visualstudio.com](https://code.visualstudio.com/)

---

## 🚀 Step 1: Project Setup (30 minutes)

```powershell
# 1. Create project folder
mkdir EduChat
cd EduChat

# 2. Initialize Git repository
git init
git remote add origin https://github.com/LeoRanoe/EduChat.git

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install Reflex
pip install reflex pymongo python-dotenv openai

# 5. Initialize Reflex project
reflex init
# When prompted, choose "blank" template and app name "educhat"

# 6. Create .env file
New-Item .env -ItemType File
```

Add to `.env`:
```env
MONGODB_URI=your_mongodb_uri_here
MONGODB_DB_NAME=educhat_db
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo
ENVIRONMENT=development
```

---

## 🗄️ Step 2: MongoDB Setup (15 minutes)

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Click **"Build a Database"** → Choose **"Free"** (M0)
3. Select region closest to you (e.g., `us-east-1`)
4. Create database user:
   - Username: `educhat_admin`
   - Password: Generate strong password (save it!)
5. Click **"Network Access"** → **"Add IP Address"** → **"Allow from anywhere"** (for development)
6. Click **"Connect"** → **"Connect your application"**
7. Copy connection string and add to `.env`:
```env
MONGODB_URI=mongodb+srv://educhat_admin:YOUR_PASSWORD@cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

---

## 🤖 Step 3: OpenAI API Setup (10 minutes)

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to **API Keys**
3. Click **"Create new secret key"**
4. Name it `EduChat-Dev`
5. Copy the key and add to `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Note:** You'll need to add billing info (~$10-20 for testing)

---

## 💻 Step 4: Build Core Chat Interface (2-3 hours)

### Create Project Structure
```powershell
mkdir educhat\components
mkdir educhat\pages
mkdir educhat\services
mkdir educhat\state
```

### 1. Database Service (`educhat/services/database.py`)
```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _client = None
    
    @classmethod
    def get_db(cls):
        if cls._client is None:
            cls._client = MongoClient(os.getenv('MONGODB_URI'))
        return cls._client[os.getenv('MONGODB_DB_NAME', 'educhat_db')]

db = Database.get_db()
```

### 2. AI Service (`educhat/services/ai_service.py`)
```python
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_ai_response(user_message: str) -> str:
    """Get AI response for user message"""
    try:
        response = openai.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[
                {"role": "system", "content": "Je bent een behulpzame assistent voor Surinaams onderwijs. Help studenten met informatie over opleidingen, toelatingseisen en studiekeuzebegeleiding in Suriname."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, er ging iets mis: {str(e)}"
```

### 3. App State (`educhat/state/app_state.py`)
```python
import reflex as rx
from educhat.services.ai_service import get_ai_response
from educhat.services.database import db
from datetime import datetime

class Message(rx.Base):
    role: str  # "user" or "assistant"
    content: str
    timestamp: str

class AppState(rx.State):
    messages: list[Message] = []
    user_input: str = ""
    is_loading: bool = False
    
    def send_message(self):
        if not self.user_input.strip():
            return
        
        # Add user message
        user_msg = Message(
            role="user",
            content=self.user_input,
            timestamp=datetime.now().isoformat()
        )
        self.messages.append(user_msg)
        
        # Save to database
        db.vragen.insert_one({
            "role": "user",
            "content": self.user_input,
            "timestamp": datetime.now()
        })
        
        # Get AI response
        self.is_loading = True
        query = self.user_input
        self.user_input = ""
        
        ai_response = get_ai_response(query)
        
        # Add AI message
        bot_msg = Message(
            role="assistant",
            content=ai_response,
            timestamp=datetime.now().isoformat()
        )
        self.messages.append(bot_msg)
        
        # Save to database
        db.vragen.insert_one({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now()
        })
        
        self.is_loading = False
```

### 4. Main Page (`educhat/educhat.py`)
```python
import reflex as rx
from educhat.state.app_state import AppState

def message_bubble(message) -> rx.Component:
    """Render a message bubble"""
    is_user = message.role == "user"
    return rx.box(
        rx.text(message.content),
        background_color="#D4F1D4" if is_user else "#FFFFFF",
        border="1px solid #E0E0E0" if not is_user else "none",
        border_radius="12px",
        padding="12px 16px",
        max_width="70%",
        margin_left="auto" if is_user else "0",
        margin_right="0" if is_user else "auto",
        margin_bottom="8px"
    )

def chat_interface() -> rx.Component:
    """Main chat interface"""
    return rx.container(
        rx.vstack(
            # Header
            rx.heading("Welkom bij EduChat", size="8", color="#228B22", text_align="center"),
            
            # Messages area
            rx.box(
                rx.foreach(AppState.messages, message_bubble),
                height="500px",
                overflow_y="auto",
                padding="20px",
                border="1px solid #E0E0E0",
                border_radius="8px",
                margin_y="20px"
            ),
            
            # Input area
            rx.hstack(
                rx.input(
                    placeholder="Vraag mij van alles!",
                    value=AppState.user_input,
                    on_change=AppState.set_user_input,
                    on_key_down=lambda key: AppState.send_message() if key == "Enter" else None,
                    width="100%",
                    padding="12px",
                    border_radius="8px"
                ),
                rx.button(
                    "➤",
                    on_click=AppState.send_message,
                    background_color="#228B22",
                    color="white",
                    border_radius="50%",
                    padding="12px 16px"
                ),
                width="100%"
            ),
            
            width="100%",
            max_width="800px",
            padding="20px"
        ),
        center_content=True
    )

app = rx.App()
app.add_page(chat_interface, route="/")
```

### 5. Run Development Server
```powershell
reflex run
```

**Open browser:** http://localhost:3000

---

## 🚀 Step 5: Deploy to Render (30 minutes)

### 1. Create `render.yaml` in project root:
```yaml
services:
  - type: web
    name: educhat
    env: python
    branch: main
    buildCommand: |
      pip install -r requirements.txt
      reflex init
      reflex export --frontend-only --no-zip
    startCommand: reflex run --env prod
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
```

### 2. Create `requirements.txt`:
```txt
reflex>=0.4.0
pymongo>=4.6.0
python-dotenv>=1.0.0
openai>=1.0.0
gunicorn>=21.2.0
```

### 3. Push to GitHub:
```powershell
git add .
git commit -m "Initial EduChat MVP"
git branch -M main
git push -u origin main
```

### 4. Deploy on Render:
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - Name: `educhat`
   - Branch: `main`
   - Build Command: (use from render.yaml)
   - Start Command: `reflex run --env prod`
5. Add Environment Variables:
   - `MONGODB_URI` (your connection string)
   - `OPENAI_API_KEY` (your API key)
   - `MONGODB_DB_NAME`: `educhat_db`
   - `OPENAI_MODEL`: `gpt-3.5-turbo`
   - `ENVIRONMENT`: `production`
6. Click **"Create Web Service"**

**Wait 5-10 minutes for deployment...**

**Your app is live!** 🎉 → `https://educhat.onrender.com`

---

## ✅ Verify It Works

Test your deployed app:

1. **Open URL:** `https://educhat.onrender.com`
2. **Type:** "Wat is MINOV?"
3. **Verify:** You get an AI response
4. **Check MongoDB:** See message logged in database

---

## 📚 What's Next?

You now have a working MVP! Continue with:

1. **Phase 2:** Add onboarding quiz (see [project-checklist.md](project-checklist.md))
2. **Improve UI:** Follow [design-requirements.md](design-requirements.md)
3. **Add Features:** Sidebar, feedback buttons, error handling

---

## 🆘 Quick Troubleshooting

### "reflex: command not found"
```powershell
venv\Scripts\activate
pip install --upgrade reflex
```

### "MongoDB connection failed"
- Check connection string in `.env`
- Verify IP whitelist in MongoDB Atlas
- Ensure database user has correct permissions

### "OpenAI API error"
- Verify API key in `.env`
- Check OpenAI account has billing enabled
- Try regenerating API key

### App won't deploy on Render
- Check build logs in Render dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` is up to date

---

## 📞 Get Help

- **Full Setup Guide:** [setup-guide.md](setup-guide.md)
- **Design Specs:** [design-requirements.md](design-requirements.md)
- **Complete Checklist:** [project-checklist.md](project-checklist.md)
- **Deployment Guide:** [render-deployment.md](render-deployment.md)

---

**Congratulations! You've built and deployed EduChat MVP! 🎉**

**Time spent:** ~4-5 hours  
**What you have:** Working AI chatbot live on the internet  
**Next:** Add more features and improve design
