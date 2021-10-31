import telebot
from flask import Flask, request
from os import getenv, makedirs
from os import path as p
import logging
from pydub import AudioSegment
import speech_recognition as sr

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = getenv('API_BOT_TOKEN_USER_INFO')
MODE = getenv('MODE')

bot = telebot.TeleBot(API_TOKEN)

server = Flask(__name__)

makedirs('files/voice/wav', exist_ok=True)
makedirs('files/documents', exist_ok=True)
makedirs('files/photos', exist_ok=True)


@bot.message_handler(content_types=['voice'])
def recognizer(message):
    sended_msg = bot.send_message(chat_id=message.chat.id,
                                  text=' Обрабатываю...')
    info = bot.get_file(message.voice.file_id)
    file_bytes = bot.download_file(info.file_path)
    with open(f'files/{info.file_path}', 'wb') as file:
        file.write(file_bytes)
    ogg = AudioSegment.from_ogg(f'files/{info.file_path}')
    path = info.file_path[:-3] + 'wav'
    path = p.join('files', 'voice', 'wav', p.basename(path))
    ogg.export(path, format='wav')
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio_file = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_file, language='ru-RU')
    except Exception:
        text = 'Не удалось распознать речь'
    bot.edit_message_text(chat_id=message.chat.id,
                          message_id=sended_msg.message_id,
                          text=text)


@server.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    json_update = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_update)

    bot.process_new_updates([update])
    return '', 200


if MODE == 'webhook':
    logger.info('Current mode: webhook')
    bot.remove_webhook()
    bot.set_webhook(url=getenv("WEBHOOK_URL") + API_TOKEN)

    server.run(host="0.0.0.0",
               port=int(getenv('PORT', 8443)))
else:
    bot.remove_webhook()
    bot.polling()
