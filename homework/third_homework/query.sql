-- Count number of records from regular table
SELECT COUNT(1) AS record_count FROM `my-de-journey.zoomcamp_data.yellow-taxi-data-regular`

-- Count distict on external and material table to check the size when run
SELECT COUNT(DISTINCT(PULocationID)) AS distinct_location FROM `my-de-journey.zoomcamp_data.yellow-taxi-data-regular`
-- Result: 155.12MB
SELECT COUNT(DISTINCT(PULocationID)) AS distinct_location FROM `my-de-journey.zoomcamp_data.external-yellow-taxi-data`
-- Result: 0B

SELECT PULocationID AS locationID FROM `my-de-journey.zoomcamp_data.yellow-taxi-data-regular`
-- 155.12MB
SELECT PULocationID, DOLocationID FROM `my-de-journey.zoomcamp_data.yellow-taxi-data-regular`
-- 310.24MB

-- Count of fare_amount=0
SELECT COUNT(fare_amount) AS numberOfZeroFare FROM `my-de-journey.zoomcamp_data.external-yellow-taxi-data` WHERE fare_amount=0;

--Create a partition and cluster table
CREATE OR REPLACE TABLE my-de-journey.zoomcamp_data.yellow_taxi_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `my-de-journey.zoomcamp_data.external-yellow-taxi-data`


SELECT DISTINCT(VendorID) FROM `my-de-journey.zoomcamp_data.yellow-taxi-data-regular`
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) < '2024-03-16'
-- Estimated process byte = 310.24MB for regular table

SELECT DISTINCT(VendorID) FROM `my-de-journey.zoomcamp_data.yellow_taxi_partitioned_clustered`
WHERE DATE(tpep_dropoff_datetime) >= '2024-03-01' AND DATE(tpep_dropoff_datetime) < '2024-03-16';
-- Estimated process byte = 26.84MB for partitioned and clustered table
