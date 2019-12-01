FROM python:3.7.1

LABEL Author="Heather Moore"
LABEL E-mail="hm90@example.com"
LABEL version="0.0.1"

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

CMD flask run --host=0.0.0.0 --port=8080
