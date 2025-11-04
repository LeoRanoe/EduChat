# 🚀 EduChat – Render Deployment Guide

**Project:** EduChat  
**Hosting Platform:** Render  
**Purpose:** Complete deployment strategy and configuration for production hosting

---

## 📋 Overview

Render provides free hosting for web applications with automatic deployments from GitHub. This guide covers:
- Initial Render setup
- Configuration for Reflex applications
- Environment variables management
- CI/CD pipeline setup
- Production optimizations
- Monitoring and maintenance

---

## 🎯 Render Service Options

### Recommended Service Type: **Web Service**

| Feature | Free Tier | Paid Tier ($7/mo) |
|---------|-----------|-------------------|
| RAM | 512 MB | 2 GB+ |
| CPU | Shared | Dedicated |
| Build time | 400 hrs/mo | Unlimited |
| Sleep after inactivity | Yes (15 min) | No |
| Custom domain | ✅ Yes | ✅ Yes |
| SSL Certificate | ✅ Free | ✅ Free |
| CI/CD from GitHub | ✅ Yes | ✅ Yes |

**Note:** Free tier sleeps after 15 minutes of inactivity (first request will take ~30s to wake up)

---

## 🛠️ Step-by-Step Deployment

### Step 1: Prepare Repository for Deployment

#### 1.1 Create `render.yaml` Configuration

Create a file named `render.yaml` in the project root:

```yaml
# render.yaml - Render deployment configuration

services:
  # Web Service for Reflex app
  - type: web
    name: educhat
    env: python
    region: oregon  # Choose: oregon, frankfurt, singapore
    plan: free  # or 'starter' for paid tier
    branch: main  # Deploy from main branch
    
    # Build command
    buildCommand: |
      pip install --upgrade pip
      pip install -r requirements.txt
      reflex init
      reflex export --frontend-only --no-zip
    
    # Start command
    startCommand: reflex run --env prod --backend-only
    
    # Environment variables (add in Render dashboard)
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
      - key: MONGODB_URI
        sync: false  # Set manually in dashboard
      - key: OPENAI_API_KEY
        sync: false  # Set manually in dashboard
      - key: MONGODB_DB_NAME
        value: educhat_db
      - key: OPENAI_MODEL
        value: gpt-3.5-turbo
      - key: ENVIRONMENT
        value: production
      - key: APP_NAME
        value: EduChat
      - key: APP_VERSION
        value: 1.0.0
    
    # Health check
    healthCheckPath: /
    
    # Auto-deploy on push to main
    autoDeploy: true

# Optional: Static site for frontend (if separating frontend/backend)
# - type: static
#   name: educhat-frontend
#   env: static
#   buildCommand: |
#     pip install -r requirements.txt
#     reflex export --frontend-only
#   staticPublishPath: .web/_static
#   routes:
#     - type: rewrite
#       source: /*
#       destination: /index.html
```

#### 1.2 Update `requirements.txt` for Production

```txt
# requirements.txt

# Core
reflex>=0.4.0
pymongo>=4.6.0
python-dotenv>=1.0.0
openai>=1.0.0

# Production server
gunicorn>=21.2.0
uvicorn[standard]>=0.24.0

# Optional: Google AI alternative
# google-generativeai>=0.3.0

# Monitoring (optional)
# sentry-sdk>=1.38.0
```

#### 1.3 Update `rxconfig.py` for Production

```python
# rxconfig.py

import reflex as rx
import os

# Determine environment
is_production = os.getenv('ENVIRONMENT', 'development') == 'production'

config = rx.Config(
    app_name="educhat",
    
    # API URL - use Render URL in production
    api_url=os.getenv("RENDER_EXTERNAL_URL", "http://localhost:8000") if is_production else "http://localhost:8000",
    
    # Database
    db_url="sqlite:///reflex.db",
    
    # Environment
    env=rx.Env.PROD if is_production else rx.Env.DEV,
    
    # Production optimizations
    frontend_packages=[
        "react@18.2.0",
        "react-dom@18.2.0",
    ],
    
    # Logging
    loglevel="INFO" if is_production else "DEBUG",
)
```

#### 1.4 Create Production Startup Script (Optional)

Create `start.sh` for custom startup:

```bash
#!/bin/bash
# start.sh - Production startup script

echo "🚀 Starting EduChat..."

# Run database migrations if needed
# python data/scripts/init_database.py

# Start Reflex in production mode
reflex run --env prod --loglevel info
```

Make it executable:
```bash
chmod +x start.sh
```

---

### Step 2: Push Code to GitHub

```bash
# Make sure all changes are committed
git add .
git commit -m "Add Render deployment configuration"

# Push to main branch
git checkout main
git push origin main
```

---

### Step 3: Create Render Account and Connect GitHub

