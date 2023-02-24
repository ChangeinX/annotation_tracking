FROM python:3.9-alpine

RUN apk update && apk add --no-cache postgresql-libs && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

ENV FLASK_APP run.py
ENV FLASK_CONFIG docker

RUN adduser -D nathan
USER nathan

WORKDIR /home/nathan


COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY run.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]