FROM python:3.8

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
COPY db.sqlite3 /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/