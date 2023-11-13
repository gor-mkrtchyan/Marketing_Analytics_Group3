import os
import pandas as pd
import logging
from bookstore.db.etl.logger.logger import CustomFormatter

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


from sqlalchemy import create_engine,Column,Integer,String,Float, DATE, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

engine=create_engine('sqlite:///BookStore.db')

from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Customers(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    street_address = Column(String)
    state = Column(String)
    city = Column(String)
    zip_code = Column(String)

class Books(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    isbn = Column(String)
    publication_year = Column(Integer)
    language = Column(String)
    cover_type = Column(String)
    pages_number = Column(Integer)
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    publisher_id = Column(Integer, ForeignKey('publishers.publisher_id'))

    author = relationship("Authors")
    publisher = relationship("Publisher")

class Publisher(Base):
    __tablename__ = "publishers"

    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)

class Authors(Base):
    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    full_name = Column(String)

class Inventory(Base):
    __tablename__ = "inventory"

    book_id = Column(Integer, primary_key=True)
    stocklevel_used = Column(Integer)
    stocklevel_new = Column(Integer)

class OrderItem(Base):
    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)

class Orders(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(DATE)
    subtotal = Column(Float)
    shipping = Column(Float)
    total = Column(Float)

    customer = relationship("Customers")

Base.metadata.create_all(engine)




Session = sessionmaker(bind=engine)
session = Session()

# Read CSV data and populate the database for each table
def populate_table_from_csv(model, csv_file):
    df = pd.read_csv(csv_file)
    records = df.to_dict(orient='records')
    session.bulk_insert_mappings(model, records)
    session.commit()

csv_files = {
    Customers: '../../../data/customers.csv',
    Books: '../../../data/books.csv',
    Publisher: '../../../data/publishers.csv',
    Authors: '../../../data/authors.csv',
    Inventory: '../../../data/inventory.csv',
    OrderItem: '../../../data/orderitem.csv',
    Orders: '../../../data/orders.csv',
}

for model, csv_file in csv_files.items():
    populate_table_from_csv(model, csv_file)

# Close the session when done
session.close()


