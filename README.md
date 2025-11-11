# 🎓 EduChat - AI Chatbot voor Surinaams Onderwijs

**Welkom bij EduChat!** Een slimme AI-gestuurde chatbot die Surinaamse studenten helpt bij het vinden van opleidingen, toelatingseisen, deadlines en studiekeuzebegeleiding.

![EduChat Logo](assets/logo.png)

## 🌟 Project Overzicht

EduChat is een moderne, AI-aangedreven educatieve assistent speciaal ontworpen voor het Surinaamse onderwijssysteem. Via een natuurlijke conversatie kunnen studenten:

- 🏫 Informatie vinden over opleidingen en instellingen
- 📋 Toelatingseisen en inschrijvingsprocedures ontdekken
- 📅 Deadlines en belangrijke data tracken
- 🔍 Studies vergelijken en de beste keuze maken
- 💬 Persoonlijke studie-advies krijgen

## 🎯 Belangrijkste Kenmerken

### ✅ Must-Have (MVP - Phase 1)
- **Natuurlijke Chat Interface** - Intuïtieve conversatie met AI
- **AI-Gegenereerde Antwoorden** - Context-bewuste, relevante antwoorden
- **Gespreksgeschiedenis** - Behoud van context binnen sessie
- **Database Logging** - Opslag van vragen en antwoorden
- **Responsive Design** - Werkt op mobiel, tablet en desktop
- **Suriname Focus** - 100% gericht op Surinaams onderwijs

### 🎨 Should-Have (Phase 2)
- **Onboarding Quiz** - Studiekeuzetest voor personalisatie
- **Feedbacksysteem** - Thumbs up/down voor antwoorden
- **Foutafhandeling** - Duidelijke foutmeldingen en suggesties
- **Snelle Reacties** - <2 seconden responstijd

### 📊 Could-Have (Phase 3)
- **Programma Vergelijking** - Side-by-side vergelijking van studies
- **Actuele Data** - Real-time informatie over instellingen
- **Analytics Dashboard** - Inzicht in gebruikersgedrag

### 🚀 Premium Features (Phase 4)
- **User Accounts** - Persistente gespreksgeschiedenis
- **Herinneringen** - Deadline notificaties
- **Meertalig** - Nederlands en Engels ondersteuning

## 🛠️ Technologie Stack

| Component | Technologie | Reden |
|-----------|-------------|-------|
| **Framework** | Reflex (Python) | Volledige full-stack in één taal |
| **Database** | Supabase (PostgreSQL) | Open-source, real-time, gratis tier |
| **AI** | OpenAI / Google AI | Geavanceerde taalmodellen |
| **Hosting** | Render | Gratis tier, automatische CI/CD |

## 🚀 Deployment Status

✅ **Production Ready!** This project is configured for deployment to Render.

- **Configuration**: `render.yaml` ✅
- **Database**: Supabase PostgreSQL ✅  
- **CI/CD**: GitHub Actions ✅
- **Documentation**: Complete deployment guides ✅

### Quick Deploy

1. Push to GitHub
2. Connect to Render
3. Add environment variables
4. Deploy! 🎉

See [`RENDER_DEPLOYMENT.md`](RENDER_DEPLOYMENT.md) for detailed instructions.
| **Version Control** | GitHub | Gestructureerde branches (dev/staging/main) |

## 📁 Project Structuur

```
EduChat/
├── .github/
│   └── workflows/          # CI/CD pipelines
├── educhat/                # Hoofdapplicatie
│   ├── components/         # UI componenten
│   │   ├── shared/         # Gedeelde componenten (buttons, inputs)
│   │   ├── sidebar.py      # Zijbalk met conversaties
│   │   ├── chat_container.py
│   │   └── message_bubble.py
│   ├── pages/              # Pagina's
│   │   ├── index.py        # Chat interface
│   │   ├── onboarding.py   # Quiz interface
│   │   └── admin.py        # Analytics dashboard
│   ├── services/           # Backend services
│   │   ├── database.py     # MongoDB client
│   │   ├── ai_service.py   # OpenAI integratie
│   │   └── rag_service.py  # RAG implementatie
│   ├── state/              # State management
│   │   ├── app_state.py
│   │   └── onboarding_state.py
│   ├── utils/              # Helper functies
│   └── styles/             # Styling en thema's
├── data/                   # Data en scripts
│   ├── instellingen.json   # Surinaamse instellingen
│   └── scripts/
│       └── import_data.py
├── tests/                  # Unit en integratie tests
├── docs/                   # Documentatie
│   ├── prd.md
│   ├── design-requirements.md
│   ├── project-checklist.md
│   ├── setup-guide.md
│   └── render-deployment.md
├── .env.example            # Environment variables template
├── .gitignore
├── requirements.txt        # Python dependencies
├── rxconfig.py             # Reflex configuratie
├── render.yaml             # Render deployment config
└── README.md               # Dit bestand
```

