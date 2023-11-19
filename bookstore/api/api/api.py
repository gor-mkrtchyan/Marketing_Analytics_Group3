# #Connecting to DB
#
# import pandas as pd
# from fastapi import FastAPI, HTTPException, Depends
# from pydantic import BaseModel
# from typing import Optional
# import sqlite3
#
# app = FastAPI()
#
# # Define the path to the SQLite database
# db_path = "bookstore/db/etl/data_preperation/BookStore.db"
#
#
# # Create a context manager for connecting to the database
# def get_db():
#     db = sqlite3.connect(db_path)
#     yield db
#     db.close()
#
#
# class Book(BaseModel):
#     title: Optional[str] = None
#     price: Optional[float] = None
#     isbn: Optional[str] = None
#     publication_year: Optional[int] = None
#     language: Optional[str] = None
#     cover_type: Optional[str] = None
#     pages_number: Optional[int] = None
#     book_id: int
#
#
# @app.get("/")
# def read_root():
#     return {"message": "BookStore API"}
#
#
# @app.get("/books/")
# def get_books(db: sqlite3.Connection = Depends(get_db)):
#     # Fetch data from the database instead of the CSV file
#     query = "SELECT * FROM books"
#     books_data = pd.read_sql_query(query, db)
#     return books_data.to_dict(orient="records")
#
#
# @app.get("/books/{title}")
# def get_book(title: str, db: sqlite3.Connection = Depends(get_db)):
#     # Fetch data from the database instead of the CSV file
#     query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
#     matching_books = pd.read_sql_query(query, db)
#
#     if matching_books.empty:
#         raise HTTPException(status_code=404, detail="Book not found")
#
#     return matching_books.to_dict(orient="records")
#
#
#
# @app.put("/books/{title}")
# def update_book(title: str, book: Book, db: sqlite3.Connection = Depends(get_db)):
#     # Update data in the database instead of the CSV file
#     query = f"SELECT * FROM books WHERE title LIKE '%{title}%'"
#     matching_books = pd.read_sql_query(query, db)
#
#     if matching_books.empty:
#         raise HTTPException(status_code=404, detail="Book not found")
#
#     for index, row in matching_books.iterrows():
#         for field, value in book.dict(exclude_unset=True).items():
#             if field != "book_id" and value is not None:
#                 row[field] = value
#
#         # Update the row in the database
#         update_query = (
#             "UPDATE books SET " +
#             ", ".join([f'{field} = "{value}"' for field, value in row.items()]) +
#             f" WHERE book_id = {row['book_id']}"
#         )
#         db.execute(update_query)
#
#     return {"title": title, **row.to_dict()}
#
# @app.post("/books/", response_model=Book)
# def create_book(book: Book, db: sqlite3.Connection = Depends(get_db)):
#     # Insert new data into the database instead of the CSV file
#     new_book_id = pd.read_sql_query("SELECT MAX(book_id) FROM books", db).iloc[0, 0] + 1
#     book_dict = book.dict()
#     book_dict["book_id"] = new_book_id
#
#     # Insert the new row into the database
#     insert_query = (
#         f"INSERT INTO books ({', '.join(book_dict.keys())}) "
#         f"VALUES ({', '.join(['?' for _ in book_dict.values()])})"
#     )
#     db.execute(insert_query, list(book_dict.values()))
#
#     return book

# Connecting to CSV
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fuzzywuzzy import fuzz


app = FastAPI()




import os
#Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate to the 'data' folder from the 'api' folder
data_path = os.path.join(script_dir,  'data', 'books.csv')
books_data = pd.read_csv(data_path)

# Load data
#books_data = pd.read_csv("../api/data/books.csv")


class Book(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    language: Optional[str] = None
    cover_type: Optional[str] = None
    pages_number: Optional[int] = None
    book_id: int

@app.get("/")
def read_root():
    return {"message": "BookStore API"}

@app.get("/books/")
def get_books():
    return books_data.to_dict(orient="records")

@app.get("/books/{title}")
def get_book(title: str):
    matching_books = get_matching_books(title)
    if matching_books.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return matching_books.to_dict(orient="records")

@app.put("/books/{title}")
def update_book(title: str, book: Book):
    matching_books_index = get_matching_books(title).index
    if matching_books_index.empty:
        raise HTTPException(status_code=404, detail="Book not found")

    for index in matching_books_index:
        book_data = books_data.loc[index]
        for field, value in book.dict(exclude_unset=True).items():
            if field != "book_id" and value is not None:
                book_data[field] = value

        books_data.loc[index] = book_data

    books_data.to_csv("api/data/books.csv", index=False)
    return {"title": title, **book_data.to_dict(orient="records")[0]}

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    new_book_id = books_data["book_id"].max() + 1
    book_dict = book.dict()
    book_dict["book_id"] = new_book_id
    books_data = books_data.append(book_dict, ignore_index=True)
    books_data.to_csv("api/data/books.csv", index=False)
    return book

def get_matching_books(title: str):
    threshold = 80  # You can adjust this threshold based on your needs
    return books_data[books_data["title"].apply(lambda x: fuzz.token_sort_ratio(title, x)) > threshold]

