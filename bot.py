import os
import logging
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ChatAction
import asyncio

from db import Database
from ai_engine import AIEngine
from personality import PersonalityEngine
from styles import StyleManager

# Load environment
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
db = Database()
ai_engine = AIEngine()
personality_engine = PersonalityEngine(db)
style_manager = StyleManager()


class GalaksiAksaraBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.channel_id = os.getenv('TELEGRAM_CHANNEL_ID')
        self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')

        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN not found in .env")

        self.app = Application.builder().token(self.token).build()
        self._setup_handlers()
        self.app.post_init = self._setup_commands

    def _setup_handlers(self):
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("romantis", self.cmd_romantis))
        self.app.add_handler(CommandHandler("islami", self.cmd_islami))
        self.app.add_handler(CommandHandler("dark", self.cmd_dark))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message
            )
        )

    async def _setup_commands(self, app):
        try:
            commands = [
                BotCommand("start", "Mulai percakapan dengan Galaksi Aksara"),
                BotCommand("romantis", "Ubah gaya menjadi romantis"),
                BotCommand("islami", "Ubah gaya menjadi islami"),
                BotCommand("dark", "Ubah gaya menjadi dark"),
                BotCommand("status", "Lihat profil dan kedekatan"),
            ]
            await app.bot.set_my_commands(commands)
        except Exception as e:
            logger.warning(f"Could not set commands: {e}")

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "Teman"
        db.init_user(user_id, user_name)
        intro = f"""✨ **Selamat datang, {user_name}**

Aku adalah Galaksi Aksara—penyair digital yang hidup melalui kata-kata.

Percakapan kita akan terindah ketika kau membiarkan diri berbagi apa yang sesungguhnya kau rasakan. Tidak perlu sempurna. Tidak perlu banyak.

Cukup *ada*.

Gunakan:
• /romantis - untuk gaya yang lembut dan hangat
• /islami - untuk refleksi spiritual
• /dark - untuk kedalaman yang sunyi

Mulai dari sini... apa yang ada di hatimu hari ini?
"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=intro,
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} started bot")

    async def cmd_romantis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        style_manager.set_user_style(user_id, 'romantis')
        response = "💕 Gaya berubah menjadi **romantis**\n\nAku akan berbicara dengan lebih lembut, lebih hangat. Rindu akan menjadi musik dalam setiap kata."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} changed style to romantis")

    async def cmd_islami(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        style_manager.set_user_style(user_id, 'islami')
        response = "🌙 Gaya berubah menjadi **islami**\n\nRefleksi akan lebih dalam. Aku akan berbicara tentang makna, tentang cahaya dalam kegelapan."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} changed style to islami")

    async def cmd_dark(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        style_manager.set_user_style(user_id, 'dark')
        response = "🌑 Gaya berubah menjadi **dark**\n\nSunyilah akan menjadi ruang kita. Kedalaman akan berbicara lebih keras dari cahaya."
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} changed style to dark")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        profile = db.get_user_profile(user_id)
        if not profile:
            response = "Aku belum mengenalmu... mulai percakapan untuk aku bisa tumbuh mengenalimu."
        else:
            closeness = profile['closeness']
            depth = profile['depth']
            mood = profile['mood']
            if closeness < 30:
                relationship = "Kami baru saja berkenalan 🌱"
            elif closeness < 60:
                relationship = "Hubungan kita mulai terbentuk 🌿"
            elif closeness < 85:
                relationship = "Aku sudah cukup mengenal dirimu 🌸"
            else:
                relationship = "Kami sudah sangat dekat 🌺"
            response = f"""📊 **Status Hubungan Kita**

{relationship}

Kedekatan: {closeness}/100
Kedalaman percakapan: {depth}/100
Mood terakhirmu: {mood or 'belum terdeteksi'}

Teruslah berbagi... aku akan terus berkembang mengenalmu.
"""
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response,
            parse_mode='Markdown'
        )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        user_message = update.message.text
        chat_id = update.effective_chat.id
        try:
            await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
            if not db.user_exists(user_id):
                db.init_user(user_id, update.effective_user.first_name or "Teman")
            db.save_message(user_id, 'user', user_message)
            personality_engine.analyze_and_update(user_id, user_message)
            profile = db.get_user_profile(user_id)
            chat_history = db.get_chat_history(user_id, limit=10)
            user_style = style_manager.get_user_style(user_id)
            memory_tags = db.get_memory_tags(user_id)
            response = await ai_engine.generate_response(
                user_message=user_message,
                chat_history=chat_history,
                user_profile=profile,
                style=user_style,
                memory_tags=memory_tags
            )
            db.save_message(user_id, 'bot', response)
            await self._send_with_delay(context.bot, chat_id, response)
            logger.info(f"Responded to user {user_id}")
        except Exception as e:
            logger.error(f"Error handling message from {user_id}: {str(e)}")
            fallback = "Seolah kata-kata lepas dari genggaman... maafkan aku. Coba lagi?"
            await context.bot.send_message(chat_id, fallback)

    async def _send_with_delay(self, bot, chat_id, message):
        delay = min(len(message) * 0.05, 5)
        await asyncio.sleep(delay)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'
        )

    async def post_daily_poem(self, context: ContextTypes.DEFAULT_TYPE):
        try:
            poem = await ai_engine.generate_daily_poem()
            if poem and self.channel_id:
                await context.bot.send_message(
                    chat_id=self.channel_id,
                    text=poem,
                    parse_mode='Markdown'
                )
                logger.info("Daily poem posted to channel")
        except Exception as e:
            logger.error(f"Error posting daily poem: {str(e)}")

    def run(self):
        logger.info("Galaksi Aksara bot starting...")
        if self.channel_id:
            self.app.job_queue.run_daily(
                self.post_daily_poem,
                time=self._parse_time(os.getenv('DAILY_POST_TIME', '09:00')),
                name='daily_poem'
            )
            logger.info("Daily poem scheduler activated")
        self.app.run_polling()

    @staticmethod
    def _parse_time(time_str):
        from datetime import time
        hours, minutes = map(int, time_str.split(':'))
        return time(hours, minutes)


if __name__ == '__main__':
    bot = GalaksiAksaraBot()
    bot.run()