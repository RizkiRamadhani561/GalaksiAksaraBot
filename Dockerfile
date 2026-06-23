FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY bot.py db.py personality.py ai_engine.py styles.py fallback_poems.json ./

# Create logs directory
RUN mkdir -p logs

# Run bot
CMD ["python", "bot.py"]
