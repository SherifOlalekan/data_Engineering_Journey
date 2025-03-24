# Module 5 Homework 

## Question 1:
- Install spark
- Run Spark
- Create a local spark session
- Execute spark.version
```
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()
```
```
pyspark.__version__
```
#### '3.5.5'

## Question 2:
Read the October 2024 Yellow into a Spark Dataframe
```
!wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-10.parquet

df_yellow_oct = spark.read \
    .option("header", "true") \
    .parquet("yellow_tripdata_2024-10.parquet")
```
Repartition the Dataframe to 4 partitions and save it to parquet.
```
df_yellow_oct \
        .repartition(4) \
        .write.parquet("tmp/yellow_oct")
```
Average size of each paraquet partition is **22.4**, close option is **B**

## Question 3: Count records 

How many taxi trips were there on the 15th of October?
```
df_yellow_oct.createOrReplaceTempView('oct_data')

spark.sql("""
SELECT
    EXTRACT(DAY FROM tpep_pickup_datetime) as day,
    COUNT(1) as trip_num
FROM
    oct_data
WHERE EXTRACT(DAY FROM tpep_pickup_datetime) = 15
GROUP BY day

""").show()
```
Number of trip is **128,893**, closest option is **C**

## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?
```
spark.sql("""
SELECT
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    DATEDIFF(minute, tpep_pickup_datetime, tpep_dropoff_datetime)/60 AS hour_diff,
    trip_distance
    
FROM
    oct_data
order by hour_diff DESC
""").show()
```
Longest trip in hours is **162.61...**, option **C**

## Question 5: User Interface

Spark’s User Interface which shows the application's dashboard runs on port **4040** option **C**

## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:
```
# write to parquet
df.write.parquet("lookup_zones")

# Load the zone lookup data into a temp view in Spark
df = spark.read.parquet("lookup_zones/part-00000-ee773c6e-6b73-419f-b3b9-a1bd783df62c-c000.snappy.parquet")
df.createOrReplaceTempView('lookup_zones')
```
Using the zone lookup data and the Yellow October 2024 data, what is the name of the LEAST frequent pickup location Zone?
```
spark.sql("""
SELECT
    lookup_zones.Zone,
    COUNT(1) as trip_num
      
FROM
    oct_data

INNER JOIN lookup_zones ON oct_data.PULocationID=lookup_zones.LocationID

GROUP BY Zone
ORDER BY trip_num ASC

""").show()
```
LEAST frequent pickup location Zone is **Governor's Island/Ellis Island/Liberty Island** Option **A**
