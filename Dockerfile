FROM ubuntu:16.04

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

RUN apt-get update -y && \
    apt-get install -y python3.5 python-pip

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
