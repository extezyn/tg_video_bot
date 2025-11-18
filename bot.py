import logging
import tempfile
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
RAPID_API_KEY = "YOUR_RAPID_API_KEY"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_instagram_video(url):
    api_url = "https://instagram-downloader.p.rapidapi.com/index"

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "instagram-downloader.p.rapidapi.com"
    }

    params = {"url": url}

    response = requests.get(api_url, headers=headers, params=params).json()

    if "media" not in response:
        raise Exception("API не вернул ссылку на видео")

    return response["media"]  # mp4 ссылка


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь ссылку — я скачаю тебе видео.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not url.startswith("http"):
        await update.message.reply_text("Отправь корректную ссылку.")
        return

    try:
        # Instagram
        if "instagram.com" in url:
            direct_url = download_instagram_video(url)
        else:
            raise Exception("Пока что поддерживается только Instagram.")

        # Скачиваем файл
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")

        video_data = requests.get(direct_url).content
        with open(temp_file.name, "wb") as f:
            f.write(video_data)

        # отправляем
        await update.message.reply_video(open(temp_file.name, "rb"))

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
