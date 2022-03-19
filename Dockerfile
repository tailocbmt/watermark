FROM python:3.7-slim

RUN apt-get update 

COPY requirements.txt .
RUN pip install -r requirements.txt


WORKDIR /app
COPY . .

CMD python3 app.py
