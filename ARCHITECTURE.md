# 🏗️ Architecture Overview

GalaksiAksaraBot - Technical Design & Architecture

---

## 🎯 System Design Goals

1. **Natural Personality** - Bot terasa hidup, tidak seperti template
2. **Learning System** - Bot belajar tentang user dari waktu ke waktu
3. **Graceful Degradation** - Works even when components fail
4. **Lightweight** - Runs on minimal resources
5. **Modular** - Easy to maintain and extend
6. **Privacy-Focused** - User data stored locally

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Telegram User                                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓ (Text Messages)
┌─────────────────────────────────────────────────────────────────┐
│                   Telegram Bot API                               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      bot.py (Main)                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ - Command Handlers (/start, /romantis, etc)              │   │
│  │ - Message Router                                          │   │
│  │ - Job Scheduler (Daily Posts)                             │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────┬──────────────┬──────────────┬────────────────────┘
              │              │              │
              ↓              ↓              ↓
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  personality │ │  ai_engine   │ │   styles     │
    │   engine     │ │              │ │   manager    │
    └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
           │                │                │
           └────────┬───────┴────────┬───────┘
                    │                │
                    ↓                ↓
           ┌─────────────────────────────────┐
           │    Database (SQLite)             │
           ├─────────────────────────────────┤
           │ • chat_history                  │
           │ • user_profile                  │
           │ • memory_tags                   │
           │ • user_preferences              │
           └─────────────────────────────────┘
                    │
                    └─────────────┬─────────────┐
                                  │             │
                                  ↓             ↓
                           ┌──────────────┐ ┌──────────────┐
                           │ Ollama API   │ │ Fallback     │
                           │ (Local LLM)  │ │ Poems        │
                           └──────────────┘ └──────────────┘
```

---

## 📦 Module Structure

### 1. **bot.py** - Application Core
```
Responsibilities:
- Initialize Telegram bot
- Handle all commands
- Route messages
- Manage job scheduler
- Error handling

Key Classes:
- GalaksiAksaraBot: Main bot class

Key Methods:
- handle_message(): Route user messages
- cmd_start(): Intro command
- cmd_romantis/islami/dark(): Style commands
- post_daily_poem(): Schedule poems
```

### 2. **db.py** - Data Persistence
```
Responsibilities:
- SQLite database management
- User profile tracking
- Chat history storage
- Emotional memory tags
- Database cleanup

Key Class:
- Database: DB operations

Key Tables:
- chat_history (user messages & bot responses)
- user_profile (personality metrics)
- memory_tags (emotional themes)
- user_preferences (style, length)

Key Methods:
- init_user(): Create new user profile
- save_message(): Store chat
- get_chat_history(): Retrieve context
- update_personality(): Update metrics
- add_memory_tag(): Track emotions
```

### 3. **personality.py** - Relationship Engine
```
Responsibilities:
- Analyze user messages
- Update personality metrics
- Detect emotions
- Track conversation depth
- Generate contextual descriptions

Key Class:
- PersonalityEngine: Personality tracking

Key Metrics:
- closeness (0-100): Relationship depth
- depth (0-100): Conversation complexity
- mood: Detected emotional state

Key Methods:
- analyze_and_update(): Main analysis
- _detect_emotions(): NLP-like emotion extraction
- _calculate_closeness_increase(): Relationship growth
- _calculate_depth_increase(): Conversation complexity
- get_response_tone(): Determine response style
```

### 4. **ai_engine.py** - AI Generation
```
Responsibilities:
- Generate natural responses
- Integrate Ollama API
- Advanced prompt engineering
- Fallback mechanism
- Daily poem generation

Key Class:
- AIEngine: AI operations

Key Components:
- Prompt builder with personality context
- Ollama API caller (async)
- Fallback poem library
- Style-specific instructions

Key Methods:
- generate_response(): Main response generation
- _build_prompt(): Sophisticated prompt creation
- _call_ollama(): Ollama API call
- _get_fallback_response(): Template poem fallback
- generate_daily_poem(): Daily poem generation
```

### 5. **styles.py** - Style Management
```
Responsibilities:
- Manage user style preferences
- Validate style values
- Provide style descriptions

Key Class:
- StyleManager: Style handling

Supported Styles:
- romantis: Soft, warm, romantic
- islami: Spiritual, reflective
- dark: Silent, deep, acceptance
- default: Poetic, natural

Key Methods:
- set_user_style(): Change user style
- get_user_style(): Retrieve user style
- is_valid_style(): Validate style
```

---

## 💾 Database Schema

### Table: chat_history
```sql
id (INTEGER PRIMARY KEY)
user_id (INTEGER)
role (TEXT) - 'user' or 'bot'
content (TEXT) - Full message
timestamp (DATETIME) - When sent

