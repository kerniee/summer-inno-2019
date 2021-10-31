import telebot
from flask import Flask, request
from os import getenv
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

API_TOKEN = getenv('API_BOT_TOKEN_USER_INFO')

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)
qa = [['2+2*2', '6'], ['33+3+3', '39'], ['Three plus four', '7']]


@bot.message_handler(func=lambda message: True)
def send_question(message):
    if state + 1 < len(qa):
        bot.send_message(chat_id=message.chat.id,
        text='{}/nId: {}/nFirst: {}'.format(
            message.from_user.username,
            message.from_user.id,
            message.from_user.first_name
        ))


@server.route('/' + API_TOKEN, methods=['POST'])
def get_message():
    json_update = request.stream.read().decode('utf-8')
    update = telebot.types.Update.de_json(json_update)

    bot.process_new_updates([update])
    return '', 200


bot.remove_webhook()
bot.set_webhook(url=getenv("WEBHOOK_URL") + API_TOKEN)

server.run(host="0.0.0.0",
           port=int(getenv('PORT', 8443)))
