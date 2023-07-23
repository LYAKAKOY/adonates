FROM python:3.11-alpine3.18

WORKDIR /web_app

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000
RUN echo -e "http://nl.alpinelinux.org/alpine/v3.18/main\nhttp://nl.alpinelinux.org/alpine/v3.18/community" > /etc/apk/repositories

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

COPY ./web_app .