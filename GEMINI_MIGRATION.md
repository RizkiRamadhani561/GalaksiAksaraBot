# Gemini Migration Guide — Galaksi Aksara Bot

> **Status:** ✅ Complete  
> **Date:** 2026-06-22  
> **Target:** Convert from Ollama (local LLM) to Google Gemini API (cloud AI)

---

## 📋 Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] `pip` package manager available
- [ ] Telegram Bot Token (already in `.env`)
- [ ] Google Gemini API Key (get from https://aistudio.google.com/app/apikey)
- [ ] Internet connection (Gemini is cloud-based)
- [ ] Original project files backed up (script does this automatically)

---

## 🔄 What Changed

| Aspect | Before (Ollama) | After (Gemini) |
|--------|-----------------|----------------|
| **AI Engine** | `ai_engine.py` with `requests.post` to `localhost:11434` | `ai_engine.py` with `google.genai.Client()` SDK v2.9.0 |
| **Dependency** | Required Ollama Docker container running locally | Zero local dependencies — pure cloud API |
| **Environment** | `OLLAMA_URL=http://localhost:11434` | `GEMINI_API_KEY=your_key_here` |
| **SDK** | `requests` library for HTTP calls | `google-genai` official Google SDK |
| **Fallback** | Ollama → Template poems | Gemini API → Template poems |
| **Deploy** | Multi-container Docker (Ollama + Bot) | Single-container or direct Python |
| **Cost** | Free (local) | Free tier: 60 req/min |
| **Reliability** | Dependent on local hardware | Google Cloud infrastructure |

## 📁 Files Modified

| File | Change Description |
|------|-------------------|
| `ai_engine.py` | Complete rewrite — replaced Ollama HTTP calls with `google.genai.Client()` |
| `.env` | Added `GEMINI_API_KEY=`, removed `OLLAMA_URL=` and `OLLAMA_MODEL=` |
| `.env.example` | Updated template with Gemini configuration placeholders |
| `requirements.txt` | `google-genai>=0.8.0` replaces `requests>=2.31.0` |
| `docker-compose.yml` | Removed Ollama service, volume mounts, healthcheck, network — simplified to single service |
| `Dockerfile` | Removed `curl` system dependency and `HEALTHCHECK` directive |
| `GEMINI_MIGRATION.md` | **New** — this document |

## 🔧 Step-by-Step Migration

### Step 1: Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Click **"Get API Key"** button
3. Sign in with your Google account
4. Click **"Create API Key"** 
5. Copy the key (format: `AIzaSy...` or `AQ.Ab8...`)
6. **Important:** Store this key securely — don't commit to git

### Step 2: Install Dependencies

```bash
pip install google-genai
```

This installs the official Google Gemini v2 SDK (`google.genai` package, version 2.9.0+).

### Step 3: Update Environment Variables

Edit `.env` file:

```env
# Before (Ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=phi

# After (Gemini)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
```

### Step 4: Replace ai_engine.py

The core change is in `ai_engine.py`:

**Before** (Ollama HTTP call):
```python
async def _call_ollama(self, prompt):
    url = f"{self.ollama_url}/api/generate"
    response = requests.post(url, json={
        "model": self.model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.9,
        "top_p": 0.95,
        "top_k": 40
    }, timeout=30)
    return response.json().get('response')
```

**After** (Gemini API call):
```python
async def _call_gemini(self, prompt):
    def _sync_call():
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={
                "temperature": 0.9,
                "top_p": 0.95,
                "max_output_tokens": 300,
            }
        )
        return response.text.strip() if response and response.text else None
    
    return await asyncio.get_event_loop().run_in_executor(None, _sync_call)
```

### Step 5: Test Locally

```bash
# Quick syntax check
python -c "from google import genai; c = genai.Client(api_key='test'); print('SDK OK')"

# Full bot test
python bot.py
```

Expected output:
```
Database initialized
Galaksi Aksara bot starting...
Daily poem scheduler activated
getMe → 200 OK
setMyCommands → 200 OK
Application started
getUpdates → 200 OK
```

### Step 6: Deploy

**Direct Python:**
```bash
cd /path/to/BotTelegram
python bot.py
```

**With Docker:**
```bash
docker build -t galaksi-bot .
docker run -d --env-file .env galaksi-bot
```

## 🏗️ Architecture

```
                    ┌──────────────────┐
                    │  User Message     │
                    │  via Telegram     │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  bot.py          │
                    │  Message Handler │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  ai_engine.py    │
                    │                  │
                    │  ┌────────────┐  │
                    │  │ Gemini API  │  │  ← TIER 1 (Primary)
                    │  │ (cloud)     │  │
                    │  └─────┬──────┘  │
                    │        │ fails   │
                    │  ┌─────▼──────┐  │
                    │  │ Templates   │  │  ← TIER 2 (Fallback)
                    │  │ (built-in)  │  │
                    │  └────────────┘  │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Response to     │
                    │  User ✨         │
                    └──────────────────┘
```

## 🛠️ Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| `ModuleNotFoundError: No module named 'google'` | `google-genai` not installed | Run `pip install google-genai` |
| `google.auth.exceptions.RefreshError` | Invalid or expired API key | Generate new key at https://aistudio.google.com/app/apikey |
| `429 Resource has been exhausted` | Rate limit exceeded | Wait 60 seconds. Free tier: 60 requests/minute |
| Empty response from Gemini | Content filtered by safety settings | Adjust prompt to avoid sensitive topics |
| `telegram.error.Conflict: 409` | Another bot instance running | Kill all Python processes: `taskkill /f /im python.exe` |
| Bot responds with template poems only | Gemini API key missing or invalid | Check `GEMINI_API_KEY` in `.env` file |
| `google.genai` not found | Wrong package installed | Install correct one: `pip install google-genai` (not `google-generativeai`) |

### Common Mistakes to Avoid

1. **Don't use the old SDK**: The deprecated `google.generativeai` shows FutureWarning. We use `google.genai` (v2).
2. **Don't commit API keys**: `.env` is in `.gitignore`. Always verify before committing.
3. **Don't forget the fallback**: If Gemini fails, the bot still responds with built-in poems.
4. **Don't run multiple instances**: Telegram only allows one polling connection per bot token.

## ↩️ Rollback Instructions

To revert to Ollama:

```bash
# 1. Restore backed-up files
cp ai_engine.py.backup_YYYYMMDD_HHMMSS ai_engine.py

# 2. Restore .env
# Edit .env and replace Gemini config with Ollama config:
# OLLAMA_URL=http://localhost:11434
# OLLAMA_MODEL=phi

# 3. Start Ollama
docker run -d -p 11434:11434 ollama/ollama

# 4. Run bot
python bot.py
```

## ✅ Verification Checklist

After migration, verify:

- [ ] `python bot.py` starts without errors
- [ ] `getMe` returns 200 OK (Telegram connected)
- [ ] `setMyCommands` returns 200 OK (commands registered)
- [ ] Bot responds to `/start` command
- [ ] Bot responds to text messages
- [ ] Style switching works (`/romantis`, `/islami`, `/dark`)
- [ ] No `FutureWarning` about deprecated SDK
- [ ] Template poems work when API key is removed (fallback test)

## 📊 Before/After Comparison

| Metric | Ollama | Gemini |
|--------|--------|--------|
| Startup time | ~30s (model load) | <1s (no model to load) |
| Response time | 2-10s (local GPU/CPU) | 1-3s (Google servers) |
| Memory usage | 2-4GB (Ollama + model) | <50MB (SDK only) |
| Disk space | 2-4GB (model file) | <10MB (SDK) |
| Cost | Free (electricity) | Free tier (60 req/min) |
| Availability | Requires local hardware | Google Cloud SLA |
| Quality | Depends on model (phi3) | gemini-2.0-flash (SOTA) |