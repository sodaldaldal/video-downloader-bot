import os
import logging
import tempfile
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from yt_dlp import YoutubeDL

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Токен бота из ENV
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in environment")
    exit(1)

# Опциональный файл cookies для YouTube-аутентификации
COOKIES_FILE = os.environ.get("YT_COOKIES_FILE")
if COOKIES_FILE and not os.path.exists(COOKIES_FILE):
    logger.warning(f"Cookies file {COOKIES_FILE} not found — proceeding without cookies")
    COOKIES_FILE = None

# Настройки yt-dlp
ydl_opts = {
    "format": "bestvideo+bestaudio/best",
    "quiet": True,
}
if COOKIES_FILE:
    ydl_opts["cookiefile"] = COOKIES_FILE

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Пришли мне ссылку на видео (YouTube, Instagram и т.д.), и я его скачаю."
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Скачиваю видео, подожди…")

    with tempfile.TemporaryDirectory() as tmpdir:
        opts = ydl_opts.copy()
        opts["outtmpl"] = os.path.join(tmpdir, "%(id)s.%(ext)s")
        try:
            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, "rb") as video_file:
                await update.message.reply_video(video_file)

        except Exception as e:
            logger.error(f"Ошибка при скачивании: {e}")
            msg = str(e)
            if "Sign in to confirm" in msg:
                await update.message.reply_text(
                    "Для скачивания этого видео нужна авторизация YouTube. "
                    "Экспортируй cookies в cookies.txt и задай YT_COOKIES_FILE."
                )
            else:
                await update.message.reply_text(
                    "Не удалось скачать видео. Проверь ссылку и попробуй ещё раз."
                )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем хэндлеры
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Запускаем polling и сразу сбрасываем все старые апдейты
    app.run_polling(drop_pending_updates=True)
