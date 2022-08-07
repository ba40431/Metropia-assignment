FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py"]