## Running Spark in the Cloud

### Connecting to Google Cloud Storage 

Uploading data to GCS:

```bash
gsutil -m cp -r pq/ gs://dtc_data_lake_de-zoomcamp-nytaxi/pq
```

Create a lib folder and Download the jar for connecting to GCS


```
gsutil cp gs://hadoop-lib/gcs/gcs-connector-hadoop3-latest.jar ./lib/gcs-connector-hadoop3-latest.jar
```


### Local Cluster and Spark-Submit

Creating a stand-alone cluster ([docs](https://spark.apache.org/docs/latest/spark-standalone.html)):

```bash
./sbin/start-master.sh
```

Creating a worker:

```bash
URL="spark://data-engineer-2753.africa-south1-a.c.my-de-journey.internal:7077"
./sbin/start-worker.sh ${URL}

```

Turn the notebook into a script:

```bash
jupyter nbconvert --to=script 06_spark_sql.ipynb
```

Edit the script and then run it:

```bash 
python 06_spark_sql.py \
    --input_green=data/pq/green/2020/*/ \
    --input_yellow=data/pq/yellow/2020/*/ \
    --output=data/report-2020
```

Use `spark-submit` for running the script on the cluster

```bash
URL="spark://data-engineer-2753.africa-south1-a.c.my-de-journey.internal:7077"

spark-submit \
    --master="${URL}" \
    06_spark_sql.py \
        --input_green=data/pq/green/2021/*/ \
        --input_yellow=data/pq/yellow/2021/*/ \
        --output=data/report-2021
```

### Data Proc

Upload the script to GCS:

```bash
gsutil -m cp -r 06_spark_sql.py gs://olalekanroy-data-bucket/code/06_spark_sql.py
```

Params for the job:

* `--input_green=gs://olalekanroy-data-bucket/pq/green/2021/*/`
* `--input_yellow=gs://olalekanroy-data-bucket/pq/yellow/2021/*/`
* `--output=gs://olalekanroy-data-bucket/report-2021`

olalekanroy-data-bucket
olalekanroy-data-bucket/pq

```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=africa-south1 \
    gs://dtc_data_lake_de-zoomcamp-nytaxi/code/06_spark_sql.py \
    -- \
        --input_green=gs://olalekanroy-data-bucket/pq/green/2020/*/ \
        --input_yellow=gs://olalekanroy-data-bucket/pq/yellow/2020/*/ \
        --output=gs://olalekanroy-data-bucket/report-2020
```

### Big Query

Upload the script to GCS:

```bash
gsutil -m cp -r 06_spark_sql_big_query.py gs://olalekanroy-data-bucket/code/06_spark_sql_big_query.py
```


```bash
gcloud dataproc jobs submit pyspark \
    --cluster=de-zoomcamp-cluster \
    --region=africa-south1 \
    gs://olalekanroy-data-bucket/code/06_spark_sql_big_query.py \
    -- \
        --input_green=gs://olalekanroy-data-bucket/pq/green/2020/*/ \
        --input_yellow=gs://olalekanroy-data-bucket/pq/yellow/2020/*/ \
        --output=trips_data_all.reports-2020
```