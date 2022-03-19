FROM python:3.7-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update 
RUN pip install opencv-python

WORKDIR /app
COPY . .

CMD python3 app.py
