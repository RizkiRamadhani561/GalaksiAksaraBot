# 📑 GalaksiAksaraBot - Complete File Index

Full project manifest dengan deskripsi setiap file.

---

## 🗂️ Project Structure

```
galaxi_aksara_bot/
│
├── 🤖 Source Code
│   ├── bot.py                 # Main bot application
│   ├── db.py                  # Database management
│   ├── personality.py         # Personality engine
│   ├── ai_engine.py          # AI/Ollama integration
│   └── styles.py             # Style management
│
├── 📋 Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment template
│   ├── .env                   # Actual env (don't commit)
│   ├── .gitignore             # Git ignore rules
│   ├── Dockerfile             # Container build
│   └── docker-compose.yml     # Docker Compose setup
│
├── 🔧 Setup & Tools
│   └── setup.sh               # Automated setup script
│
├── 📚 Documentation
│   ├── README.md              # Complete documentation
│   ├── QUICKSTART.md          # Quick start guide
│   ├── DEPLOYMENT.md          # Render deployment
│   ├── ADVANCED.md            # Advanced configuration
│   ├── TESTING.md             # Testing & QA
│   ├── ARCHITECTURE.md        # Technical architecture
│   └── INDEX.md               # This file
│
├── 💾 Runtime Files (Generated)
│   ├── galaxi_aksara.db       # SQLite database
│   └── bot.log                # Application logs
│
└── 📝 Project Files
    └── .git/                  # Git history (after init)
```

---

## 📄 Files Description

### Source Code Files

#### `bot.py` (Main Application)
**Size:** ~400 lines
**Purpose:** Bot core, command handlers, message routing

**Key Classes:**
- `GalaksiAksaraBot`: Main bot class

**Key Functions:**
- `cmd_start()`: /start command
- `cmd_romantis()`, `cmd_islami()`, `cmd_dark()`: Style commands
- `cmd_status()`: User profile display
- `handle_message()`: Main message handler
- `post_daily_poem()`: Daily poem posting

**Dependencies:**
- python-telegram-bot
- asyncio
- Custom: db, ai_engine, personality, styles

**Usage:**
```bash
python bot.py
```

---

#### `db.py` (Database Layer)
**Size:** ~350 lines
**Purpose:** SQLite database operations

**Key Classes:**
- `Database`: Database connection & operations

**Key Methods:**
- `init_user()`: Create new user
- `save_message()`: Store chat message
- `get_chat_history()`: Retrieve context
- `update_personality()`: Update metrics
- `add_memory_tag()`: Track emotions
- `cleanup_old_messages()`: Maintenance

**Tables Managed:**
- `chat_history`: Messages
- `user_profile`: User metrics
- `memory_tags`: Emotional themes
- `user_preferences`: User settings

**Dependencies:**
- sqlite3
- logging

---

#### `personality.py` (Relationship Engine)
**Size:** ~250 lines
**Purpose:** User personality tracking & analysis

**Key Classes:**
- `PersonalityEngine`: Personality management

**Key Methods:**
- `analyze_and_update()`: Main analysis
- `_detect_emotions()`: Emotion extraction
- `_calculate_closeness_increase()`: Relationship growth
- `_calculate_depth_increase()`: Complexity tracking

**Tracked Metrics:**
- Closeness (0-100): Relationship depth
- Depth (0-100): Conversation complexity
- Mood: Current emotional state
- Memory tags: Emotional themes

**Dependencies:**
- db.Database
- logging

---

#### `ai_engine.py` (AI Integration)
**Size:** ~450 lines
**Purpose:** Gemini integration & response generation

**Key Classes:**
- `AIEngine`: AI operations

**Key Methods:**
- `generate_response()`: Main response generation
- `_build_prompt()`: Sophisticated prompt creation
- `_call_gemini()`: Gemini API wrapper
- `_get_fallback_response()`: Template fallback
- `generate_daily_poem()`: Daily poem generation

**Features:**
- Advanced prompt engineering
- Style-specific instructions
- Personality context integration
- Graceful fallback mechanism
- Timeout handling

**Dependencies:**
- google-genai
- asyncio
- json
- logging

**External Services:**
- Google Gemini API

---

#### `styles.py` (Style Management)
**Size:** ~80 lines
**Purpose:** User style preferences

**Key Classes:**
- `StyleManager`: Style operations

**Supported Styles:**
- `romantis`: Soft, warm, romantic
- `islami`: Spiritual, reflective
- `dark`: Silent, deep, acceptance
- `default`: Natural, poetic

**Key Methods:**
- `set_user_style()`: Change style
- `get_user_style()`: Get current style
- `is_valid_style()`: Validate style

**Dependencies:**
- logging

---

### Configuration Files

#### `requirements.txt`
Lists all Python package dependencies:
```
python-telegram-bot==21.3
requests==2.31.0
APScheduler==3.10.4
python-dotenv==1.0.0
```

**Usage:**
```bash
pip install -r requirements.txt
```