Purpose: Store all messages for context
Index: (user_id, timestamp) for quick retrieval
```

### Table: user_profile
```sql
user_id (INTEGER PRIMARY KEY)
username (TEXT)
closeness (INTEGER 0-100) - Relationship depth
depth (INTEGER 0-100) - Conversation complexity
mood (TEXT) - Last detected emotion
style (TEXT) - Preferred response style
first_interaction (DATETIME)
last_interaction (DATETIME)

Purpose: Store user personality metrics
```

### Table: memory_tags
```sql
id (INTEGER PRIMARY KEY)
user_id (INTEGER)
tag (TEXT) - Emotional theme
weight (INTEGER 0-100) - Importance weight
first_mentioned (DATETIME)
last_mentioned (DATETIME)

Purpose: Track emotional topics
Supports: Emotion detection, context enrichment
```

### Table: user_preferences
```sql
user_id (INTEGER PRIMARY KEY)
preferred_style (TEXT)
response_length (TEXT)
poetry_preference (TEXT)

Purpose: Store user preferences
```

---

## 🔄 Request Flow

### User sends message:

```
1. User sends message in Telegram
   ↓
2. Telegram API → bot.py (handle_message)
   ↓
3. Show typing indicator
   ↓
4. Database: Save user message
   ↓
5. Personality Engine: Analyze message
   │ - Detect emotions
   │ - Update closeness/depth
   │ - Extract memory tags
   ↓
6. Database: Update user profile & tags
   ↓
7. Retrieve:
   - Chat history (last 10 messages)
   - User profile (closeness, mood, depth)
   - User style preference
   - Memory tags (top 5)
   ↓
8. AI Engine: Generate response
   │ - Build sophisticated prompt
   │ - Include personality context
   │ - Call Ollama (with timeout)
   │ - If timeout/error → use fallback
   ↓
9. Database: Save bot response
   ↓
10. Telegram API: Send response to user
    ↓
11. Add delay for natural feel
    ↓
12. Message sent to user
```

---

## 🧠 Personality System Workflow

### How Closeness Increases:

```
User sends message
    ↓
_calculate_closeness_increase():
    - Base: +2 per message
    - Long (>50 chars): +1
    - Very long (>100 chars): +1
    - Emotional content: +2
    - Contains question (?): +1
    ↓
Example: "Aku lelah dan sedih, bagaimana bisa tahan?" (54 chars)
    - Base: +2
    - Emotions (lelah, sedih): +2
    - Question mark: +1
    = Total: +5 closeness increase
    ↓
Update user_profile.closeness += 5
```

### How Depth Increases:

```
User sends message with deep topics
    ↓
_calculate_depth_increase():
    - Check depth_keywords
    - Count sentences
    ↓
Keywords include:
- mengapa, bagaimana, apa arti (questions)
- filosofi, makna (concepts)
- diri, jiwa, hati, perasaan (emotions)
    ↓
Example: "Mengapa aku selalu merasa sedih tentang makna hidup?"
    - "mengapa": +1
    - "makna": +1
    - 1 sentence → no bonus
    = Total: +2 depth increase
```

### Memory Tag Extraction:

```
Message: "Aku very lonely dan merasa abandonded"

_detect_emotions():
    - "lonely" → "kesunyian"
    - "abandoned" → "kehilangan"
    
add_memory_tag("kesunyian", weight=2)
add_memory_tag("kehilangan", weight=2)

Next time user asks something:
    - Retrieve tags
    - Include in prompt
    - Response considers past emotional themes
