FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ=Europe/Istanbul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /code
RUN apt update
RUN apt install -y --assume-yes python3-dev libpq-dev build-essential python3-pip
RUN apt-get update
RUN pip install --upgrade pip

COPY main.py main.py
COPY config.py config.py
COPY docker-compose.yml docker-compose.yml
COPY Dockerfile Dockerfile
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt