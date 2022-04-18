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