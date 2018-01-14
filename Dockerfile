FROM centos:latest

MAINTAINER Antonis Stamatiou "stamatiou.antonis@protonmail.com"

RUN yum update -y && yum install -y wget && wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
RUN rpm -ivh epel-release-latest-7.noarch.rpm
RUN yum update -y && yum install -y python 2.7 python-pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app
ENV TELEBOT='your-token'

ENTRYPOINT [ "python" ]

CMD [ "/app/telbot.py","--polling" ]
