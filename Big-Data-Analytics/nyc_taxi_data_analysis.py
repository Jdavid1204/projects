"""
Script Summary:
This script processes NYC Yellow Taxi trip data using PySpark to perform various analytics tasks.
It sets up an S3 connection for data access and computes metrics like trip counts,
average tips per passenger, and top routes based on tipping behavior.

Imports:
- Standard and external libraries for file handling, date-time manipulation, and Spark functionality.
"""

import sys, string
import os
import socket
from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.sql.functions import from_unixtime, date_format, col, to_date, concat_ws, sum, month, to_timestamp, count, lit
from pyspark.sql.types import FloatType, IntegerType, StructType, StructField, StringType, DoubleType, TimestampType



if __name__ == "__main__":

    # Initialise Spark session
    spark = SparkSession\
        .builder\
        .appName("task1")\
        .getOrCreate()
    
    # Retrieve S3 configuration details from environment variables
    s3_data_repository_bucket = os.environ['DATA_REPOSITORY_BUCKET']
    s3_endpoint_url = os.environ['S3_ENDPOINT_URL']+':'+os.environ['BUCKET_PORT']
    s3_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    s3_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    s3_bucket = os.environ['BUCKET_NAME']

    # Configure Hadoop settings for S3 access
    hadoopConf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoopConf.set("fs.s3a.endpoint", s3_endpoint_url)
    hadoopConf.set("fs.s3a.access.key", s3_access_key_id)
    hadoopConf.set("fs.s3a.secret.key", s3_secret_access_key)
    hadoopConf.set("fs.s3a.path.style.access", "true")
    hadoopConf.set("fs.s3a.connection.ssl.enabled", "false")


    # Load and inspect data
    taxi_zone_lookupDF = spark.read.format("csv").options(header='True').csv("s3a://" + s3_data_repository_bucket + "/ECS765/nyc_taxi/taxi_zone_lookup.csv")
    taxi_zone_lookupDF.printSchema()
    
    yellow_taxiDF = spark.read.format("csv").options(header='True').csv("s3a://" + s3_data_repository_bucket + "/ECS765/nyc_taxi/yellow_tripdata/2023/*.csv")
    yellow_taxiDF.printSchema()
    print("The number of entries is: " + str(yellow_taxiDF.count()))


    # Filter data based on fare and trip conditions
    filteredDF = yellow_taxiDF.filter((col("fare_amount") > 50) & (col("trip_distance") < 1))
    date_filteredDF = filteredDF.filter((col("tpep_pickup_datetime") >= to_date(lit("2023-02-01"), "yyyy-MM-dd")) & (col("tpep_pickup_datetime") <= to_date(lit("2023-02-08"), "yyyy-MM-dd")))

    # Create a new column trip_date with the rows of tpeppickup in a different format. Then group then by day and count the number of rows(trips) of each column(day)
    # Aggregate trip counts by day
    num_tripsDF = date_filteredDF.withColumn("trip_date", date_format(col("tpep_pickup_datetime"), "yyyy-MM-dd")).groupBy("trip_date").count().withColumnRenamed("count", "trip_count").orderBy("trip_date")
    
    num_tripsDF.show(truncate=False)


    # Join taxi zone and trip data for borough information
    zone_lookup_yellow = yellow_taxiDF.join(taxi_zone_lookupDF, yellow_taxiDF["PULocationID"] == taxi_zone_lookupDF["LocationID"], "left").withColumnRenamed("Borough", "Pickup_Borough").withColumnRenamed("zone", "Pickup_Zone").withColumnRenamed("service_zone", "Pickup_service_zone").drop("LocationID", "PULocationID")
    second_join = zone_lookup_yellow.join(taxi_zone_lookupDF, zone_lookup_yellow["DOLocationID"] == taxi_zone_lookupDF["LocationID"], "left").withColumnRenamed("Borough", "Dropoff_Borough").withColumnRenamed("zone", "Dropoff_Zone").withColumnRenamed("service_zone", "Dropoff_service_zone.").drop("LocationID", "DOLocationID")
    second_join.printSchema()


    # Add route and month columns for analysis
    routeDF = second_join.withColumn("route", concat_ws(" to ", second_join["Pickup_Borough"], second_join["Dropoff_Borough"]))
    route_monthDF = routeDF.withColumn("Month", month(to_timestamp(second_join["tpep_pickup_datetime"], "yyyy-MM-dd HH:mm:ss")))

    route_monthDF.show(10,truncate=False)


    # Compute total and average tips per passenger by route and month
    total_tip_passengerDF = route_monthDF.groupBy("Month", "route").agg(sum("tip_amount").alias("total_tip_amount"), sum("passenger_count").alias("total_passenger_count"))
    avg_tip_passengerDF = total_tip_passengerDF.withColumn("average_tip_per_passenger", col("total_tip_amount") / col("total_passenger_count"))
    avg_tip_passengerDF.select("Month", "route", "total_tip_amount", "total_passenger_count", "average_tip_per_passenger").show(10, truncate=False)


    # Filter routes with zero average tips per passenger
    filtered_avg_tip_passenger = avg_tip_passengerDF.filter(col("average_tip_per_passenger") == 0)
    filtered_avg_tip_passenger.select("Month", "route", "total_tip_amount", "total_passenger_count", "average_tip_per_passenger").show(truncate=False)


    # Display top 10 routes by average tips per passenger
    sorted_routesDF = avg_tip_passengerDF.orderBy(col("average_tip_per_passenger").desc()).limit(10)
    sorted_routesDF.select("Month", "route", "total_tip_amount", "total_passenger_count", "average_tip_per_passenger").show(truncate=False)


    # Stop the Spark session
    spark.stop()