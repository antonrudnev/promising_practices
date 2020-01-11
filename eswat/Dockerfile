FROM python:3.7-slim

WORKDIR /eswat

COPY src/requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

EXPOSE 5000

CMD gunicorn --bind=0.0.0.0:5000 --workers=2 --access-logfile=- wsgi:app
