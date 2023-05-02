FROM python:3.9

ENV PYTHONUNBUFFERED=1

RUN mkdir /torob
WORKDIR /torob

RUN pip install --upgrade pip
COPY q1/requirements.txt /torob/
RUN pip install -r requirements.txt

COPY . /torob/