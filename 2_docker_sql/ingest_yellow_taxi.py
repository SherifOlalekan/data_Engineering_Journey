#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time

from sqlalchemy import create_engine
import pandas as pd



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'

    # download the csv: use wget to download the data from the url provided, -O write it to the file (csv_name)
    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")

    df.to_sql(name=table_name, con=engine, if_exists="append")


    while True:
        try:
            t_start = time()
            df = next(df_iter)

            df.tpep_pickup_datetime=pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime=pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name=table_name, con=engine, if_exists="append")

            t_end = time()

            print("Inserting another chunk....., took %.3f seconds" % (t_end - t_start))

        except StopIteration:
                print("Finished ingesting data into the Postgres database")
                break

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgress")

    parser.add_argument("--user", required=True, help="username for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="databse name for postgres")
    parser.add_argument("--table_name", required=True, help="name of the table where we will write the results to")
    parser.add_argument("--url", required=True, help="url of the csv file")

    args = parser.parse_args()

    main(args)

#to activate the ingestion script;
# URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

# python ingest_yellow_taxi.py \
#     --user = root \
#     --password = root \
#     --host = localhost \
#     --port = 5432 \
#     --db = ny_taxi \
#     --table_name = yellow_taxi_trips \
#     --url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"


#To dockerize the script

#first build the docker image:
# docker build -t taxi_ingest:v01 .

# To run the docker image taxi_ingest:v01;
# docker run -it \
#     --network=pg-network \ (i'm not sure about this yet)
#     taxi_ingest:v01 \
#         --user = root \
#         --password = root \
#         --host = 172.18.0.1 \
#         --port = 5432 \
#         --db = ny_taxi \
#         --table_name = yellow_taxi_trips \
#         --url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

