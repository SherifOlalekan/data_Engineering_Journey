FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_green_taxi.py ingest_green_taxi.py

ENTRYPOINT [ "python", "ingest_green_taxi.py"]