from flask import Flask, request
from os import getenv

server = Flask(__name__)


@server.route('/', methods=['POST'])
def echo():
    if request.json['session']['new']:
        response = {
            'version': request.json['version'],
            'session': request.json['session'],
            'response': {
                'text': 'Привет! Введи слово, чтобы проверить его на палиндром'
            }
        }
    else:
        inp = request.json['request']['original_utterance']
        if len(inp) > 1:
            text = 'Скажите одно слово'
        elif inp == inp[::-1]:
            text = 'Это палиндром! Попробуйте еще раз?'
        else:
            text = 'Это не палиндром! Попробуйте еще раз?'
        response = {
            'version': request.json['version'],
            'session': request.json['session'],
            'response': {
                'text': text
            }
        }
    return response


server.run(host="0.0.0.0",
           port=int(getenv('PORT', 5000)))
