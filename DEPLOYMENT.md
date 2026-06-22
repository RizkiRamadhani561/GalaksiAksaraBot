# 🚀 Deployment Guide - GalaksiAksaraBot to Render

Panduan lengkap untuk deploy bot ke Render dengan smooth.

---

## 📋 Prerequisites

- GitHub account
- Render account (https://render.com)
- Telegram Bot Token (dari @BotFather)
- Channel ID untuk posting (opsional)

---

## 🔑 Step 1: Dapatkan Telegram Credentials

### Get Bot Token

1. Open Telegram, search **@BotFather**
2. Send `/newbot`
3. Follow prompts:
   - Bot name: `Galaksi Aksara`
   - Bot username: `galaksi_aksara_bot` (unik untuk user mu)
4. Copy token yang diberikan, contoh:
   ```
   your_telegram_bot_token
   ```

### Get Channel ID

Option A: Jika sudah punya channel:
1. Add bot ke channel
2. Send message ke channel
3. Buka browser:
   ```
   https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates
   ```
4. Cari `chat.id` di response
   ```json
   "chat": {
     "id": -1001234567890,
     "title": "Galaksi Aksara Channel"
   }
   ```
5. Copy ID (format: `-1001234567890`)

Option B: Menggunakan channel username:
- Format: `@galaksi_aksara`
- Lebih mudah, tidak perlu ID number

---

## 💾 Step 2: Push Code ke GitHub

### Create Repository

1. Go to https://github.com/new
2. Create repository:
   - Name: `galaxi-aksara-bot`
   - Description: "Poetic Telegram Bot with AI"
   - Public (recommended) or Private
   - DO NOT initialize with README (kita punya)

### Push Code

```bash
# Dari folder project
git init
git add .
git commit -m "Initial commit: GalaksiAksaraBot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/galaxi-aksara-bot.git
git push -u origin main
```

Verify di GitHub bahwa semua file ter-push.

---

## 🎯 Step 3: Create Render Service

### Option A: Direct Deployment (Recommended)

1. Go to https://render.com/dashboard
2. Click "New +"
3. Select **"Web Service"**
4. Connect GitHub:
   - Click "Connect GitHub"
   - Authorize Render
   - Select repository: `galaxi-aksara-bot`
   - Select branch: `main`

### Configure Service

Fill form:

| Field | Value |
|-------|-------|
| Name | `galaxi-aksara-bot` |
| Environment | Python 3 |
| Region | Singapore (untuk latency terbaik ke Indo) |
| Branch | main |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python bot.py` |
| Instance Type | Free (or Starter/Standard for production) |

### Create Service

Click "Create Web Service"

Render akan langsung build dan deploy.

---

## 🔐 Step 4: Set Environment Variables

### Di Render Dashboard

1. Go ke service yang baru dibuat
2. Click pada tab **"Environment"**
3. Add variables:

```
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_CHANNEL_ID = -1001234567890  (or @channel_name)
GEMINI_API_KEY = your_gemini_api_key_here
GEMINI_MODEL = gemini-2.0-flash
DAILY_POST_TIME = 09:00
LOG_LEVEL = INFO
```

4. Click "Save"

Render akan otomatis restart service.

---

## ⚙️ Step 5: Gemini di Production

Bot ini memakai Google Gemini API, jadi tidak perlu menjalankan server model lokal di Render. Cukup pastikan `GEMINI_API_KEY` dan `GEMINI_MODEL` sudah diisi di environment variables.

Jika key tidak tersedia atau Gemini gagal merespons, bot otomatis memakai fallback puisi bawaan.

Sudah implemented di `ai_engine.py`:
```python
# Coba Gemini dulu
response = await self._call_gemini(prompt)
if response:
    return response

# Fallback otomatis
return self._get_fallback_response(...)
```

---

## 🧪 Step 6: Test Deployment

### Check Service Status

1. Di Render dashboard, lihat logs
2. Seharusnya muncul:
   ```
   INFO - Database initialized
   INFO - 🌙 Galaksi Aksara bot starting...
   INFO - Daily poem scheduler activated
   ```

### Test di Telegram

1. Find bot di Telegram search
2. Send `/start`
3. Bot seharusnya respond dengan intro puitis
4. Chat dengan bebas → bot respond dengan puisi

### Monitor Logs

```bash
# Di Render dashboard
1. Click service name
2. Go to "Logs" tab
3. Live logs akan terlihat
```

---

## 🔄 Step 7: Auto-Deployment

### GitHub Integration

Setiap kali push ke main:

```bash
git add .
git commit -m "Update: improve responses"
git push origin main
```

Render **otomatis**:
1. Detect push
2. Pull code
3. Build
4. Deploy
5. Restart bot

Tidak perlu manual restart!

---

## 📊 Monitoring & Maintenance

### Check Service Health

```bash
# Render dashboard → Metrics tab
- CPU usage
- Memory usage
- Network
```

### View Recent Errors

Render dashboard → Logs tab:
- Red = errors
- Yellow = warnings
- Blue = info

### Restart Service

1. Render dashboard → Settings
2. "Restart instance"
3. Service restart (usually <1 minute downtime)

---

## 🆘 Troubleshooting

### Bot tidak respond

**Check 1: Service running?**
- Render dashboard → Status
- Seharusnya "Live"

**Check 2: Logs ada error?**
- Render dashboard → Logs
- Cari error messages

**Check 3: Environment variables?**
- Render dashboard → Environment
- Verify TELEGRAM_BOT_TOKEN ada

### Daily poems tidak post

**Check 1: TELEGRAM_CHANNEL_ID valid?**
- Verify format: `-1001234567890` atau `@channel_name`
- Bot sudah di-add ke channel?

**Check 2: Scheduled time?**
- Check DAILY_POST_TIME
- Render timezone: UTC
- Convert ke UTC jika perlu

### Gemini connection error

- Check `GEMINI_API_KEY` ada di environment variables
- Check `GEMINI_MODEL` valid
- Check logs untuk error dari `google-genai`

**Better solution:**
- Use fallback mode otomatis
- Bot tetap berfungsi dengan fallback poems

---

## 💰 Pricing

### Render Free Tier
- 1 free instance (~0.5 GB RAM)
- Auto-sleep after 15 min no traffic
- Good untuk testing

### Render Paid
- Starter: $7/month (0.5 GB RAM, always on)
- Standard: $28+/month (2 GB+ RAM, better performance)

### Legacy Ollama Notes
- DigitalOcean Basic: $5/month
- AWS Lightsail: $3.50-5/month
- Linode: $5/month

### Total Cost Options
- **Free**: Render free + fallback poems = $0
- **Budget**: Render Starter + fallback = $7/month
- **Best**: Render Standard + Gemini = $7-28/month

---

## 🎯 Deployment Checklist

- [ ] GitHub account setup
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] GitHub connected to Render
- [ ] Web service created
- [ ] Environment variables set
- [ ] Bot token from @BotFather
- [ ] Channel ID/username configured
- [ ] Service deployed successfully
- [ ] Tested in Telegram (/start command)
- [ ] Logs checked for errors
- [ ] Daily posting configured

---

## 📱 Useful Commands

### Check Bot Status
```bash
# At Telegram
/status  # Shows relationship info
```

### Manual Testing
```bash
# Push test message
git commit --allow-empty -m "Test deployment"
git push

# Watch logs
# Render dashboard → Logs
```

### Database Backup
```bash
# Download from Render
# Via SFTP or GitHub
# galaxi_aksara.db file
```

---

## 🔗 Useful Links

- [Render Dashboard](https://render.com/dashboard)
- [Telegram BotFather](https://t.me/botfather)
- [Google AI Studio](https://aistudio.google.com/app/apikey)
- [DigitalOcean](https://digitalocean.com)

---

## ✅ Success!

Bot sekarang live dan accessible 24/7! 🎉

**Enjoy your poetic bot!** 🌙✨
