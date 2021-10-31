FROM python:3.7-alpine

COPY . echo-bot
WORKDIR echo-bot

RUN pip install -r requirements.txt
CMD ["python", "main.py"]