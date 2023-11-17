
# from BookStore.db.etl.data_preperation import data_generator
# from BookStore.db.etl.data_preperation import schema
# from BookStore.db.etl.data_preperation import sql_interactions


# db/etl/data_preparation/__init__.py
# Import necessary modules or functions from the 'data_preparation' sub-package.
from .data_generator import generate_customer, generate_orders
#from .schema import Customers, Books, Publisher, Authors, Inventory, OrderItem, Orders
# bookstore/db/etl/data_preparation/__init__.py
#from .schema import *
from .sql_interactions import SqlHandler
