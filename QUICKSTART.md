# 🌙 GalaksiAksaraBot - Quick Start

Mulai dalam 5 menit!

---

## ⚡ Fastest Setup

### 1. Requirements
```bash
# Make sure installed:
python3 --version      # Python 3.9+
git --version          # For cloning
curl --version         # For checking Ollama
```

### 2. Clone & Setup
```bash
# Clone/download project
cd galaxi_aksara_bot

# Setup (all in one)
bash setup.sh full
```

### 3. Configure
```bash
# Edit .env file
nano .env

# Minimal required:
TELEGRAM_BOT_TOKEN=your_token_from_botfather
TELEGRAM_CHANNEL_ID=@your_channel  (optional)
```

### 4. Start Ollama (terminal baru)
```bash
ollama serve
```

Models tersedia:
```bash
ollama pull phi         # Fast, lightweight (recommended)
ollama pull mistral     # Better quality
ollama pull neural-chat # Chat optimized
```

### 5. Run Bot (terminal ketiga)
```bash
cd galaxi_aksara_bot
source venv/bin/activate
python bot.py
```

Output seharusnya:
```
2024-01-15 10:30:47,345 - root - INFO - 🌙 Galaksi Aksara bot starting...
```

### 6. Test
Cari bot di Telegram, kirim `/start`

---

## 🐳 Atau Gunakan Docker (Paling Mudah)

```bash
# Make sure Docker installed
docker --version

# Setup
docker-compose up -d

# Check logs
docker-compose logs -f bot

# Stop
docker-compose down
```

---

## 📱 Bot Commands

```
/start    - Mulai percakapan
/romantis - Gaya romantis (lembut & hangat)
/islami   - Gaya islami (spiritual & reflektif)
/dark     - Gaya dark (sunyi & dalam)
/status   - Lihat profil & kedekatan
```

---

## 🛠️ Troubleshooting Quick

| Problem | Solution |
|---------|----------|
| Bot tidak respond | 1. Check terminal ada error 2. Check token di .env 3. Cek logs |
| Cannot connect Ollama | Jalankan `ollama serve` di terminal baru |
| ModuleNotFoundError | Run `pip install -r requirements.txt` |
| Database error | Run `rm galaxi_aksara.db` then `python bot.py` |
| Permission denied setup.sh | Run `chmod +x setup.sh` |

---

## 📚 Full Documentation

- **Setup lengkap**: [README.md](README.md)
- **Deploy ke Render**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Architecture**: [README.md#architecture--features](README.md)

---

## 🎓 Next Steps

1. **Customize responses**: Edit prompts di `ai_engine.py`
2. **Adjust personality**: Tweak `personality.py`
3. **Add fallback poems**: Edit `ai_engine.py` fallback_poems
4. **Deploy to cloud**: Follow [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 💡 Tips

- Bot learns about user over time
- More interaction = deeper responses
- Fallback poems active jika Ollama offline
- Database auto-cleanup old chats (30 days)

---

**Happy poetrying!** 🌙✨

Need help? Check README.md untuk full documentation.
