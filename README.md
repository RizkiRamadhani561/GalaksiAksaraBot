# 🌙 GalaksiAksaraBot - Dokumentasi Lengkap

Bot Telegram bernama "Galaksi Aksara" dengan AI yang hidup, reflektif, dan emosional.

---

## 📋 Table of Contents
1. [Setup Lokal](#setup-lokal)
2. [Konfigurasi Ollama](#konfigurasi-ollama)
3. [Environment Variables](#environment-variables)
4. [Cara Menjalankan](#cara-menjalankan)
5. [Deployment ke Render](#deployment-ke-render)
6. [Architecture & Features](#architecture--features)
7. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Lokal

### Prerequisites
- Python 3.9+
- pip (Python package manager)
- Ollama installed locally
- Telegram Bot Token (dari @BotFather)

### Step 1: Clone atau Download Project

```bash
cd galaxi_aksara_bot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup Environment Variables

```bash
cp .env.example .env
nano .env  # atau buka dengan text editor
```

Edit file `.env` dengan nilai yang sesuai:

```env
TELEGRAM_BOT_TOKEN=6234234923:ABCD1234567890...
TELEGRAM_CHANNEL_ID=@galaksi_aksara_channel
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi
DAILY_POST_TIME=09:00
```

---

## 🧠 Konfigurasi Ollama

### Step 1: Install Ollama

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download dari https://ollama.ai

### Step 2: Download Model

Gunakan model ringan seperti `phi` atau `mistral`:

```bash
ollama pull phi
```

atau untuk model yang lebih canggih:

```bash
ollama pull mistral
ollama pull neural-chat
```

### Step 3: Jalankan Ollama Server

```bash
ollama serve
```

Server akan berjalan di `http://localhost:11434`

### Step 4: Test Ollama

```bash
curl http://localhost:11434/api/tags
```

Seharusnya menampilkan daftar model yang tersedia.

---

## 🔐 Environment Variables

### TELEGRAM_BOT_TOKEN
Dapatkan dari @BotFather di Telegram:
1. Chat dengan @BotFather
2. Kirim `/newbot`
3. Ikuti instruksi
4. Copy token yang diberikan

### TELEGRAM_CHANNEL_ID
ID atau username channel tempat bot posting puisi harian:
- Format username: `@channel_name`
- Format ID: `-1001234567890`

Untuk mendapatkan ID channel:
1. Add bot ke channel
2. Kirim pesan ke channel
3. Akses: `https://api.telegram.org/bot{TOKEN}/getUpdates`
4. Cari `chat.id` di response

### OLLAMA_URL
URL server Ollama (default: `http://localhost:11434`)

Untuk Render (cloud):
- Setup Ollama di server terpisah
- atau gunakan fallback (template poems)

### OLLAMA_MODEL
Model yang akan digunakan:
- `phi` - ringan, cepat, 2.7B parameters
- `mistral` - lebih bagus, 7B parameters
- `neural-chat` - spesialisasi chat

---

## ▶️ Cara Menjalankan

### Run Lokal

```bash
python bot.py
```

Output akan terlihat seperti:
```
2024-01-15 10:30:45,123 - root - INFO - Database initialized
2024-01-15 10:30:46,234 - root - INFO - 🌙 Galaksi Aksara bot starting...
2024-01-15 10:30:47,345 - root - INFO - Daily poem scheduler activated
```

### Test di Telegram

1. Find bot di Telegram (cari username yang dibuat di BotFather)
2. Kirim `/start`
3. Bot akan merespons dengan intro puitis
4. Chat dengan bebas
5. Bot akan selalu merespons dengan puisi

### Commands

```
/start      - Intro dan mulai percakapan
/romantis   - Ubah gaya ke romantis (lembut, hangat)
/islami     - Ubah gaya ke islami (spiritual, reflektif)
/dark       - Ubah gaya ke dark (sunyi, dalam)
/status     - Lihat profil dan tingkat kedekatan
```

---

## ☁️ Deployment ke Render

### Step 1: Push Code ke GitHub

```bash
git init
git add .
git commit -m "Initial commit: GalaksiAksaraBot"
git remote add origin https://github.com/yourusername/galaxi-aksara-bot.git
git push -u origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up dengan GitHub account
3. Connect GitHub repository

### Step 3: Create New Web Service

1. Click "New +"
2. Select "Web Service"
3. Connect GitHub repo
4. Fill form:

```
Name: galaxi-aksara-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
Instance Type: Free (atau Paid untuk production)
```

### Step 4: Environment Variables

Di Render dashboard:
1. Go ke "Environment" tab
2. Add variables:

```
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHANNEL_ID=your_channel
OLLAMA_URL=http://your-ollama-server:11434
OLLAMA_MODEL=phi
DAILY_POST_TIME=09:00
```

### Step 5: Deploy

Click "Create Web Service"

Render akan otomatis deploy dan restart service setiap ada push ke GitHub.

---

### Setup Ollama untuk Cloud Deployment

Untuk production di cloud, ada beberapa opsi:

**Option 1: Ollama di Server Terpisah**
- Setup Ollama di dedicated server (DigitalOcean, AWS, etc)
- Set `OLLAMA_URL` ke server address
- Pastikan server accessible dari Render

**Option 2: Gunakan Fallback (Recommended untuk Free Tier)**
- Bot akan otomatis fallback ke template poems
- Masih terasa natural dan puitis
- Tidak perlu setup Ollama yang rumit

**Option 3: Hybrid Approach**
- Jika Ollama timeout/offline, bot gunakan fallback
- Jika Ollama online, gunakan AI generation
- Best of both worlds

---

## 🏗️ Architecture & Features

### File Structure

```
galaxi_aksara_bot/
├── bot.py           # Main application
├── db.py            # Database management
├── personality.py   # Personality engine
├── ai_engine.py     # AI/Ollama integration
├── styles.py        # Style manager
├── requirements.txt # Dependencies
├── .env.example     # Env variables template
├── .env             # Actual env (gitignore this!)
└── galaxi_aksara.db # SQLite database (auto-created)
```

### Database Schema

**chat_history**
```sql
- id (PRIMARY KEY)
- user_id
- role (user/bot)
- content
- timestamp
```

**user_profile**
```sql
- user_id (PRIMARY KEY)
- username
- closeness (0-100)      -- relationship depth
- depth (0-100)          -- conversation depth
- mood                   -- last detected mood
- style                  -- preferred style
- first_interaction
- last_interaction
```

**memory_tags**
```sql
- id (PRIMARY KEY)
- user_id
- tag (emotion/theme)
- weight (0-100)
- first_mentioned
- last_mentioned
```

### Features

#### 1. **Personality System**
- Tracks user closeness (0-100)
- Measures conversation depth
- Detects emotional mood
- Adapts response based on relationship

#### 2. **Memory System**
- Saves chat history
- Extracts emotional themes (memory tags)
- Uses context for coherent responses
- Autocleanup after 30 days

#### 3. **Multi-Style Responses**
- **Romantis**: Lembut, hangat, penuh rindu
- **Islami**: Reflektif, spiritual, tidak menggurui
- **Dark**: Sunyi, dalam, kedalaman
- **Default**: Puitis, natural, autentik

#### 4. **AI Integration**
- Uses Ollama with local LLM
- Advanced prompt engineering
- Fallback to template poems if AI fails
- Graceful degradation

#### 5. **Daily Posts**
- Auto-generates and posts puisi harian
- Configurable schedule
- Supports both channel and group chats

#### 6. **Natural Behavior**
- Typing indicators for realistic feel
- Message delays based on content length
- Error handling with fallbacks
- Logging for monitoring

---

## 🐛 Troubleshooting

### Bot tidak respond

**Check 1: Ollama running?**
```bash
curl http://localhost:11434/api/tags
```

**Check 2: Token valid?**
- Verify token di `.env`
- Make sure no extra spaces

**Check 3: Check logs**
```bash
tail -f bot.log
```

---

### Ollama connection error

**Error: "Cannot connect to Ollama"**

Solution:
1. Make sure Ollama server running:
   ```bash
   ollama serve
   ```

2. Check URL in `.env`:
   ```
   OLLAMA_URL=http://localhost:11434
   ```

3. Test manually:
   ```bash
   curl http://localhost:11434/api/tags
   ```

Bot akan use fallback poems jika Ollama tidak available.

---

### Model not found

**Error: "Model 'phi' not found"**

Solution:
```bash
ollama pull phi
```

Check available models:
```bash
ollama list
```

---

### Database errors

**Delete dan recreate database:**
```bash
rm galaxi_aksara.db
python bot.py
```

---

### Performance issues on Render Free Tier

- Use lightweight model: `phi` instead of `mistral`
- Enable fallback (automatic)
- Consider upgrading to paid instance
- Or setup separate Ollama server

---

## 📊 Monitoring

### Check Bot Status

```bash
# See logs
tail -f bot.log

# Check database
sqlite3 galaxi_aksara.db ".tables"
```

### Performance Tips

1. **Reduce model size**: Use `phi` (2.7B) instead of larger models
2. **Cache responses**: Reuse fallback poems strategically
3. **Cleanup old data**: Run periodic cleanup:
   ```python
   db.cleanup_old_messages(days=30)
   ```

---

## 🎓 Tips for Better Results

### 1. Craft Good Prompts
Edit `ai_engine.py` untuk customize prompt
- Tambah personality traits
- Adjust style instructions
- Modify tone guidelines

### 2. Improve Memory System
- Tweak emotion detection di `personality.py`
- Add more memory tags
- Adjust closeness calculation

### 3. Fallback Poems
Edit fallback_poems di `ai_engine.py` untuk customize
- Make them more personal
- Add more variety
- Match your aesthetic

### 4. Testing Locally
```bash
# Run in debug mode
python -m pdb bot.py

# Test Ollama directly
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model":"phi","prompt":"test","stream":false}'
```

---

## 🔄 Updates & Maintenance

### Regular Tasks
- Monitor `bot.log` for errors
- Clean old messages: `db.cleanup_old_messages()`
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Test Ollama connection periodically

### Monitoring Script
```bash
#!/bin/bash
while true; do
  if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "Ollama down at $(date)" >> ollama_status.log
  fi
  sleep 300  # Check every 5 minutes
done
```

---

## 📞 Support & Debugging

### Enable Debug Logging
Edit bot.py:
```python
logging.basicConfig(level=logging.DEBUG)  # Change from INFO
```

### Test Components Individually

**Test Database:**
```python
from db import Database
db = Database()
db.init_user(123, "Test User")
print(db.get_user_profile(123))
```

**Test AI Engine:**
```python
import asyncio
from ai_engine import AIEngine
ai = AIEngine()
result = asyncio.run(ai.generate_response(...))
print(result)
```

---

## 📝 License & Attribution

GalaksiAksaraBot - A poetic Telegram bot
Inspired by the beauty of Indonesian poetry and AI creativity.

---

## 🌟 Future Enhancements

- [ ] Image generation for daily posts
- [ ] Voice messages support
- [ ] User statistics dashboard
- [ ] Collaborative poems (multiple users)
- [ ] Scheduled reminders
- [ ] Export chat history
- [ ] Advanced NLP sentiment analysis
- [ ] Multi-language support

---

**Happy poetrying! 🌙✨**
