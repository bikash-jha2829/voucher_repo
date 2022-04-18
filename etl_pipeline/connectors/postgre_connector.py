import logging
import os
from typing import List

import pandas as pd
import psycopg2

from utils.plugins.custom_logger import ensure_basic_logging

LOG_FORMAT = " %(asctime)s %(levelname)-8s : %(name)s %(message)s"
logger = logging.getLogger("postgres_connector")


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def load_files(spark_session, file_type: str, path: str):
    """
    Method to read parquet file using spark
    much more optimized as compared to read it via pandas df using pyarrow engine
    """
    logger.info(f"Loading {file_type} format :: {path}")
    input_df = spark_session \
        .read.format(file_type) \
        .options(header=True, inferSchema=True) \
        .load(path)

    return input_df


def load_to_db(spark_session, db_type):
    pass


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def write_to_postgres(connection, write_df: pd.DataFrame, table):
    cursor = connection.cursor()
    # Save the dataframe to disk
    tmp_df = "./tmp_dataframe.csv"
    write_df.to_csv(tmp_df, index=False, header=False)
    f = open(tmp_df, 'r')
    try:
        cursor.copy_from(f, table, sep=",")
        connection.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        os.remove(tmp_df)
        logger.error("Error: %s" % error)
        connection.rollback()
        cursor.close()
        raise error
    logger.info("copy_from_file() done")
    cursor.close()
    os.remove(tmp_df)


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def prepare_postgres_env(connection, stage: str, sql_file):
    logger.info(f"preparing {stage}  stage in ETL")
    with connection.cursor() as cursor:
        try:
            logger.info(f"running sql file :: {sql_file}")
            cursor.execute(open(sql_file, "r").read())
        except (TypeError, Exception) as err:
            connection.rollback()
            cursor.close()
            raise err
