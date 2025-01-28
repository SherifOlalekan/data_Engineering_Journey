# Module 1 Homework Solution: Docker & SQL

## Question 1.  
```
docker run -it --entrypoint bash python:3.12.8
pip --version
```
### Ans:
- 24.3.1



## Question 2.
Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the postgres database?

### Ans:
- postgres:5433


## Question 3. Trip Segmentation Count
*This is a confusing question, i really don't understand it. More clearity will be appreciated.*



## Question 4. Longest trip for each day
Which was the pick up day with the longest trip distance?
```
SELECT
DATE(lpep_pickup_datetime), trip_distance
FROM green_taxi_data
ORDER BY trip_distance DESC
LIMIT 1;
```
### Ans:
- 2019-10-31


## Question 5. Three biggest pickup zones
Which were the top pickup locations with over 13,000 in
`total_amount` (across all trips) for 2019-10-18?
```
SELECT "Zone", "PULocationID", SUM(total_amount) AS total_amount
FROM green_taxi_data
INNER JOIN zones
ON green_taxi_data."PULocationID" = zones."LocationID"
WHERE DATE(lpep_pickup_datetime) = '2019-10-18'
GROUP BY "PULocationID", "Zone"
HAVING SUM(total_amount) > 13000
ORDER BY total_amount DESC;
```
### Ans: 
- East Harlem North, East Harlem South, Morningside Heights


## Question 6. Largest tip
For the passengers picked up in October 2019 in the zone
named "East Harlem North" which was the drop off zone that had
the largest tip?
```
SELECT z2."Zone", MAX(t.tip_amount) AS max_tip
FROM green_taxi_data t
JOIN zones z1 ON t."PULocationID" = z1."LocationID"
JOIN zones z2 ON t."DOLocationID" = z2."LocationID"
WHERE z1."Zone" = 'East Harlem North'
AND t.lpep_pickup_datetime >= '2019-10-01'
AND t.lpep_pickup_datetime < '2019-11-01'
GROUP BY z2."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```
### Ans:
- JFK Airport

## Question 7. Terraform Workflow

Which of the following sequences, **respectively**, describes the workflow for: 
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

### Ans:
- terraform init, terraform apply -auto-approve, terraform destroy
