FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_yellow_taxi.py ingest_yellow_taxi.py

ENTRYPOINT [ "python", "ingest_yellow_taxi.py"]
