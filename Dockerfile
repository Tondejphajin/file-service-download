FROM python:3.10-slim

WORKDIR /backend_download

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000