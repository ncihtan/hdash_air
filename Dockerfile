FROM apache/airflow:2.4.0-python3.10

COPY Dockerfile .

USER root
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt --assume-yes install \
    python3-dev \
    freetds-dev \
    build-essential \
    openssl \
    libssl-dev \
    libenchant-2-dev \
    postgresql \
    libkrb5-dev
USER airflow

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
