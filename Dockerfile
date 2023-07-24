# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /webapp

COPY ./requirements.txt /webapp

RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=1
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]