---

#### `.env.example`
Template for environment variables.

**Variables:**
- `TELEGRAM_BOT_TOKEN`: Bot token from @BotFather
- `TELEGRAM_CHANNEL_ID`: Channel for daily posts
- `GEMINI_API_KEY`: Gemini API key
- `GEMINI_MODEL`: Gemini model name
- `DAILY_POST_TIME`: Schedule time
- `LOG_LEVEL`: Logging level

**Usage:**
```bash
cp .env.example .env
# Edit .env with your values
```

---

#### `.env` (Not in Repo)
Your actual environment variables. Git-ignored.

---

#### `.gitignore`
Specifies files not tracked by Git:
- `.env` files
- `*.db` database files
- Python cache (`__pycache__`)
- Virtual environment (`venv/`)
- Logs (`*.log`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`, `Thumbs.db`)

---

#### `Dockerfile`
Container build specification.

**Base Image:** `python:3.11-slim`

**What it does:**
1. Installs system dependencies
2. Installs Python packages from requirements.txt
3. Copies application code
4. Sets up health check
5. Runs `python bot.py`

**Usage:**
```bash
docker build -t galaxi-aksara .
docker run galaxi-aksara
```

---

#### `docker-compose.yml`
Orchestrates the bot container with environment variables.

**Services:**
- `bot`: Bot application

**Features:**
- Health checks
- Volume persistence
- Network isolation
- Environment variables
- Auto-restart

**Usage:**
```bash
docker-compose up -d
docker-compose logs -f bot
docker-compose down
```

---

### Setup & Tools

#### `setup.sh`
Automated setup script with multiple commands.

**Commands:**
- `bash setup.sh init`: Initialize project
- `bash setup.sh check-gemini`: Check Gemini configuration
- `bash setup.sh test`: Run tests
- `bash setup.sh docker`: Docker setup
- `bash setup.sh run`: Run bot
- `bash setup.sh full`: Full setup

**Features:**
- Colored output
- Error handling
- Step-by-step guidance
- Dependency checking

**Usage:**
```bash
chmod +x setup.sh
bash setup.sh full
```

---

### Documentation Files

#### `README.md` (Complete Guide)
**Sections:**
1. Setup Lokal - Local development setup
2. Konfigurasi Gemini AI - Gemini setup
3. Environment Variables - Configuration
4. Cara Menjalankan - Running the bot
5. Deployment ke Render - Cloud deployment
6. Architecture & Features - System overview
7. Troubleshooting - Common issues

**When to read:**
- First time setup
- Deployment guidance
- Issue resolution

---

#### `QUICKSTART.md` (Fast Start)
**Content:**
- Minimal setup (5 minutes)
- Docker alternative
- Basic troubleshooting
- Quick tips

**When to read:**
- Want quick start
- Already familiar with bot
- Troubleshooting single issue

**Length:** ~100 lines (brief)

---

#### `DEPLOYMENT.md` (Render Guide)
**Sections:**
1. Prerequisites
2. Telegram credentials
3. GitHub setup
4. Render deployment
5. Environment variables
6. Gemini deployment notes
7. Testing
8. Monitoring
9. Troubleshooting
10. Pricing

**When to read:**
- Deploying to production
- Using Render
- Setting up Gemini credentials

**Length:** ~500 lines (detailed)

---

#### `ADVANCED.md` (Customization)
**Sections:**
1. Personality customization
2. Response style tuning
3. AI engine configuration
4. Database optimization
5. Performance tuning
6. Security hardening
7. Scaling strategies
8. Advanced features

**When to read:**
- Want to customize bot
- Optimize performance
- Add new features
- Advanced configuration

**Length:** ~600 lines

---

#### `TESTING.md` (QA Guide)
**Sections:**
1. Test scenarios (basic to advanced)
2. Telegram integration tests
3. Security testing
4. Performance testing
5. Debugging checklist
6. Unit tests template
7. Pre-deployment checklist

**When to read:**
- Before deployment
- Troubleshooting issues
- Quality assurance
- Setting up tests

**Length:** ~400 lines

---

#### `ARCHITECTURE.md` (Technical Design)
**Sections:**
1. System design goals
2. System architecture (diagram)
3. Module structure
4. Database schema
5. Request flow
6. Personality system workflow
7. AI response generation
8. Error handling
9. Scalability analysis
10. Performance profile
11. Technology stack

**When to read:**
- Understanding system design
- Contributing code
- Complex troubleshooting
- Architecture decisions

**Length:** ~800 lines

---

#### `INDEX.md` (This File)
Complete file manifest with descriptions.

---

### Runtime Files (Generated)

#### `galaxi_aksara.db`
SQLite database file. Generated on first run.

**Tables:**
- `chat_history`: User & bot messages
- `user_profile`: User metrics
- `memory_tags`: Emotional themes
- `user_preferences`: User settings

**Size:** ~50KB for 100 users

**Management:**
```bash
# View structure
sqlite3 galaxi_aksara.db ".schema"

# Export data
sqlite3 galaxi_aksara.db ".dump" > backup.sql

# Cleanup old messages
# In Python: db.cleanup_old_messages(days=30)
```

---

#### `bot.log`
Application log file. Auto-created on startup.

**Content:**
- Debug information
- Error messages
- Success confirmations
- Performance metrics

**View:**
```bash
tail -f bot.log
cat bot.log | grep ERROR
```

**Cleanup:**
```bash
rm bot.log  # Delete and restart bot
```

---

## 📊 File Statistics

| File | Lines | Type | Purpose |
|------|-------|------|---------|
| bot.py | 400 | Code | Main application |
| db.py | 350 | Code | Database |
| personality.py | 250 | Code | Personality |
| ai_engine.py | 450 | Code | AI integration |
| styles.py | 80 | Code | Style management |
| **Total Code** | **1,530** | | |
| requirements.txt | 4 | Config | Dependencies |
| .env.example | 10 | Config | Environment |
| Dockerfile | 20 | Config | Container |
| docker-compose.yml | 40 | Config | Compose |
| setup.sh | 250 | Tool | Setup script |
| README.md | 600 | Doc | Complete guide |
| QUICKSTART.md | 100 | Doc | Quick start |
| DEPLOYMENT.md | 500 | Doc | Deployment |
| ADVANCED.md | 600 | Doc | Advanced config |
| TESTING.md | 400 | Doc | Testing |
| ARCHITECTURE.md | 800 | Doc | Architecture |
| **Total Docs** | **4,000** | | |
| **Grand Total** | **~5,500** | | Lines of code & docs |

---

## 🔗 File Dependencies

```
bot.py
├── requires: db.py
├── requires: personality.py
├── requires: ai_engine.py
├── requires: styles.py
├── requires: python-telegram-bot
└── requires: .env

db.py
├── uses: sqlite3
└── imports: logging

personality.py
├── requires: db.py
└── imports: logging

ai_engine.py
├── uses: requests (Ollama API)
├── uses: asyncio
└── imports: logging

styles.py
└── imports: logging
```

---

## 📦 Setup Checklist

When setting up, you need:

**Before Setup:**
- [ ] Python 3.9+
- [ ] Git (for version control)
- [ ] Google Gemini API key

**During Setup:**
- [ ] Clone/download project
- [ ] Run `bash setup.sh full`
- [ ] Copy `.env.example` to `.env`
- [ ] Edit `.env` with credentials
- [ ] Run bot: `python bot.py`

**Generated Files:**
- [ ] `galaxi_aksara.db` (created automatically)
- [ ] `bot.log` (created automatically)
- [ ] `venv/` (Python virtual environment, if using)

---

## 🎯 Which File to Edit?

| Need to... | Edit file |
|-----------|-----------|
| Change personality calculation | `personality.py` |
| Customize responses | `ai_engine.py` |
| Add new style | `styles.py` + `bot.py` |
| Modify database | `db.py` |
| Change commands | `bot.py` |
| Adjust schedule | `.env` (DAILY_POST_TIME) |
| Change Gemini model | `.env` (GEMINI_MODEL) |
| Add custom prompts | `ai_engine.py` (_build_prompt) |
| Fallback poems | `ai_engine.py` (fallback_poems) |
| Email/SMS | Would need new integration |

---

## 📈 Usage Patterns

### Development:
```
Edit code → Run bot.py → Test in Telegram → Iterate
```

### Deployment:
```
Setup .env → docker-compose up → Monitor logs
```

### Maintenance:
```
Monitor bot.log → Check database → Update code → Restart
```

### Scaling:
```
Current: SQLite → Future: PostgreSQL
```

---

## 🔒 Files to Keep Secure

⚠️ **Never commit to GitHub:**
- `.env` (has token!)
- `*.db` (has user data)
- `*.log` (has sensitive info)
- `venv/` (local environment)

✅ **Safe to commit:**
- `.py` source files
- `.env.example` (template)
- `.gitignore`
- Documentation (`.md` files)
- `Dockerfile`, `docker-compose.yml`
- `requirements.txt`

---

## 💡 Quick Navigation

**Getting Started:** Start with `QUICKSTART.md`
**Complete Setup:** Read `README.md`
**Deploy to Cloud:** Follow `DEPLOYMENT.md`
**Customize Bot:** Check `ADVANCED.md`
**Troubleshoot Issues:** See `README.md#troubleshooting`
**Understand Architecture:** Read `ARCHITECTURE.md`
**Test Before Deploy:** Follow `TESTING.md`

---

## 📞 File-Specific Support

Having issues?

1. **Check `README.md` first** - Most questions answered
2. **See `TROUBLESHOOTING` section**
3. **Review `bot.log` for errors**
4. **Check `ADVANCED.md` for customization**
5. **Read `ARCHITECTURE.md` for design questions**

---

**Happy exploring!** 🌙✨

All files are documented, modular, and ready to extend.
