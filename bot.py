import os
import yt_dlp
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ChatAction

TOKEN = os.getenv(TOKEN)


def download_video(url):
    # Скачиваем видео в mp4
    ydl_opts = {
        "format": "mp4/best",
        "outtmpl": "video.mp4",     # итоговый файл
        "quiet": True,
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "video.mp4"


def handle_message(update, context):
    url = update.message.text.strip()

    update.message.reply_text("🔽 Скачиваю видео, подожди...")
    update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)

    try:
        path = download_video(url)

        with open(path, "rb") as file:
            update.message.reply_video(video=file)

        os.remove(path)

    except Exception as e:
        update.message.reply_text(f"❌ Ошибка при скачивании: {e}")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
