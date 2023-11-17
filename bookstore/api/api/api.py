import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fuzzywuzzy import fuzz

app = FastAPI()

# Load data
books_data = pd.read_csv("api/data/books.csv")

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
