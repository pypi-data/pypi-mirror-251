FROM python:3.8-slim-buster

RUN pip install arkitekt[all]

RUN mkdir /app
WORKDIR /app
COPY .arkitekt /app/.arkitekt
COPY app.py /app/app.py
