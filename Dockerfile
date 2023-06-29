FROM python:3.11-alpine

WORKDIR /web_app

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

COPY ./web_app .