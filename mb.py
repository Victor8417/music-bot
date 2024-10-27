import telebot
from pytubefix import YouTube
import os

# Инициализация бота с вашим токеном и ID канала
TOKEN = '8181794539:AAENaPKR9ltnKXlXILoRFw9eJFnjfH2J7c8'
CHANNEL_ID = '@vimusic1488'  # Вставьте сюда ID вашего канала
bot = telebot.TeleBot(TOKEN)


# Функция для загрузки аудио и отправки пользователю и в канал
def download_and_send_audio(link, chat_id):
    try:
        yt = YouTube(link)
        stream = yt.streams.filter(only_audio=True).first()  # Получаем аудиопоток

        if stream is None:
            bot.send_message(chat_id, "Не удалось найти аудиопоток в этом видео.")
            return

        audio_path = stream.download(filename=f"{yt.title}.mp3")  # Загружаем аудио с именем из YouTube
        bot.send_message(chat_id, "Аудиофайл загружен, отправка...")  # Сообщение о загрузке

        # Проверяем, существует ли файл перед отправкой
        if os.path.exists(audio_path):
            with open(audio_path, 'rb') as audio:
                # Отправляем аудиофайл пользователю
                bot.send_audio(chat_id=chat_id, audio=audio, title=yt.title)

                # Сохраняем позицию файла и пересылаем в канал
                audio.seek(0)  # Возвращаемся в начало файла перед отправкой в канал
                bot.send_audio(chat_id=CHANNEL_ID, audio=audio, title=yt.title)

            bot.send_message(chat_id, "Аудиофайл успешно отправлен.")  # Успешное отправление
        else:
            bot.send_message(chat_id, "Файл не найден для отправки.")

        os.remove(audio_path)  # Удаляем файл после отправки
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка: {e}")


# Обработка ссылок, отправленных пользователем
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Отправь ссылку на YouTube видео, и я отправлю аудиофайл.")


@bot.message_handler(content_types=['text'])
def handle_message(message):
    url = message.text.strip()
    if url.startswith("http") and ("youtube.com" in url or "youtu.be" in url):
        download_and_send_audio(url, message.chat.id)
    else:
        bot.reply_to(message, "Пожалуйста, отправьте действительную ссылку на YouTube видео.")


bot.polling()





