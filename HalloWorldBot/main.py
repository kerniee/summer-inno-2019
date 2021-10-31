import telebot
from telebot import types
import db
from os import getenv
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

#API_TOKEN = '930202745:AAF9git1r2RvVJmd2rABQ1VtAvTW9tsGyAY'
API_TOKEN = getenv('API_BOT_TOKEN')

bot = telebot.TeleBot(API_TOKEN)
qa = [['2+2*2', '6'], ['33+3+3', '39'], ['Three plus four', '7']]


@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    chat_id = message.chat.id
    db.set_state(chat_id, 0)

    bot.send_message(chat_id=chat_id,
                     text='''Hello {}, answer my questions, please :)'''.format(message.chat.first_name))
    bot.send_message(chat_id=chat_id,
                     text=qa[0][0])


@bot.message_handler(func=lambda message: db.get_state(message.chat.id) < len(qa))
def send_question(message):
    chat_id = message.chat.id
    state = db.get_state(chat_id)

    if message.text == qa[state][1]:
        db.set_state(chat_id, state+1)
        if state + 1 < len(qa):
            bot.send_message(chat_id=chat_id,
                             text='Right! Next Q')
            bot.send_message(chat_id=chat_id,
                             text=qa[state + 1][0])
        else:
            bot.send_message(chat_id=chat_id,
                             text='Congratulations! /restart to try again')
    else:
        bot.send_message(chat_id=chat_id,
                         text='Try again')


bot.polling()
