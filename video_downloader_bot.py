import os
import logging
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in environment")
    exit(1)

# yt-dlp options
ydl_opts = {
    'outtmpl': '%(id)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'quiet': True,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Пришли мне ссылку на видео (YouTube, Instagram и т.д.), и я его скачаю."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Скачиваю видео, подожди...")

    with tempfile.TemporaryDirectory() as tmpdir:
        opts = ydl_opts.copy()
        opts['outtmpl'] = os.path.join(tmpdir, '%(id)s.%(ext)s')
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            # Send the video back to user
            with open(filename, 'rb') as video_file:
                await update.message.reply_video(video_file)
        except Exception as e:
            logger.error(f"Ошибка при скачивании: {e}")
            await update.message.reply_text(
                "Не удалось скачать видео. Проверь ссылку и попробуй ещё раз."
            )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    # Start polling; Render will keep this process alive
    app.run_polling()
