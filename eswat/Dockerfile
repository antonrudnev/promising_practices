FROM python:3.7

WORKDIR /eswat

COPY src/requirements.txt /eswat

RUN pip install -r requirements.txt

COPY src /eswat

EXPOSE 5000

CMD flask run --host=0.0.0.0 --port=5000
