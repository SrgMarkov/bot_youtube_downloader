from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pytube import YouTube
import os
import logging

# Создаем объект логгера
logger = logging.getLogger(__name__)


# Функция обработчик команды /start
def start(update, context):
    update.message.reply_text("Привет! Отправь мне ссылку на видео с YouTube, и я его скачаю.")


# Функция для скачивания видео
def download_video(update, context):
    # Получаем ссылку на видео из сообщения пользователя
    video_url = update.message.text

    try:
        # Создаем объект YouTube и загружаем видео
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()

        # Скачиваем видео в текущую директорию
        video.download()

        # Отправляем пользователю сообщение с подтверждением успешного скачивания
        update.message.reply_text("Видео успешно скачано! 🎉")

        # Отправляем файл видео пользователю
        context.bot.send_video(chat_id=update.effective_chat.id, video=open(video.default_filename, 'rb'))

        # Удаляем скачанный файл после отправки
        os.remove(video.default_filename)
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка при скачивании видео: {e}")


# Функция для обработки сообщений, содержащих ссылку на видео с YouTube
def handle_video_link(update, context):
    video_url = update.message.text
    if "youtube.com" in video_url:
        download_video(update, context)
    else:
        update.message.reply_text("Это не ссылка на видео с YouTube. Пожалуйста, отправьте ссылку на YouTube видео.")


# Основная функция для запуска бота
if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    # Создаем объект Updater с указанием токена бота
    updater = Updater("6354175201:AAF3jzUMszsjAS5x6wnzeJAwZInYR6W25dU")
    dispatcher = updater.dispatcher

    # Добавляем обработчик команды /start
    dispatcher.add_handler(CommandHandler("start", start))

    # Добавляем обработчик текстовых сообщений, содержащих ссылку на видео с YouTube
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_video_link))

    # Запускаем бота
    updater.start_polling()
    updater.idle()
