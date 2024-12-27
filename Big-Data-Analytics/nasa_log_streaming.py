"""
Script Summary:
This script processes streaming NASA log data using PySpark Structured Streaming.
It performs tasks such as extracting information from logs, defining watermarks for late data handling, filtering, grouping, and aggregating data, and writing the results to the console.

Imports:
- Standard and external libraries for system operations, date manipulation, and PySpark streaming functionality.
"""

import sys, string
import os
import socket
import time
import operator
import boto3
import json
from pyspark.sql import Row, SparkSession
from pyspark.sql.streaming import DataStreamWriter, DataStreamReader
from pyspark.sql.functions import explode, split, window, col, count
from pyspark.sql.types import IntegerType, DateType, StringType, StructType
from pyspark.sql.functions import sum, avg, max, when
from datetime import datetime

if __name__ == "__main__":

    # Initialise Spark session
    spark = SparkSession \
        .builder \
        .appName("NasaLogSparkStreaming") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    windowDuration = '60 seconds' # Duration of the aggregation window
    slideDuration = '30 seconds' # Duration for sliding window aggregation


    # Load data by specifying the host value and port value
    logsDF = spark.readStream.format("socket").option("host","stream-emulator.data-science-tools.svc.cluster.local").option("port", 5551).option('includeTimestamp', 'true').load()

    query = logsDF.writeStream.outputMode("append").option("truncate", "false").format("console").start()
    query.awaitTermination(1000)

    logsDF = logsDF.select(explode(split(logsDF.value, " ")).alias("logs"), logsDF.timestamp)


    # Define a watermark on the timestamp column with a delay of 3 seconds
    logsDF = logsDF.withWatermark("timestamp", "3 seconds")

    # Extract specific fields from the logs
    logsDF = logsDF.withColumn('idx', split(logsDF['logs'], ',').getItem(0)) \
        .withColumn('hostname', split(logsDF['logs'], ',').getItem(1)) \
        .withColumn('time', split(logsDF['logs'], ',').getItem(2)) \
        .withColumn('method', split(logsDF['logs'], ',').getItem(3)) \
        .withColumn('url', split(logsDF['logs'], ',').getItem(4)) \
        .withColumn('responsecode', split(logsDF['logs'], ',').getItem(5)) \
        .withColumn('bytes', split(logsDF['logs'], ',').getItem(6))


    # Output processed logs to the console
    query = logsDF.writeStream.outputMode("append").option("truncate", "false").format("console").start()
    query.awaitTermination(1000)


    # Count occurrences of GIF requests within a window
    gifDF = logsDF.filter(col("url").contains("gif"))
    windowedDF = gifDF.groupBy(window(col("timestamp"), windowDuration, slideDuration)).agg(count("url").alias("gif_count"))
    query = windowedDF.writeStream.outputMode("update").option("truncate", "false").format("console").start()
    query.awaitTermination(1000)


    # Aggregate total bytes transferred by hostname
    bytesHostDF = logsDF.groupBy(window(col("timestamp"), windowDuration, slideDuration), logsDF.hostname).agg(sum("bytes").alias("total_bytes")).orderBy(col("total_bytes").desc())
    query = bytesHostDF.writeStream.outputMode("complete").option("truncate", "false").format("console").start()
    query.awaitTermination(1000)                                                                                                          


    # Count successful GET requests by hostname
    getRequestDF = logsDF.filter((col("method") == "GET") & (col("responsecode") == "200"))
    numSuccessGetDF = getRequestDF.groupBy(logsDF.hostname).agg(count("*").alias("Correct_count"))
    query = numSuccessGetDF.writeStream.outputMode("complete").trigger(processingTime="10 seconds").option("truncate", "false").format("console").start()
    query.awaitTermination(1000)   


    # Pause to allow processing
    time.sleep(60) 

    query.stop()

    # Stop the Spark session
    spark.stop()

