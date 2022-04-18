import logging

import psycopg2
from pyspark.sql import SparkSession

from utils.plugins.custom_logger import ensure_basic_logging

LOG_FORMAT = " %(asctime)s %(levelname)-8s : %(name)s %(message)s"
logger = logging.getLogger("pd_spark_init")

'''
This package is to initialize spark session , streaming context and spark context
we just created spark session for our use case

'''


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def start_spark(app_name='postgres_etl', jar_packages=[], master="local[2]", spark_config={}):
    """
    Start a spark session
    Spark since we need to read parquet file
    jar packages : dependencies with different connectors
    """
    logging.info("Creating Spark session")
    try:
        # get Spark session factory
        spark_session = (
            SparkSession
                .builder
                .master(master)
                .appName(app_name)
                .config("parquet.enable.summary-metadata", "false")
                .getOrCreate())
    except Exception as err:
        raise err

    return spark_session


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def postgres_init(connection=None, **kwargs):
    logger.info("Creating psycopg2 connection")
    if not connection:
        connection = psycopg2.connect(user="voucher",
                                      password="password",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="voucher",
                                      options="-c search_path=raw,model_staging,model_production")
    logger.info("Successfully created psycopg2 connection")
    return connection


def start_spark_streaming(stream_name="demo stream"):
    pass