## 🚀 Quick Start

### Vereisten

- Python 3.11+
- Node.js 18+
- Git
- MongoDB Atlas account
- OpenAI API key

### Installatie

1. **Clone de repository**
```bash
git clone https://github.com/LeoRanoe/EduChat.git
cd EduChat
```

2. **Maak virtuele omgeving aan**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
```

3. **Installeer dependencies**
```bash
pip install -r requirements.txt
```

4. **Configureer environment variables**
```bash
cp .env.example .env
# Bewerk .env met jouw API keys en database URI
```

5. **Initialiseer Reflex**
```bash
reflex init
```

6. **Start development server**
```bash
reflex run
```

7. **Open browser**
```
http://localhost:3000
```

## 📚 Documentatie

Volledige documentatie is beschikbaar in de `docs/` folder:

- **[PRD (Product Requirements Document)](docs/prd.md)** - Complete productspecificatie
- **[Design Requirements](docs/design-requirements.md)** - UI/UX richtlijnen en design system
- **[Project Checklist](docs/project-checklist.md)** - Complete ontwikkel checklist met alle taken
- **[Setup Guide](docs/setup-guide.md)** - Stap-voor-stap ontwikkelomgeving setup
- **[Render Deployment](docs/render-deployment.md)** - Productie deployment strategie

## 🎨 Design System

### Kleurenpalet
- **Primair Groen:** `#228B22`
- **Achtergrond:** `#FFFFFF`
- **Chat Bubble (Gebruiker):** `#D4F1D4`
- **Chat Bubble (Bot):** `#FFFFFF` met border
- **Text:** `#2D2D2D`

### Typografie
- **Font:** Sans-serif (Inter/Roboto)
- **H1:** 48-64px (bold)
- **Body:** 16px (regular)

Zie [design-requirements.md](docs/design-requirements.md) voor complete design specificaties.

## 🔐 Beveiliging

- ✅ Alle API keys via environment variables
- ✅ HTTPS verplicht in productie
- ✅ MongoDB network access beperkt
- ✅ Input sanitization en validatie
- ✅ Rate limiting voor API calls
- ✅ Geen persoonlijke data opslag (GDPR compliant)

## 🧪 Testing

```bash
# Run unit tests
pytest tests/ -v

# Run linting
flake8 educhat/ --max-line-length=120

# Run type checking
mypy educhat/
```

## 📊 Ontwikkel Roadmap

### ✅ Phase 1: Core MVP (Weken 1-3)
- [x] Project setup
- [ ] Chat interface
- [ ] AI integratie
- [ ] MongoDB logging
- [ ] Render deployment

### 🔄 Phase 2: UX Improvements (Weken 4-5)
- [ ] Onboarding quiz
- [ ] Feedback systeem
- [ ] Error handling
- [ ] Performance optimalisatie

### 📈 Phase 3: Data Integration (Weken 6-8)
- [ ] Surinaamse onderwijsdata
- [ ] RAG implementatie
- [ ] Programma vergelijking
- [ ] Analytics dashboard

### 🚀 Phase 4: Premium Features (Weken 9-12)
- [ ] User accounts
- [ ] Herinneringen
- [ ] Meertaligheid
- [ ] Advanced analytics

## 🤝 Bijdragen

We verwelkomen bijdragen! Volg deze stappen:

1. Fork de repository
2. Maak een feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit je changes (`git commit -m 'Add AmazingFeature'`)
4. Push naar de branch (`git push origin feature/AmazingFeature`)
5. Open een Pull Request

### Branch Strategie
- `main` - Productie (deploy naar Render)
- `staging` - QA testing
- `dev` - Actieve ontwikkeling

## 📈 Success Metrics

| Metric | Target |
|--------|--------|
| **Correcte antwoorden** | >85% |
| **Responstijd** | ≤2 seconden |
| **Uptime** | 99%+ |
| **Gebruikerstevredenheid** | 80%+ positief |
| **Actieve gebruikers (maand 1)** | 100+ |

## 📞 Contact & Support

- **Project Owner:** Leo Ranoe
- **GitHub:** [LeoRanoe/EduChat](https://github.com/LeoRanoe/EduChat)
- **Issues:** [GitHub Issues](https://github.com/LeoRanoe/EduChat/issues)

## 📄 Licentie

Dit project is gelicenseerd onder de MIT License - zie [LICENSE](LICENSE) bestand voor details.

## 🙏 Credits

- **Reflex Framework** - [reflex.dev](https://reflex.dev/)
- **OpenAI API** - [openai.com](https://openai.com/)
- **MongoDB Atlas** - [mongodb.com](https://www.mongodb.com/)
- **Render Hosting** - [render.com](https://render.com/)

---

**Gebouwd met ❤️ voor Surinaamse studenten**

🎓 **EduChat - Jouw studie-assistent, altijd beschikbaar**
