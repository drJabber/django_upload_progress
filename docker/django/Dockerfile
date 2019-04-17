FROM python:3.7


ENV PYTHONUNBUFFERED 1

RUN apt update 
RUN apt install -y binutils libproj-dev gdal-bin

COPY ./requirements.txt /requirements.txt
COPY ./info/404.png /info/404.png
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

WORKDIR /app
