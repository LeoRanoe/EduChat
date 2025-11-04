# 🚀 EduChat Development Guide

**Version:** 0.1.0  
**Last Updated:** November 4, 2025  
**Status:** Phase 1.1 Complete - Project Initialization

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Project Structure](#project-structure)
4. [Getting Started](#getting-started)
5. [Development Workflow](#development-workflow)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Next Steps](#next-steps)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

**EduChat** is an AI-powered educational assistant specifically designed for Surinamese students. It helps students with:
- Finding information about educational institutions in Suriname
- Understanding admission requirements and application processes
- Getting answers to education-related questions in Dutch
- Comparing different educational programs

### Tech Stack

- **Framework:** Reflex (Python full-stack framework)
- **Database:** MongoDB Atlas
- **AI Service:** OpenAI GPT-4 (or Google Gemini)
- **Deployment:** Render
- **Version Control:** Git/GitHub

---

## ✅ Prerequisites

Before you start, ensure you have the following installed:

- [x] **Python 3.12.6** (or 3.11+)
- [x] **Git 2.46.0**
- [x] **VS Code** (or preferred IDE)
- [x] **Virtual Environment** activated
- [ ] **MongoDB Compass** (download from https://www.mongodb.com/try/download/compass)

### Required Accounts

You'll need to create accounts for:

1. **MongoDB Atlas** (free tier) - https://www.mongodb.com/cloud/atlas/register
2. **OpenAI** - https://platform.openai.com/signup (or Google AI Studio)
3. **Render** - https://render.com/ (for deployment)

---

## 📁 Project Structure

```
EduChat/
├── .github/              # GitHub workflows (future CI/CD)
├── .venv/                # Virtual environment (not in git)
├── assets/               # Static assets (images, icons)
├── Documents/            # Project documentation
│   ├── design-requirements.md
│   ├── project-checklist.md
│   └── ...
├── educhat/              # Main application code
│   ├── __init__.py
│   ├── educhat.py       # App entry point
│   ├── components/       # UI components
│   │   ├── __init__.py
│   │   └── shared/      # Reusable components
│   ├── pages/           # Application pages
│   │   ├── __init__.py
│   │   └── index.py     # Main chat page
│   ├── services/        # External integrations
│   │   └── __init__.py
│   ├── state/           # State management
│   │   ├── __init__.py
│   │   └── app_state.py # Main app state
│   ├── styles/          # Styling and themes
│   │   ├── __init__.py
│   │   └── theme.py     # Color palette, fonts
│   └── utils/           # Utility functions
│       ├── __init__.py
│       ├── constants.py
│       └── helpers.py
├── .env                 # Environment variables (not in git)
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore rules
├── README.md            # Project readme
├── requirements.txt     # Python dependencies
└── rxconfig.py          # Reflex configuration
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/LeoRanoe/EduChat.git
cd EduChat
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.\venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   MONGODB_URI=your_mongodb_connection_string
   OPENAI_API_KEY=your_openai_api_key
   ```

### 5. Verify Installation

Check that Reflex is installed correctly:
```bash
reflex --version
```

---

## 🔧 Configuration

### MongoDB Setup

1. **Create MongoDB Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas/register
   - Choose the free tier (M0)

2. **Create a Cluster**
   - Select a cloud provider (AWS recommended)
   - Choose a region (closest to Suriname or target users)
   - Name your cluster (e.g., `educhat-cluster`)

3. **Create Database User**
   - Go to Database Access
   - Add a new user with password authentication
   - Save username and password

4. **Configure Network Access**
   - Go to Network Access
   - Add IP Address: `0.0.0.0/0` (allow from anywhere) for development
   - For production, restrict to specific IPs

5. **Get Connection String**
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database password
   - Add to `.env` file as `MONGODB_URI`

### OpenAI API Setup

1. **Create OpenAI Account**
   - Go to https://platform.openai.com/signup
   - Complete registration

2. **Generate API Key**
   - Go to https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (you won't see it again!)
   - Add to `.env` file as `OPENAI_API_KEY`

3. **Add Payment Method**
   - OpenAI requires a payment method for API access
   - Add card details in billing settings
   - Set usage limits to control costs

---

## 💻 Development Workflow

### Git Branching Strategy

We use three main branches:

- **`main`** - Production-ready code
- **`staging`** - Pre-production testing
- **`dev`** - Active development

### Working on a Feature

1. **Switch to dev branch:**
   ```bash
   git checkout dev
   ```

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request:**
   - Go to GitHub repository
   - Create PR from your feature branch to `dev`
   - Request review if working in a team

### Commit Message Convention

Use conventional commits format:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting)
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

**Examples:**
```bash
git commit -m "feat: add chat message component"
git commit -m "fix: resolve MongoDB connection timeout"
git commit -m "docs: update installation instructions"
```

---

## 🏃 Running the Application

### Development Mode

Start the Reflex development server:

```bash
reflex run
```

This will:
- Start the backend server (Python)
- Start the frontend dev server (Next.js)
- Open browser at http://localhost:3000

### Hot Reload

Reflex supports hot reload. Any changes to Python files will automatically restart the server.

### Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

---
### Development Priorities

1. **Week 1**: Complete MongoDB and AI integration
2. **Week 2**: Build core UI components
3. **Week 3**: Implement chat functionality and state management

---

## 🐛 Troubleshooting

### Virtual Environment Issues

**Problem:** Virtual environment not activating

**Solution:**
```powershell
# PowerShell: Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

### Module Import Errors

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### Reflex Commands Not Found

**Problem:** `reflex: command not found`

**Solution:**
```bash
# Verify reflex is installed
pip list | grep reflex

# If not installed
pip install reflex

# On Windows, use full path if needed
D:/EduChat/venv/Scripts/reflex.exe run
```

### MongoDB Connection Errors

**Problem:** Cannot connect to MongoDB Atlas

**Solution:**
1. Verify connection string in `.env`
2. Check network access settings (IP whitelist)
3. Verify database user credentials
4. Test connection with MongoDB Compass

### Port Already in Use

**Problem:** Port 3000 or 8000 already in use

**Solution:**
```bash
# Find and kill process using the port
# Windows PowerShell:
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process

# Or change port in rxconfig.py:
config = rx.Config(
    app_name="educhat",
    frontend_port=3001,
    backend_port=8001,
)
```

---

## 📚 Additional Resources

### Documentation

- **Reflex Docs:** https://reflex.dev/docs/getting-started/introduction/
- **MongoDB Docs:** https://www.mongodb.com/docs/
- **OpenAI API Docs:** https://platform.openai.com/docs/introduction
- **Python dotenv:** https://pypi.org/project/python-dotenv/

### Learning Resources

- **Reflex Tutorial:** https://reflex.dev/docs/tutorial/intro/
- **MongoDB University:** https://university.mongodb.com/
- **OpenAI Cookbook:** https://github.com/openai/openai-cookbook

### Community & Support

- **Reflex Discord:** https://discord.gg/reflex-dev
- **Stack Overflow:** Tag questions with `reflex`, `mongodb`, `openai`
- **GitHub Issues:** https://github.com/LeoRanoe/EduChat/issues

---

## 📝 Code Style Guidelines

### Python Code Style

Follow PEP 8 standards:

```python
# Good: Clear function names, type hints, docstrings
def format_message(role: str, content: str) -> dict:
    """Format a message for storage.
    
    Args:
        role: The role of the message sender (user/assistant)
        content: The message content
        
    Returns:
        Dictionary with formatted message data
    """
    return {
        "role": role,
        "content": content,
        "timestamp": get_timestamp(),
    }
```

### Component Organization

```python
# Structure components consistently
import reflex as rx
from educhat.styles.theme import COLORS

def my_component() -> rx.Component:
    """Component description."""
    return rx.box(
        rx.text("Content"),
        style={
            "background": COLORS["primary_green"],
            "padding": "1rem",
        }
    )
```

---