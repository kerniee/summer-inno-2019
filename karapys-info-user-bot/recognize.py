import speech_recognition as sr
import sys

audios = sys.argv[1:]
if not audios:
    audios = input().split()
recognizer = sr.Recognizer()
texts = ''
for audio in audios:
    with sr.AudioFile(audio) as source:
        audio_file = recognizer.record(source)
    text = recognizer.recognize_google(audio_file, language='ru-RU')
    texts = texts + text + '\n'
print(texts)

