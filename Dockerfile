FROM python

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
ENV TELEBOT=${TELEBOT}

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
