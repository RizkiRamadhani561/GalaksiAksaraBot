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
   6234234923:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
   ```

### Get Channel ID

Option A: Jika sudah punya channel:
1. Add bot ke channel
2. Send message ke channel
3. Buka browser:
   ```
   https://api.telegram.org/bot{PASTE_TOKEN_HERE}/getUpdates
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
TELEGRAM_BOT_TOKEN = 6234234923:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
TELEGRAM_CHANNEL_ID = -1001234567890  (or @channel_name)
OLLAMA_URL = http://localhost:11434
OLLAMA_MODEL = phi
DAILY_POST_TIME = 09:00
LOG_LEVEL = INFO
```

4. Click "Save"

Render akan otomatis restart service.

---

## ⚙️ Step 5: Handle Ollama untuk Production

Karena bot perlu akses Ollama, ada beberapa opsi:

### Option 1: Gunakan Fallback Mode (RECOMMENDED)

**Kelebihan:**
- Tidak perlu setup Ollama di server
- Bot tetap berfungsi dengan template poems
- Fallback poems masih terasa natural dan puitis
- Free dan simple

**Cara:**
1. Set `OLLAMA_URL` ke invalid address
2. AI Engine akan auto fallback
3. Bot akan respond dengan template poems
4. Tetap terasa seperti puisi asli!

Aturan fallback:
```python
# Jika Ollama offline/timeout → gunakan fallback
# Fallback poems sudah disetting untuk berbagai mood
# Natural dan tidak terasa seperti template
```

### Option 2: Setup Ollama di Server Terpisah

Jika ingin AI generation penuh:

**Setup di DigitalOcean / AWS / Linode:**

1. Create droplet (minimal 2GB RAM, 30GB disk untuk phi)
2. SSH ke server:
   ```bash
   ssh root@your_server_ip
   ```

3. Install Ollama:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull phi
   ```

4. Run Ollama:
   ```bash
   # Background
   nohup ollama serve > /tmp/ollama.log 2>&1 &
   
   # Or use systemd (better)
   sudo systemctl enable ollama
   sudo systemctl start ollama
   ```

5. Expose port (untuk akses dari Render):
   ```bash
   # Edit Ollama config
   OLLAMA_HOST=0.0.0.0:11434
   ```

6. Setup firewall:
   ```bash
   ufw allow 11434
   ```

7. Di Render, set:
   ```
   OLLAMA_URL = http://your_server_ip:11434
   ```

**Cost estimate:**
- DigitalOcean: $5-10/month
- Atau upgrade Render instance: $7-28/month

### Option 3: Hybrid Approach (BEST)

Setup yang smart:

1. AI Engine coba connect ke Ollama
2. Jika timeout/error → fallback ke template
3. Jika available → gunakan AI generation
4. User tidak notice bedanya

Sudah implemented di `ai_engine.py`:
```python
try:
    response = await self._call_ollama(prompt)
    if response:
        return response
except:
    pass

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

### Ollama connection error

**Jika pakai external Ollama:**
- Check server IP accessible dari Render
- Check firewall allow port 11434
- Check OLLAMA_URL format benar

**Better solution:**
- Disable Ollama
- Use fallback mode
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

### Ollama Server (jika pake external)
- DigitalOcean Basic: $5/month
- AWS Lightsail: $3.50-5/month
- Linode: $5/month

### Total Cost Options
- **Free**: Render free + fallback poems = $0
- **Budget**: Render Starter + fallback = $7/month
- **Best**: Render Standard + Ollama = $35-50/month

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
- [Ollama](https://ollama.ai)
- [DigitalOcean](https://digitalocean.com)

---

## ✅ Success!

Bot sekarang live dan accessible 24/7! 🎉

**Enjoy your poetic bot!** 🌙✨