```

---

## 🤖 AI Response Generation Workflow

### Prompt Building:

```
_build_prompt():
    
    1. System Identity
    Kamu adalah Galaksi Aksara—penyair digital...
    
    2. Relationship Context
    Status: kami sudah cukup dekat
    Closeness: 65/100
    Depth: 40/100
    Mood: sedih
    
    3. Memory Tags
    Riwayat emosional: kehilangan, dukha, rindu
    
    4. Chat History
    - Mereka: previous message...
    - Aku: previous response...
    
    5. Style Instructions
    [Style-specific prompts for romantis/islami/dark]
    
    6. Current Message
    "..." (user's latest message)
    
    7. Rules
    - 3-6 lines
    - Metaphorical
    - Natural, not template
```

### Response Generation:

```
Call Ollama:
    - Send prompt (detailed context)
    - Temperature: 0.9 (creative)
    - Top_p: 0.95 (balanced)
    - Timeout: 30 seconds
    
If success:
    → Return Ollama response
    
If timeout or error:
    → Use fallback poem
    
If fallback selected:
    → Pick based on style & emotion
    → Return template poem
```

---

## 🌪️ Error Handling Strategy

### Graceful Degradation:

```
Scenario: Ollama offline

Flow:
1. Try Ollama API call
2. Timeout occurs (30 sec)
3. Catch exception
4. Log error: "Cannot connect to Ollama"
5. Return fallback poem
6. Send to user: "Seolah kata-kata lepas..."
7. User experience: Unaffected! ✓

Result: Bot still functional
```

### Error Levels:

```
CRITICAL (Bot crashes):
- Database file corrupted
- Invalid token
- Out of memory

HANDLED (Graceful degradation):
- Ollama timeout → fallback
- Model not found → fallback
- API rate limit → retry with backoff
- Invalid user input → safe handling

LOGGED (Monitor):
- Long response times
- Database query errors
- Personality analysis failures
```

---

## 📈 Scalability Considerations

### Current Limitations:

```
SQLite:
- ~1000 users: No issue
- ~10000 users: Getting slow
- ~100000 users: Needs migration

Memory:
- Current: ~50MB with data
- Per user: ~1MB
- 1000 users: ~1GB RAM

Performance:
- Response time: 2-5 sec (Ollama)
- API calls: 1 per message
- Database: ~50ms per query
```

### Scaling Path:

```
Phase 1 (Current):
- SQLite database
- Single bot instance
- Fallback for Ollama

Phase 2 (100+ users):
- Migrate to PostgreSQL
- Add caching layer (Redis)
- Monitor performance

Phase 3 (1000+ users):
- Load balancing
- Message queue (RabbitMQ)
- Distributed Ollama
- Analytics database

Phase 4 (10000+ users):
- Microservices
- Database sharding
- Message broker
- CDN for content
```

---

## 🔐 Security Architecture

### Data Storage:

```
Sensitive data:
- Token: .env file (gitignored)
- User messages: Local SQLite
- User emotions: Local SQLite
- User IDs: Local SQLite

No data:
- Sent to external servers
- Stored in cloud
- Shared with third parties
```

### Telegram Security:

```
Token handling:
- Never logged
- Loaded from .env
- Never exposed in errors
- Checked before use

API calls:
- HTTPS only
- Timeout protection
- Rate limiting (can be added)
- Input validation
```

---

## 📊 Performance Profile

### Memory Usage:

```
Base:
- Python runtime: ~30MB
- Bot code: ~5MB
- Database (1000 users): ~50MB
Total: ~85MB

Per user addition:
- Profile data: ~1KB
- Chat history (100 msgs): ~50KB
- Memory tags: ~2KB
Total per user: ~53KB
```

### Response Time:

```
With Ollama:
- Message received: 0ms
- Parse & DB save: 10ms
- Personality analysis: 5ms
- Prompt building: 5ms
- Ollama call: 2000-5000ms (LLM)
- DB save response: 10ms
- Send to Telegram: 50ms
Total: 2-5 seconds

Without Ollama (fallback):
- Message received: 0ms
- All above except Ollama: 30ms
- Select fallback: 1ms
- Send to Telegram: 50ms
Total: <100ms
```

### Network Usage:

```
Per message:
- Received: ~1KB (user message)
- Sent: ~2KB (bot response)
- Total: ~3KB

Daily (100 messages):
- Up: 100KB
- Down: 200KB
Total: 300KB/day

Monthly (1000 messages):
- 3MB
```

---

## 🧪 Testing Architecture

```
Unit Tests:
- Database operations
- Personality calculations
- Emotion detection
- Prompt building

Integration Tests:
- Full message flow
- Ollama integration
- Daily poem generation
- User profile updates

Manual Tests:
- Telegram interface
- Command handling
- Style switching
- Multi-user scenarios
```

---

## 🚀 Deployment Architecture

### Local Development:
```
Python 3.9+ → Ollama (local) → SQLite → Telegram API
```

### Docker:
```
Bot Container → Ollama Container → Shared Network
↓
SQLite (volume mount)
```

### Render (Free):
```
Render Instance → Ollama (external or fallback)
↓
SQLite (persistent storage)
↓
Telegram API
```

### Production (Recommended):
```
Load Balancer → Bot Instances (multiple)
                      ↓
                   PostgreSQL (shared)
                      ↓
                   Ollama Server (shared)
                      ↓
                   Telegram API
```

---

## 📚 Technology Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Bot Framework | python-telegram-bot | Async, reliable, maintained |
| Async | asyncio | Built-in, efficient |
| Database | SQLite | Lightweight, no setup |
| LLM | Ollama (local) | Private, offline-capable |
| Scheduler | APScheduler | Simple, built-in |
| HTTP | requests | Standard, simple |
| Config | python-dotenv | Standard for env vars |
| Logging | logging module | Built-in |

---

**GalaksiAksaraBot - Simple yet sophisticated** 🌙✨
