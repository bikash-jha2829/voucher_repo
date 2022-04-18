from _pytest import unittest
from pyspark.sql import SparkSession

from etl_pipeline.jobs.etl_job import transform_data


class PySparkTestCase(unittest.TestCase):
    """Set-up of global test SparkSession"""

    @classmethod
    def setUpClass(cls):
        cls.spark = (SparkSession
                     .builder
                     .master("local[1]")
                     .appName("PySpark unit test")
                     .getOrCreate())

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()


class TransformTestCase(PySparkTestCase):

    def test_dataparser_schema(self):
        input_df = self.spark.createDataFrame(
            data=[['2020-05-20 15:43:38.364972+00:00', 'Peru', '2020-04-19 00:00:00+00:00', '2020-04-18 00:00:00+00:00', '1.0', '5720.0'],
                  ['2020-05-20 15:43:38.364972+00:00', 'China', '2020-04-18 00:00:00+00:00', '2020-04-19 00:00:00+00:00', '0.0', '5720.0']],
            schema=['timestamp', 'country_code', 'last_order_ts', 'first_order_ts', 'total_orders', 'voucher_amount'])

        transformed_df = transform_data(self.spark, input_df)

        expected_df = self.spark.createDataFrame(
            data=[['2020-05-20 15:43:38.364972+00:00', 'Peru', '2020-04-19 00:00:00+00:00', '2020-04-18 00:00:00+00:00', '1.0', '5720.0', '1.0']],
            schema=['timestamp', 'country_code', 'last_order_ts', 'first_order_ts', 'total_orders', 'voucher_amount', 'diff_in_days'])

        self.assertTrue(sorted(expected_df.collect()) == sorted(transformed_df.collect()))