1. Go to [Render.com](https://render.com/)
2. Click **"Get Started for Free"**
3. Sign up with **GitHub account** (recommended for easier integration)
4. Authorize Render to access your GitHub repositories

---

### Step 4: Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. **Connect Repository:**
   - Find and select **"EduChat"** repository
   - Click **"Connect"**
3. **Configure Service:**
   - **Name:** `educhat` (or your preferred name)
   - **Region:** Choose closest to Suriname (e.g., `US East (Ohio)`)
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or specify if different)
   - **Runtime:** `Python 3`
   - **Build Command:**
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && reflex init && reflex export --frontend-only --no-zip
     ```
   - **Start Command:**
     ```bash
     reflex run --env prod
     ```
   - **Plan:** Select **"Free"** (or paid tier)

4. Click **"Advanced"** to add environment variables

---

### Step 5: Configure Environment Variables

Add the following environment variables in Render dashboard:

| Key | Value | Notes |
|-----|-------|-------|
| `PYTHON_VERSION` | `3.11.7` | Python version |
| `MONGODB_URI` | `mongodb+srv://...` | Your MongoDB Atlas connection string |
| `MONGODB_DB_NAME` | `educhat_db` | Database name |
| `OPENAI_API_KEY` | `sk-proj-...` | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | AI model to use |
| `ENVIRONMENT` | `production` | Environment flag |
| `APP_NAME` | `EduChat` | Application name |
| `APP_VERSION` | `1.0.0` | Current version |
| `SECRET_KEY` | `random_string` | Generate secure random string |
| `SESSION_TIMEOUT` | `3600` | Session timeout in seconds |

**Security Best Practice:**
- Never commit API keys to Git
- Use Render's environment variables for all secrets
- Rotate keys periodically

---

### Step 6: Deploy Application

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Build the application
   - Start the server
3. **Monitor build logs** in real-time
4. Wait for deployment to complete (5-10 minutes)
5. Access your app at: `https://educhat.onrender.com`

---

## 🔄 CI/CD Pipeline Setup

### Automatic Deployments

Render automatically deploys when you push to the `main` branch:

```bash
# Development workflow
git checkout dev
# ... make changes ...
git add .
git commit -m "Add new feature"
git push origin dev

# Test on staging
git checkout staging
git merge dev
git push origin staging

# Deploy to production
git checkout main
git merge staging
git push origin main  # 🚀 Triggers automatic deployment
```

### GitHub Actions Integration (Optional)

Create `.github/workflows/deploy.yml` for advanced CI/CD:

```yaml
# .github/workflows/deploy.yml

name: Deploy to Render

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: |
          pytest tests/ -v
      
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 educhat/ --max-line-length=120

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Trigger Render Deploy
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

Add `RENDER_DEPLOY_HOOK` to GitHub Secrets:
1. Go to Render dashboard → Service → Settings
2. Copy **Deploy Hook URL**
3. Go to GitHub repo → Settings → Secrets and variables → Actions
4. Add new secret: `RENDER_DEPLOY_HOOK`

---

## 📊 Production Optimizations

### 1. Database Connection Pooling

Update `services/database.py`:

```python
# educhat/services/database.py

from pymongo import MongoClient
import os

class Database:
    _instance = None
    _client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._client = MongoClient(
                os.getenv('MONGODB_URI'),
                maxPoolSize=50,        # Increase for production
                minPoolSize=10,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                serverSelectionTimeoutMS=5000,
                retryWrites=True
            )
            self._db = self._client[os.getenv('MONGODB_DB_NAME', 'educhat_db')]
    
    @property
    def db(self):
        return self._db

db_instance = Database()
db = db_instance.db
```

### 2. AI Service Rate Limiting

```python
# educhat/services/ai_service.py

import time
from functools import wraps

def rate_limit(calls_per_minute=20):
    """Rate limiting decorator"""
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

class AIService:
    @staticmethod
    @rate_limit(calls_per_minute=20)
    def generate_response(user_message: str, conversation_history: list = None) -> str:
        # ... existing implementation
        pass
```

### 3. Caching for Frequent Queries

```python
# educhat/utils/cache.py

from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def cached_ai_response(query_hash: str, query: str):
    """Cache AI responses for identical queries"""
    from educhat.services.ai_service import AIService
    return AIService.generate_response(query)

def get_cached_response(query: str) -> str:
    """Get cached response or generate new one"""
    query_hash = hashlib.md5(query.encode()).hexdigest()
    return cached_ai_response(query_hash, query)
```

### 4. Error Tracking with Sentry (Optional)

```python
# Add to educhat/__init__.py

import sentry_sdk
import os

