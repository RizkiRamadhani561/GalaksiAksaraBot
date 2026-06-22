# 🌙 GalaksiAksaraBot - Dokumentasi Lengkap

Bot Telegram bernama "Galaksi Aksara" dengan AI yang hidup, reflektif, dan emosional.
Catatan: beberapa bagian lama di bawah masih menyebut Ollama sebagai arsip migrasi, tetapi setup aktif untuk versi ini memakai Gemini.

---

## 📋 Table of Contents
1. [Setup Lokal](#setup-lokal)
2. [Konfigurasi Gemini AI](#konfigurasi-gemini-ai)
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
- Google Gemini API key
- Internet connection
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
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=@galaksi_aksara_channel
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
DAILY_POST_TIME=09:00
```

---

## Konfigurasi Gemini AI

Bot ini menggunakan Google Gemini API untuk respons utama, lalu fallback ke puisi bawaan jika API key belum tersedia atau Gemini sedang bermasalah.

### Step 1: Buat API key Gemini

1. Buka https://aistudio.google.com/app/apikey
2. Buat API key baru
3. Salin key yang diberikan

### Step 2: Simpan di `.env`

Tambahkan variabel ini:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

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

### GEMINI_API_KEY
API key dari Google Gemini. Wajib diisi jika ingin bot menjawab dengan Gemini.

### GEMINI_MODEL
Model Gemini yang digunakan. Default: `gemini-2.0-flash`.

### DAILY_POST_TIME
Waktu posting puisi harian ke channel. Default: `09:00`.

### LOG_LEVEL
Level logging aplikasi. Default: `INFO`.

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
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL_ID=your_channel
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
DAILY_POST_TIME=09:00
LOG_LEVEL=INFO
```

### Step 5: Deploy

Click "Create Web Service"

Render akan otomatis deploy dan restart service setiap ada push ke GitHub.

---

### Deployment Notes

Tidak perlu menjalankan server model lokal. Selama `GEMINI_API_KEY` tersedia, bot akan memakai Gemini. Jika key tidak ada atau request gagal, bot tetap jalan dengan fallback puisi bawaan.

---

## 🏗️ Architecture & Features

### File Structure

```
galaxi_aksara_bot/
├── bot.py           # Main application
├── db.py            # Database management
├── personality.py   # Personality engine
├── ai_engine.py     # AI/Gemini integration
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
- Uses Gemini with cloud API
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

**Check 1: Gemini key ada?**
```bash
echo $GEMINI_API_KEY
```

**Check 2: Token valid?**
- Verify token di `.env`
- Make sure no extra spaces

**Check 3: Check logs**
```bash
tail -f bot.log
```

---

### Gemini connection error

**Error: Gemini request gagal**

Solution:
1. Make sure `GEMINI_API_KEY` sudah ada di `.env`
2. Pastikan `GEMINI_MODEL=gemini-2.0-flash` atau model valid lain
3. Cek logs untuk pesan error dari `google-genai`

Bot akan pakai fallback poems jika Gemini tidak available.

---

### Model not found

**Error: model Gemini tidak valid**

Solution:
1. Pakai model yang didukung Gemini, misalnya `gemini-2.0-flash`
2. Update `.env` lalu restart bot
3. Cek dokumentasi Gemini jika model berubah

---

### Database errors

**Delete dan recreate database:**
```bash
rm galaxi_aksara.db
python bot.py
```

---

### Performance issues on Render Free Tier

- Use lightweight Gemini model: `gemini-2.0-flash`
- Enable fallback is automatic
- Consider upgrading to paid instance
- No local model server needed

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

# Test Gemini SDK directly
python - <<'PY'
from google import genai
print("Gemini SDK OK")
PY
```

---

## 🔄 Updates & Maintenance

### Regular Tasks
- Monitor `bot.log` for errors
- Clean old messages: `db.cleanup_old_messages()`
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Verify `GEMINI_API_KEY` is still valid periodically

### Monitoring Script
```bash
#!/bin/bash
if [ -z "$GEMINI_API_KEY" ]; then
  echo "GEMINI_API_KEY not set at $(date)" >> gemini_status.log
fi
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
