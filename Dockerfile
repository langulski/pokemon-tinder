# Use the official Python image as the base image
FROM python:3.11-slim

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /app
RUN set -eux; \
  apt-get update -qq; \
  apt-get full-upgrade -yqq; \
  apt-get install -y --no-install-recommends gcc;


COPY app /app
COPY .env /app/
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000