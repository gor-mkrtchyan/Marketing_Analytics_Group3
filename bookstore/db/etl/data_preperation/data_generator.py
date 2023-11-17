from faker import Faker
from datetime import datetime
import pandas as pd
import random
import logging
import os



logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
fake=Faker()

# Data Models

#Generate Customer Table
def generate_customer(customer_id):
    return {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "street_address": fake.street_address(),
        "state": fake.state(),
        "city": fake.city(),
        "zip_code": fake.zipcode()
    }

from datetime import datetime

def generate_orders(order_id):
    # Generate a random date between a specific date range
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_date = fake.date_time_between_dates(start_date, end_date)

    return {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": random_date,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total
    }

