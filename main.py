from flask import Flask, request
from os import getenv
import db

server = Flask(__name__)


@server.route('/', methods=['POST'])
def echo():
    user_id = str(request.json['session']['user_id'])
    end = False
    if request.json['session']['new']:
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
        if state == 0:
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
