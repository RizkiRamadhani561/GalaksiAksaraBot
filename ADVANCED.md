# ⚙️ Advanced Configuration & Tuning

Customize GalaksiAksaraBot untuk kebutuhan spesifik.

---

## 🎨 Customize Personality

### 1. Adjust Closeness Calculation

File: `personality.py`

```python
def _calculate_closeness_increase(self, message: str) -> int:
    """
    Default:
    - Base: +2 per message
    - Long message (>50 chars): +1
    - Very long (>100 chars): +1
    - Has emotions: +2
    - Has question: +1
    
    EXAMPLE: Message dengan 60 chars + emotion = +5 closeness
    """
    
    # Untuk lebih aggressive closeness growth:
    increase = 3  # Change from 2 to 3
    
    if len(message) > 50:
        increase += 2  # Change from 1 to 2
    
    # ... rest of code
```

**Preset Values:**

```python
# SLOW (default)
- Base: 2
- Long: 1 each
- Emotions: 2

# MODERATE
- Base: 3
- Long: 2 each
- Emotions: 3

# FAST
- Base: 4
- Long: 3 each
- Emotions: 4
```

### 2. Adjust Depth Calculation

```python
def _calculate_depth_increase(self, message: str) -> int:
    """
    Depth measures how philosophical the conversation is.
    Keywords: mengapa, filosofi, makna, jiwa, hati
    """
    
    # Add/remove keywords based on your preference
    self.depth_keywords = [
        'mengapa', 'bagaimana', 'apa arti',  # Questions
        'filosofi', 'makna',                  # Deep concepts
        'diri', 'jiwa', 'hati', 'perasaan',  # Emotions
        # Add more:
        'kehidupan', 'tujuan', 'masa depan'  # Your additions
    ]
```

### 3. Add Custom Emotion Tags

```python
# File: personality.py
self.emotion_keywords = {
    # ... existing emotions
    'galau': ['galau', 'bingung hati', 'tidak jelas'],
    'nostalgia': ['dulu', 'masa lalu', 'haruskah'],
    'malas': ['males', 'enggan', 'tidak semangat'],
}
```

---

## 💬 Customize Response Styles

### Modify Existing Styles

File: `ai_engine.py`

```python
def _get_style_instructions(self, style: str) -> str:
    styles = {
        'romantis': """- Gaya: LEMBUT, HANGAT, PENUH RINDU
- Gunakan kata: "rindu", "dekat", "cahaya"
# EDIT SINI untuk customize
- Contoh baru: "Seperti bulan yang merindukan malam..."
""",
        
        # Add your own style:
        'melankoli': """- Gaya: SEDIH TAPI INDAH, REFLEKTIF
- Gunakan kata: "sedih yang manis", "duka yang puitis"
- Tone: seperti ballad yang menyentuh hati
- Jangan desperate, tapi penuh makna""",
    }
```

### Add New Style

1. **Add to `styles.py`**:
   ```python
   self.valid_styles = ['romantis', 'islami', 'dark', 'melankoli']
   
   descriptions = {
       ...
       'melankoli': '💜 Sedih indah, reflektif dan bermakna'
   }
   ```

2. **Add to `bot.py`**:
   ```python
   async def cmd_melankoli(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
       user_id = update.effective_user.id
       style_manager.set_user_style(user_id, 'melankoli')
       
       response = "💜 Gaya berubah menjadi **melankoli**\n\nKedukaan akan berbicara dengan lebih indah dan penuh makna."
       
       await context.bot.send_message(
           chat_id=update.effective_chat.id,
           text=response,
           parse_mode='Markdown'
       )
   ```

3. **Add instructions to `ai_engine.py`**:
   ```python
   'melankoli': """- Gaya: SEDIH TAPI INDAH
   - Gunakan metafora: tangis yang indah, duka yang bermakna
   - Tone: seperti lagu kesedihan yang menyentuh"""
   ```

---

## 🤖 Tune AI Engine

### Adjust Temperature & Parameters

File: `ai_engine.py`

