"""
Script Summary:
This script analyses Ethereum blockchain data using PySpark.
It retrieves data from S3 storage, performs data transformations and computations such as identifying top miners,
formatting timestamps, and analysing transactions and blocks by date.

Imports:
- Standard and external libraries for system operations, date manipulation, and Spark functionality.
"""

import sys, string
import os
import math
import socket
from pyspark.sql import SparkSession
from datetime import datetime

from pyspark.sql.functions import from_unixtime, date_format, col, to_date, concat_ws, sum, month, to_timestamp, count, \
    year, countDistinct, expr, round, unix_timestamp, udf
from pyspark.sql.types import FloatType, IntegerType, DoubleType

if __name__ == "__main__":

     # Initialise Spark session
    spark = SparkSession \
        .builder \
        .appName("task2") \
        .getOrCreate()
    
    # Retrieve S3 configuration details from environment variables
    s3_data_repository_bucket = os.environ['DATA_REPOSITORY_BUCKET']
    s3_endpoint_url = os.environ['S3_ENDPOINT_URL'] + ':' + os.environ['BUCKET_PORT']
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


    # Load and inspect Ethereum blocks and transactions data
    blocksDF = spark.read.option("inferSchema", "true").format("csv").options(header='True').csv("s3a://" + s3_data_repository_bucket + "/ECS765/ethereum/blocks.csv")
    blocksDF.printSchema()
    
    transactionsDF = spark.read.format("csv").options(header='True').csv("s3a://" + s3_data_repository_bucket + "/ECS765/ethereum/transactions.csv")
    transactionsDF.printSchema()

    # Identify top 10 miners by total block size
    minersDF = blocksDF.groupBy("miner").sum("size").orderBy(col("sum(size)").desc()).withColumnRenamed("sum(size)", "total_size").limit(10)
    minersDF.select("miner", "total_size").show(truncate=False)

    # Convert block timestamps to human-readable date format
    unixformat_to_dateDF = blocksDF.withColumn("formatted_data", to_date(date_format(from_unixtime(col("timestamp")), "yyyy-MM-dd"))).limit(10)
    unixformat_to_dateDF.select("timestamp", "formatted_data").show(truncate=False) 

    # Perform an inner join between transactions and blocks using block hashes
    blocksDF_renamed = blocksDF.withColumnRenamed("hash", "hash_in_blocks")
    inner_join = transactionsDF.join(blocksDF_renamed, transactionsDF["block_hash"] ==  blocksDF_renamed["hash_in_blocks"], "inner")
    print("The number of entries is: " + str(inner_join.count()))
    #inner_join.limit(10).show(truncate=False)


    # Analyse unique senders and block counts for September
    num_blocks_sendersDF = inner_join.withColumn("formatted_date", to_date(date_format(from_unixtime(col("timestamp")), "yyyy-MM-dd"))).filter((month(col("formatted_date")) == 9) & (col("transaction_index") == 0)).groupBy("formatted_date").agg(count("hash_in_blocks").alias("block_count"), countDistinct("from_address").alias("unique_senders_count_number")).orderBy(col("formatted_date").asc())
    
    num_blocks_sendersDF.show(30,truncate=False)
    
    # Analyse October transaction fees and block counts
    block_countDF = num_blocks_sendersDF = inner_join.withColumn("formatted_date", to_date(date_format(from_unixtime(col("timestamp")), "yyyy-MM-dd"))).filter((month(col("formatted_date")) == 10) & (col("transaction_index") == 0)).groupBy("formatted_date").agg(count("hash_in_blocks").alias("block_count"))

    october_transaction_feeDF = inner_join.withColumn("formatted_date", to_date(date_format(from_unixtime(col("timestamp")), "yyyy-MM-dd"))).filter((month(col("formatted_date")) == 10) & (col("transaction_index") == 0)).withColumn("transaction_fee", col("gas") * col("gas_price")).groupBy("formatted_date").agg(sum("transaction_fee").alias("total_transaction_fee"))

    block_oct_transactionDF = october_transaction_feeDF.join(block_countDF, "formatted_date", "inner").orderBy(col("formatted_date").asc())
    
    block_oct_transactionDF.select("formatted_date","total_transaction_fee", "block_coun").show(31,truncate=False)
    

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_%H:%M:%S")
    num_blocks_sendersDF.coalesce(1).write.csv("s3a://" + s3_bucket + "/task2_q5" + date_time + ".csv", header=True)
    block_oct_transactionDF.coalesce(1).write.csv("s3a://" + s3_bucket + "/task2_q6" + date_time + ".csv", header=True)


    # Stop the Spark session
    spark.stop()