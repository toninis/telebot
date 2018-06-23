FROM python:alpine

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

WORKDIR /app
COPY . /app
RUN pip install -r /app/requirements.txt
ENV TELEBOT=''

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