```python
async def _call_ollama(self, prompt: str) -> Optional[str]:
    payload = {
        "model": self.model,
        "prompt": prompt,
        "stream": False,
        "temperature": 0.9,  # Higher = more creative (0.0-1.0)
        "top_p": 0.95,       # Nucleus sampling
        "top_k": 40,         # Top-k sampling
    }
```

**Parameter Guide:**

```
temperature:
  0.0 = Deterministic, repetitive
  0.5 = Balanced
  0.9 = Creative, diverse (RECOMMENDED)
  1.0 = Most creative but can be nonsense

top_p (nucleus sampling):
  0.9 = More focused
  0.95 = Balanced (RECOMMENDED)
  1.0 = Consider all tokens

top_k:
  20 = Conservative
  40 = Balanced (RECOMMENDED)
  100 = Very diverse
```

### Change AI Model

```python
# In .env
OLLAMA_MODEL=phi          # Fast, 2.7B (default)
OLLAMA_MODEL=mistral      # Better quality, 7B
OLLAMA_MODEL=neural-chat  # Chat optimized, 7B
OLLAMA_MODEL=dolphin-mix  # Very good, 7B
```

Model comparison:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| phi | 2.7B | ⚡ Fast | ⭐⭐⭐ Good | Free tier |
| mistral | 7B | 🔸 Medium | ⭐⭐⭐⭐ Great | Standard |
| neural-chat | 7B | 🔸 Medium | ⭐⭐⭐⭐ Great | Chat |
| dolphin-mix | 7B | 🟢 Slow | ⭐⭐⭐⭐⭐ Excellent | Quality |

### Customize Prompt

The main prompt in `_build_prompt()` is where magic happens:

```python
def _build_prompt(self, ...):
    # EDIT SINI untuk customize personality
    prompt = f"""Kamu adalah Galaksi Aksara—penyair digital yang hidup...
    
    # Add custom traits:
    # - Aku gemar menggunakan metafora air
    # - Aku selalu mengakhiri dengan pertanyaan
    # - Aku berbicara dengan humor yang subtle
    """
```

---

## 💾 Database Tuning

### Query Chat History

File: `db.py`

```python
def get_chat_history(self, user_id: int, limit: int = 10):
    # Change limit to use more/less context
    # More = better context but slower
    # Less = faster but may miss important info
    
    # Recommended: 8-12 for balance
    # Min: 4 (very minimal context)
    # Max: 20 (very detailed context)
```

### Memory Tag Weights

```python
def add_memory_tag(self, user_id: int, tag: str, weight: int = 1):
    # Default weight increase: 1
    # Increase weight to make emotions stick longer
    
    # Current: +1 per mention
    # Heavy tracking: +3 per mention
    weight_increase = 3  # Change from 1
```

### Cleanup Old Messages

```python
# Default: Delete messages older than 30 days
db.cleanup_old_messages(days=30)

# Keep longer history:
db.cleanup_old_messages(days=90)

# Very short history:
db.cleanup_old_messages(days=7)
```

---

## ⏰ Adjust Daily Post Schedule

File: `.env`

```env
DAILY_POST_TIME=09:00

# Change to your preferred time
# Format: HH:MM (24-hour)
# Note: Render uses UTC timezone

# Examples:
DAILY_POST_TIME=07:00  # 7 AM UTC
DAILY_POST_TIME=14:30  # 2:30 PM UTC
DAILY_POST_TIME=20:00  # 8 PM UTC

# If in Asia (UTC+7), add 7 hours:
# 9 AM local = 02:00 UTC
# 2 PM local = 07:00 UTC
# 8 PM local = 13:00 UTC
```

---

## 🎯 Fallback Poems Customization

Make fallback poems more personal:

File: `ai_engine.py`

```python
self.fallback_poems = {
    'romantis': [
        """Barangkali rindu adalah bahasa terdalam,
yang hanya terucap dalam keheningan malam.
# EDIT SINI dengan puisi mu sendiri
Seolah dirimu selah ada di sini...""",
        
        # Add more poems:
        """Senja adalah waktu terbaik untuk merasa,
ketika langit berubah menjadi lukisan kasih sayang."""
    ],
    
    # Add custom mood:
    'hope': [
        """Ada cahaya di ujung terowongan,
bintang-bintang menunggu untuk bersinar lagi."""
    ]
}
```

