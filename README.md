# voucher_repo

Task : 
The task is to create a Voucher Selection API for the country: Peru
There are 3 steps that should be done:

0. Conduct data analysis to explore and prepare the data.
1. Create a data pipeline to generate customer segments, including data cleaning, optimization.
2. Create a REST API that will expose the most used voucher value for a particular customer segment

Data Pipeline

EDA / Cleaning

Filter/Discard rows based on below :
1. Country = Peru (fetch all rows with country = Peru(case insenstive)
2. total_orders = 0 having first_order_ts/last_order_ts exists will be removed 
3. (last_order_ts - first_order_ts) < 0 / first_order_ts > last_order_ts.    will be discarded
4. Null check on  columns (total_orders / voucher_amount)

Data Pipeline details :
we used Spark framework as I tried to consider the scenario of huge data set (parquet format) to run analysis via distributed cluster computing.

Input File format : parquet
Output : write to Postgre DB

Model SQL : load segment rules / load raw data after spark transformation / joining the tables to get the final dataset into the postgre

voucher API:
localhost:5051/selection_criteria : get the list of segemnt rules criteria
localhost:5000/search_voucher : geenrates an input form to run a post request and feetch the desired voucher

Alternatively we can run a test method (run_sample.py)
from datetime import datetime

import requests

url = 'http://localhost:5051/voucher'
myobj = {
    "customer_id": 123,
    "total_orders": 30,
    "country_code": "Peru",
    "last_order_ts": "2020-07-19 00:00:00",
    "first_order_ts": "2020-04-18 00:00:00",
    "segment_name": "recency_segment"
}

x = requests.post(url, json=myobj)

print(x.text)



How to run :
1. Pycharm : Run the requirements.txt file 
    1. run the postgre instance ( docker_container/Docker.yaml or docker-compose.yaml)
    2. RUN spark job to load postgres data for pre-requisite ( etl_pipeline/jobs/etl_job.py)
    3. Run voucher_api/voucher_selection_api.py to run the api
    4. Chrome and hit the endpoints












