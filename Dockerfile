FROM python:3.9.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1
ENV GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
ENV GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/project/app

WORKDIR /opt/project/app
RUN chmod a+x ./entrypoint.sh

EXPOSE 8000

ENTRYPOINT /opt/project/app/entrypoint.sh