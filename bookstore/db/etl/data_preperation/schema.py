"""
schema.py

This module defines the database schema using SQLAlchemy and populates the tables with data from CSV files.

Author: Group 3
Date: November 17, 2023
"""

import os
import pandas as pd
import logging
from bookstore.db.etl.logger.logger import CustomFormatter
from sqlalchemy import create_engine, Column, Integer, String, Float, DATE, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the SQLAlchemy engine
engine = create_engine('sqlite:///BookStore.db')

# Create a base class for declarative models
Base = declarative_base()

# Define the Customers table
class Customers(Base):
    """Represents the 'customers' table in the database."""

    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    street_address = Column(String)
    state = Column(String)
    city = Column(String)
    zip_code = Column(String)

# Define the Books table
class Books(Base):
    """Represents the 'books' table in the database."""

    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    isbn = Column(String)
    publication_year = Column(Integer)
    language = Column(String)
    cover_type = Column(String)
    pages_number = Column(Integer)
    genre = Column(String)  # New column
    rating = Column(Float)   # New column
    author_id = Column(Integer, ForeignKey('authors.author_id'))
    publisher_id = Column(Integer, ForeignKey('publishers.publisher_id'))

    author = relationship("Authors")
    publisher = relationship("Publisher")

# Define the Publisher table
class Publisher(Base):
    """Represents the 'publishers' table in the database."""

    __tablename__ = "publishers"

    publisher_id = Column(Integer, primary_key=True)
    name = Column(String)

# Define the Authors table
class Authors(Base):
    """Represents the 'authors' table in the database."""

    __tablename__ = "authors"

    author_id = Column(Integer, primary_key=True)
    full_name = Column(String)

# Define the Inventory table
class Inventory(Base):
    """Represents the 'inventory' table in the database."""

    __tablename__ = "inventory"

    book_id = Column(Integer, primary_key=True)
    stocklevel_used = Column(Integer)
    stocklevel_new = Column(Integer)

# Define the OrderItem table
class OrderItem(Base):
    """Represents the 'order_items' table in the database."""

    __tablename__ = "order_items"

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.book_id'), primary_key=True)
    quantity = Column(Integer)
    price = Column(Float)

# Define the Orders table
class Orders(Base):
    """Represents the 'orders' table in the database."""

    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(String)
    subtotal = Column(Float)
    shipping = Column(Float)
    total = Column(Float)

    customer = relationship("Customers")

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Read CSV data and populate the database for each table
def populate_table_from_csv(model, csv_file):
    """Populates a table in the database with data from a CSV file.

    :param model: The SQLAlchemy model representing the table.
    :type model: class
    :param csv_file: Path to the CSV file containing data.
    :type csv_file: str
    :returns: None

    """

    df = pd.read_csv(csv_file)
    records = df.to_dict(orient='records')
    session.bulk_insert_mappings(model, records)
    session.commit()

# Define CSV files for each table
csv_files = {
    Customers: '../../../../data/customers.csv',
    Books: '../../../../data/books.csv',
    Publisher: '../../../../data/publishers.csv',
    Authors: '../../../../data/authors.csv',
    Inventory: '../../../../data/inventory.csv',
    OrderItem: '../../../../data/orderitem.csv',
    Orders: '../../../../data/orders.csv',
}

# Populate tables with data from CSV files
for model, csv_file in csv_files.items():
    populate_table_from_csv(model, csv_file)

# Close the session when done
session.close()
