FROM python:2.7

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

WORKDIR /app
RUN pip install telegram python-telegram-bot
COPY telbot.py /app

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
