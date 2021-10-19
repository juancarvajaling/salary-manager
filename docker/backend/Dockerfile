FROM python:3.9-slim

LABEL mainteiner="juancarvajaling@gmail.com"

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt update \
    && apt -y install netcat

WORKDIR /django_project

COPY ./django_project .

