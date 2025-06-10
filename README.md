# Video Downloader Bot

Telegram bot for downloading videos from various services using yt-dlp.

## Setup

1. Replace your bot token environment variable:
   ```bash
   export TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
   ```
2. (Optional) If you need YouTube authentication, export cookies:
   ```bash
   python3 dump_cookies.py
   export YT_COOKIES_FILE="cookies.txt"
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python video_downloader_bot.py
   ```
