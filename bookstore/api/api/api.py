import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

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

@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = books_data[books_data["book_id"] == book_id]
    if book.empty:
        raise HTTPException(status_code=404, detail="Book not found")
    return book.to_dict(orient="records")[0]

@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    book_index = books_data.index[books_data["book_id"] == book_id]
    if book_index.empty:
        raise HTTPException(status_code=404, detail="Book not found")

    book_data = books_data.loc[book_index]
    for field, value in book.dict(exclude_unset=True).items():
        if field != "book_id" and value is not None:
            book_data[field] = value

    books_data.loc[book_index] = book_data
    books_data.to_csv("api/data/books.csv", index=False)
    return {"book_id": book_id, **book_data.to_dict(orient="records")[0]}


@app.post("/books/", response_model=Book)
def create_book(book: Book):
    new_book_id = books_data["book_id"].max() + 1
    book_dict = book.dict()
    book_dict["book_id"] = new_book_id
    books_data = books_data.append(book_dict, ignore_index=True)
    books_data.to_csv("api/data/books.csv", index=False)
    return book
