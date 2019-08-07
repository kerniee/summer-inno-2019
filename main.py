from flask import Flask, request
from os import getenv
import db
import string

server = Flask(__name__)


@server.route('/', methods=['POST'])
def echo():
    user_id = request.json['session']['user_id']
    end = False
    if request.json['session']['new'] and not db.get_state(user_id):
        response = {
            'version': request.json['version'],
            'session': request.json['session'],
            'response': {
                'text': 'Привет! Как тебя зовут?'
            }
        }
        db.set_state(user_id, '0')
    else:
        state = db.get_state(user_id)
        inp = request.json['request']['original_utterance']

        if inp.lower() in ('удалить', 'убрать'):
            if not db.delete_user(user_id):
                text = 'О вас еще нет информации'
            else:
                text = 'Удалена вся информация о вас! :)'
        elif inp.lower() in ('мои данные', 'данные'):
            name = db.get_user(user_id).name
            city = db.get_user(user_id).city
            text = f'Твое имя: {name}\nТвой город: {city}'
        elif state == 0:
            db.set_name(user_id, inp)
            db.set_state(user_id, 1)
            text = 'Круто! А откуда ты?'
        elif state == 1:
            db.set_city(user_id, inp)
            db.set_state(user_id, 2)
            text = 'Хороший город! Ладно, я все записал'
            end = True
        else:
            text = 'Я уже все записал'
        response = {
            'version': request.json['version'],
            'session': request.json['session'],
            'response': {
                'text': text,
                'end_session': end
            }
        }
    return response


server.run(host="0.0.0.0",
           port=int(getenv('PORT', 5000)))
