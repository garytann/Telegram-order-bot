FROM python:3.10.0-alpine

WORKDIR /backend

COPY . .

EXPOSE 8000

RUN apk add --no-cache build-base

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt
