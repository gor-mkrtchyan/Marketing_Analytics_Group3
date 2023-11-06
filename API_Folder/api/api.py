import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Load data
books_data = pd.read_csv("api/data/books.csv")
customers_data = pd.read_csv("api/data/customers.csv")

@app.get("/")
def read_root():
    return {"message": "BookStore API"}

@app.get("/books/")
def get_books():
    return books_data.to_dict(orient="records")

@app.get("/customers/")
def get_customers():
    return customers_data.to_dict(orient="records")

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = books_data[books_data["book_id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict(orient="records")[0]

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    customer = customers_data[customers_data["customer_id"] == customer_id]
    if customer.empty:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.to_dict(orient="records")[0]

@app.post("/books/")
def create_book(book: dict):
    books_data = books_data.append(book, ignore_index=True)
    books_data.to_csv("api/data/books.csv", index=False)
    return book

@app.post("/customers/")
def create_customer(customer: dict):
    customers_data = customers_data.append(customer, ignore_index=True)
    customers_data.to_csv("api/data/customers.csv", index=False)
    return customer

@app.put("/books/{book_id}")
def update_book(book_id: int, book: dict):
    book_index = books_data.index[books_data["book_id"] == book_id]
    if book_index.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    books_data.loc[book_index] = book
    books_data.to_csv("api/data/books.csv", index=False)
    return book

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, customer: dict):
    customer_index = customers_data.index[customers_data["customer_id"] == customer_id]
    if customer_index.empty:
        raise HTTPException(status_code=404, detail="Customer not found")
    customers_data.loc[customer_index] = customer
    customers_data.to_csv("api/data/customers.csv", index=False)
    return customer
