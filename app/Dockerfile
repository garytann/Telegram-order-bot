FROM python:3.10.0-alpine

WORKDIR /app

COPY . .

# RUN apt-get update \
# 	&& apt install libffi-dev build-essential -y 

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