if os.getenv('ENVIRONMENT') == 'production':
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )
```

---

## 🔍 Monitoring & Maintenance

### Render Dashboard Monitoring

1. **Logs:** View real-time logs in Render dashboard
2. **Metrics:** Monitor CPU, memory, and request counts
3. **Events:** Track deployments and service restarts
4. **Health Checks:** Configure custom health check endpoint

### Custom Health Check Endpoint

```python
# educhat/pages/health.py

import reflex as rx
from educhat.services.database import db

def health_check() -> dict:
    """Health check endpoint for monitoring"""
    try:
        # Test database connection
        db.command('ping')
        
        return {
            "status": "healthy",
            "database": "connected",
            "app_version": os.getenv('APP_VERSION', '1.0.0')
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
```

### External Monitoring Tools

1. **UptimeRobot** (Free):
   - Create account at [uptimerobot.com](https://uptimerobot.com/)
   - Add monitor for `https://educhat.onrender.com/health`
   - Set check interval: 5 minutes
   - Configure email alerts

2. **Render Notifications:**
   - Go to Render dashboard → Service → Notifications
   - Add email for deployment notifications
   - Enable failure alerts

---

## 🐛 Troubleshooting

### Issue: Build fails with "Module not found"
**Solution:**
```bash
# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Issue: App crashes on startup
**Solution:**
- Check logs in Render dashboard
- Verify all environment variables are set
- Test MongoDB connection string
- Check OpenAI API key validity

### Issue: Slow cold starts (free tier)
**Solution:**
- Upgrade to paid tier ($7/mo) to prevent sleeping
- Or: Implement a "keep-alive" ping service
  ```bash
  # Use cron-job.org to ping your app every 10 minutes
  # URL: https://educhat.onrender.com/health
  ```

### Issue: "Memory limit exceeded"
**Solution:**
- Optimize memory usage in code
- Reduce concurrent connections
- Upgrade to paid tier with more RAM
- Implement pagination for large datasets

---

## 📈 Scaling Considerations

### When to Upgrade from Free Tier

Upgrade to paid tier ($7/mo) when:
- ✅ You have consistent traffic (no need for cold starts)
- ✅ Free tier is sleeping too often
- ✅ Need more RAM/CPU for performance
- ✅ Response times are slow

### Horizontal Scaling (Future)

For high traffic (1000+ concurrent users):
1. **Load Balancer:** Use Render's load balancing
2. **Database:** Upgrade MongoDB Atlas tier
3. **Caching:** Implement Redis for session storage
4. **CDN:** Use Cloudflare for static assets
5. **Multiple Instances:** Scale to multiple Render services

---

## 🔐 Security Checklist

- [ ] All API keys stored in environment variables (not in code)
- [ ] MongoDB network access restricted to Render IPs
- [ ] HTTPS enabled (automatic on Render)
- [ ] Content Security Policy (CSP) headers configured
- [ ] Rate limiting implemented for API endpoints
- [ ] Input validation and sanitization
- [ ] Regular dependency updates (check for CVEs)
- [ ] Database backups enabled in MongoDB Atlas
- [ ] Error messages don't expose sensitive information

---

## 🎯 Deployment Checklist

### Pre-Deployment
- [ ] All code tested locally
- [ ] Tests passing on staging branch
- [ ] Environment variables documented
- [ ] Database collections created
- [ ] MongoDB Atlas configured
- [ ] OpenAI API key obtained
- [ ] `render.yaml` configured
- [ ] `requirements.txt` up to date
- [ ] `.gitignore` configured properly

### During Deployment
- [ ] Push code to main branch
- [ ] Monitor build logs in Render
- [ ] Check for build errors
- [ ] Wait for deployment completion
- [ ] Verify app is accessible

### Post-Deployment
- [ ] Test all core features
- [ ] Verify database connections
- [ ] Test AI responses
- [ ] Check responsive design
- [ ] Monitor error logs
- [ ] Set up uptime monitoring
- [ ] Configure custom domain (optional)
- [ ] Share app URL with test users

---

## 📞 Support & Resources

- **Render Documentation:** [render.com/docs](https://render.com/docs)
- **Reflex Documentation:** [reflex.dev/docs](https://reflex.dev/docs)
- **Render Community:** [community.render.com](https://community.render.com/)
- **MongoDB Atlas Support:** [mongodb.com/docs/atlas](https://www.mongodb.com/docs/atlas/)

---

## 🔄 Maintenance Schedule

### Daily
- Monitor error logs
- Check uptime status

### Weekly
- Review analytics
- Check database performance
- Monitor API usage/costs

### Monthly
- Update dependencies
- Security audit
- Database backup verification
- User feedback review

### Quarterly
- Performance optimization review
- Cost analysis
- Feature roadmap review
- Scale infrastructure if needed

---

**Deployment guide complete! Your EduChat app is ready for production hosting on Render. 🚀**

**Production URL:** `https://educhat.onrender.com`
