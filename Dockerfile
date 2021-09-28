FROM python:3.9-slim

RUN apt update \
    && apt install -y graphviz \
    && rm -r /var/cache/apt/

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -U -r /requirements.txt

COPY src /src
WORKDIR /src
ENV PYTHONPATH=/src
