FROM python:3.9-alpine
RUN apk add build-base
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
