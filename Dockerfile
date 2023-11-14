FROM python:3.8

WORKDIR /opt/exercicio_flask

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/opt/exercicio_flask:/opt/exercicio_flask
ENV PYTHONUNBUFFERED=1

CMD [ "python", "app.py" ]