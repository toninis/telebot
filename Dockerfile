FROM python:2.7.15

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENV TELEBOT=''

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
