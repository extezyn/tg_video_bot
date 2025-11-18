import os
import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# Регулярки для распознавания ссылок
REEL_REGEX = r"(https?:\/\/www\.instagram\.com\/reel\/[^\s\/]+)"
INSTAGRAM_REGEX = r"(https?:\/\/www\.instagram\.com\/p\/[^\s\/]+)"
TIKTOK_REGEX = r"(https?:\/\/(?:www\.)?tiktok\.com\/[^\s]+)"
YOUTUBE_REGEX = r"(https?:\/\/(?:www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[^\s]+)"

# --- Функции для получения видео ---
def get_reel_video(url: str):
    api_url = "https://instagram-reels-downloader-api.p.rapidapi.com/download"
    headers = {
        "x-rapidapi-host": "instagram-reels-downloader-api.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }
    params = {"url": url}
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        return None, f"Ошибка API: {response.status_code}"
    
    data = response.json()
    if "video" in data and data["video"]:
        return data["video"], None
    else:
        return None, "Видео не найдено"

def get_instagram_post(url: str):
    # Ваш старый API или метод для постов Instagram
    api_url = "https://instagram-downloader-download-instagram-stories-videos4.p.rapidapi.com/convert"
    headers = {
        "x-rapidapi-host": "instagram-downloader-download-instagram-stories-videos4.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }
    params = {"url": url}
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        return None, f"Ошибка API: {response.status_code}"
    
    data = response.json()
    if "media" in data and len(data["media"]) > 0:
        media_url = data["media"][0].get("url")
        if media_url:
            return media_url, None
    return None, "Видео не найдено"

def get_tiktok_video(url: str):
    api_url = "https://tiktok-downloader-download-tiktok-videos.p.rapidapi.com/vid"
    headers = {
        "x-rapidapi-host": "tiktok-downloader-download-tiktok-videos.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }
    params = {"url": url}
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        return None, f"Ошибка API: {response.status_code}"
    
    data = response.json()
    if "video" in data:
        return data["video"], None
    return None, "Видео не найдено"

def get_youtube_video(url: str):
    api_url = "https://youtube-media-downloader.p.rapidapi.com/v1/youtube/video"
    headers = {
        "x-rapidapi-host": "youtube-media-downloader.p.rapidapi.com",
        "x-rapidapi-key": RAPID_API_KEY
    }
    params = {"url": url}
    
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code != 200:
        return None, f"Ошибка API: {response.status_code}"
    
    data = response.json()
    if "video" in data and len(data["video"]) > 0:
        return data["video"][0].get("url"), None
    return None, "Видео не найдено"

# --- Основной обработчик сообщений ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if re.search(REEL_REGEX, text):
        video_url, error = get_reel_video(text)
        if error:
            await update.message.reply_text(f"Ошибка: {error}")
        else:
            await update.message.reply_text(f"Ссылка на Reels видео: {video_url}")
        return

    if re.search(INSTAGRAM_REGEX, text):
        video_url, error = get_instagram_post(text)
        if error:
            await update.message.reply_text(f"Ошибка: {error}")
        else:
            await update.message.reply_text(f"Ссылка на Instagram пост: {video_url}")
        return

    if re.search(TIKTOK_REGEX, text):
        video_url, error = get_tiktok_video(text)
        if error:
            await update.message.reply_text(f"Ошибка: {error}")
        else:
            await update.message.reply_text(f"Ссылка на TikTok видео: {video_url}")
        return

    if re.search(YOUTUBE_REGEX, text):
        video_url, error = get_youtube_video(text)
        if error:
            await update.message.reply_text(f"Ошибка: {error}")
        else:
            await update.message.reply_text(f"Ссылка на YouTube видео: {video_url}")
        return

    await update.message.reply_text("Похоже, это ссылка на неподдерживаемый сервис или текст.")

# --- Запуск бота ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), message_handler))
    print("Бот запущен и ожидает ссылки на видео...")
    app.run_polling()