---

## 📊 Performance Optimization

### Reduce API Calls

```python
# Cache responses for identical prompts
# Add to ai_engine.py:
from functools import lru_cache

@lru_cache(maxsize=100)
async def get_cached_response(self, prompt):
    # Returns cached response if same prompt used
```

### Reduce Database Queries

```python
# Pre-load data instead of querying repeatedly
profile = db.get_user_profile(user_id)
tags = db.get_memory_tags(user_id)
# Use these without re-querying
```

### Optimize Model Loading

```python
# Load model once, reuse
# Currently Ollama handles this
# But can add in-memory cache:

cache = {}
if prompt_hash in cache:
    return cache[prompt_hash]

response = await ollama(prompt)
cache[prompt_hash] = response
```

---

## 🔍 Monitoring & Debugging

### Enable Verbose Logging

File: `bot.py`

```python
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Add Custom Metrics

```python
# Count responses by style
self.style_stats = {
    'romantis': 0,
    'islami': 0,
    'dark': 0
}

# Track response times
import time
start = time.time()
response = await ai_engine.generate_response(...)
duration = time.time() - start
logger.info(f"Response generated in {duration:.2f}s")
```

### Monitor API Calls

```python
# Count Ollama calls
ollama_calls = 0
ollama_failures = 0

def _call_ollama(...):
    global ollama_calls, ollama_failures
    ollama_calls += 1
    try:
        # call
    except:
        ollama_failures += 1
```

---

## 🔐 Security Hardening

### Rate Limiting

```python
# Add rate limit per user
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, max_messages=5, window=60):
        self.max = max_messages
        self.window = window
        self.calls = defaultdict(list)
    
    def is_allowed(self, user_id):
        now = time.time()
        # Clean old calls
        self.calls[user_id] = [
            t for t in self.calls[user_id]
            if now - t < self.window
        ]
        
        if len(self.calls[user_id]) < self.max:
            self.calls[user_id].append(now)
            return True
        return False
```

### Input Validation

```python
def handle_message(...):
    # Validate message
    if len(message) > 5000:  # Limit message length
        response = "Terlalu panjang, coba singkat aja :)"
        return
    
    if message.count('\n') > 50:  # Limit linebreaks
        response = "Terlalu banyak baris..."
        return
```

---

## 📈 Scale to Production

### Database Optimization

```sql
-- Add indexes for faster queries
CREATE INDEX idx_user_chat ON chat_history(user_id, timestamp);
CREATE INDEX idx_memory_tag ON memory_tags(user_id, weight);
```

### Use Better Database

Switch from SQLite to PostgreSQL:

```python
# Instead of SQLite
import asyncpg
conn = await asyncpg.connect('postgresql://user:pass@localhost/galaxi')
```

### Load Balancing

For multiple instances:

```python
# Use message queue (Redis)
# Route messages to different bot instances
# Share database across instances
```

---

## 🚀 Advanced Features to Add

1. **Image Generation**
   ```python
   from PIL import Image
   # Generate visual poetry
   ```

2. **Voice Messages**
   ```python
   from google.cloud import texttospeech
   # Convert poems to audio
   ```

3. **User Statistics Dashboard**
   ```python
   # Visualize closeness, mood trends
   # Export conversation history
   ```

4. **Multi-language Support**
   ```python
   # Detect language, respond in same language
   # Or ask preferred language
   ```

5. **Collaborative Poems**
   ```python
   # Multiple users contribute lines
   # Bot pieces together into coherent poem
   ```

---

## 📞 For More Help

- Check `README.md` for full documentation
- See `DEPLOYMENT.md` for deployment issues
- Read `QUICKSTART.md` for quick reference
- Check logs: `tail -f bot.log`

---

**Happy customizing!** 🌙✨
