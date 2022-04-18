import logging

from pyspark.sql.functions import *

from etl_pipeline.connectors.postgre_connector import load_files, write_to_postgres, prepare_postgres_env
from etl_pipeline.dependencies.pd_spark_init import start_spark, postgres_init
from utils.plugins.custom_logger import ensure_basic_logging

LOG_FORMAT = " %(asctime)s %(levelname)-8s : %(name)s %(message)s"
logger = logging.getLogger("ETL_Pipeline_main")


@ensure_basic_logging(level=logging.INFO, format=LOG_FORMAT)
def main():
    """
    Main ETL Script definition
    Extract : load Parquet file
    Transform : data cleaning , transformation using pyspark
    Load : load it to postgreDB
    """

    spark_session = start_spark()
    connection = postgres_init()
    logger.info("Preparing initial stages")
    segment_sql_file = "../../utils/sql_models/segments.sql"
    raw_sql_file = "../../utils/sql_models/raw_data.sql"
    voucher_segmentation_file = "../../utils/sql_models/voucher_segments.sql"
    prepare_postgres_env(connection, "prerequisite_segmentation_of_voucher", segment_sql_file)
    prepare_postgres_env(connection, "prerequisite_creating schema_of_raw_table", raw_sql_file)

    logger.info("ETL Job started for postgres ")

    data = load_files(spark_session, "parquet", "../../data.parquet.gzip")

    data_transformed = transform_data(spark_session, data)

    # load data
    raw_df = data_transformed.toPandas()

    write_to_postgres(connection, raw_df, "voucher_payment_hist")
    prepare_postgres_env(connection, "creation of voucher segmentation in postgres", voucher_segmentation_file)


def transform_data(spark_session, spark_df):
    df = spark_df.na.drop(how="any")
    df.createOrReplaceTempView("rawdata")
    df_1 = spark_session.sql("SELECT * FROM rawdata where lower(country_code) = 'peru' AND total_orders IS NOT NULL \
          AND voucher_amount IS NOT NULL")
    df2 = df_1.withColumn('first_order_ts', to_timestamp(col('first_order_ts'))) \
        .withColumn('last_order_ts', to_timestamp(col('last_order_ts'))) \
        .withColumn('DiffInSeconds', col("last_order_ts").cast("long") - col('first_order_ts').cast("long")) \
        .withColumn('diff_in_days', col("DiffInSeconds") / 86400)
    df2.show(5)

    valid_df = df2.where("diff_in_days >= 0 and total_orders != 0").drop("DiffInSeconds")
    return valid_df


main()
