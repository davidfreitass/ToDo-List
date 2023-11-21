FROM python:3.8-alpine

WORKDIR /opt/exercicio_flask

COPY requirements.txt .

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/opt/exercicio_flask:/opt/exercicio_flask
ENV PYTHONUNBUFFERED=1

# CMD [ "python", "app.py" ]