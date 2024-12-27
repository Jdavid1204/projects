"""
Script Summary:
This script utilises PySpark and GraphFrames to analyse NYC Green Taxi data.
It creates a graph structure from taxi trips and zones, computes various graph metrics such as shortest paths and PageRank, and performs filtering and transformations on the data.

Imports:
- Standard and external libraries for system operations, graph computations, and Spark functionality.
"""

import sys, string
import os
import socket
import time
import operator
import boto3
import json
from pyspark.sql import SparkSession
from datetime import datetime

from functools import reduce
from pyspark.sql.functions import col, lit, when, concat_ws
from pyspark import *
from pyspark.sql import *
from pyspark.sql.types import *
import graphframes
from graphframes import *


if __name__ == "__main__":

    # Initialise Spark session with GraphFrames package
    spark = SparkSession\
        .builder\
        .config("spark.jars.packages", "graphframes:graphframes:0.8.2-spark3.2-s_2.12")\
        .appName("graphframes")\
        .getOrCreate()

    sqlContext = SQLContext(spark)
    # shared read-only object bucket containing datasets
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

    
    # Load and inspect Green Taxi trip data
    green_taxi_monthsDF = spark.read.format("csv").options(header='True').csv("s3a://" + s3_data_repository_bucket + "/ECS765/nyc_taxi/green_tripdata/2023/*csv")
    green_taxi_monthsDF.printSchema()
    print("The number of entries is: " + str(green_taxi_monthsDF.count()))

    # Define schemas and create graph vertices and edges
    vertexSchema = StructType([StructField("LocationID", IntegerType(), False),
                               StructField("Borough", StringType(), True),
                               StructField("Zone", StringType(), True),
                               StructField("service_zone", StringType(), True)])

    edgeSchema = StructType([StructField("lpep_pickup_datetime", StringType(), False),
                             StructField("lpep_dropoff_datetime", StringType(), False),
                             StructField("PULocationID", StringType(), False),
                             StructField("DOLocationID", StringType(), False)])
    
    # Load edges and vertices data
    edgesDF = spark.read.format("csv").options(header='True').schema(edgeSchema).csv("s3a://" + s3_data_repository_bucket + "/ECS765/nyc_taxi/green_tripdata/2023/*csv").withColumnRenamed("PULocationID", "src").withColumnRenamed("DOLocationID", "dst").select("src", "dst")
    verticesDF = spark.read.format("csv").options(header='True').schema(vertexSchema).csv("s3a://" + s3_data_repository_bucket + "/ECS765/nyc_taxi/taxi_zone_lookup.csv").withColumnRenamed("LocationID", "id")
    edgesDF.show(5, truncate=False)
    verticesDF.show(5, truncate=False)

    # Create a graph and display triplets
    graph = GraphFrame(verticesDF, edgesDF)
    graph.triplets.show(10, truncate=False)

    # Analyse connected boroughs and zones within the same service area
    connected_borough = graph.edges.join(graph.vertices, graph.edges.src == graph.vertices.id, "inner").withColumnRenamed("id", "id_src").withColumnRenamed("Borough", "Borough_src").withColumnRenamed("service_zone","service_zone_src")
    
    connected_borough_zone = connected_borough.join(graph.vertices, graph.edges.dst == graph.vertices.id, "inner").withColumnRenamed("id", "id_dst").withColumnRenamed("Borough", "Borough_dst").withColumnRenamed("service_zone","service_zone_dst").filter((col("Borough_src") == col("Borough_dst")) & (col("service_zone_src") == col("service_zone_dst")))
    
    connected_borough_zoneFinal = connected_borough_zone.select(col("id_src").alias("id"), col("id_dst").alias("id"), col("Borough_src").alias("Borough"), col("service_zone_src").alias("service_zone"))
    print("count:" + str(connected_borough_zoneFinal.count()))
    connected_borough_zoneFinal.show(10, truncate=False)

    # Compute shortest paths to landmark node "1"
    shortest_paths = graph.shortestPaths(landmarks=["1"])
    shortest_paths_to_1 = shortest_paths.select(concat_ws("->",col("id"), lit("1")).alias("id_to_1"), col("distances").getItem("1").alias("shortest_distance"))
    shortest_paths_to_1.show(10, truncate=False)

    # Compute PageRank for graph vertices
    page_rank = graph.pageRank(resetProbability=0.17, tol=0.01).vertices.sort("pagerank", ascending=False)
    page_rank.select("id", "pagerank").show(5,truncate=False)
    
    # Stop the Spark session
    spark.stop()
