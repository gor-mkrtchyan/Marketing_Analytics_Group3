# Book Recommendation System

## Problem Statement

This project aims to develop a sophisticated book recommendation system for Armenian book sellers, Bookinist and Zangak. Current challenges include the absence of recommendation systems, leading to reduced customer engagement and a competitive disadvantage. Valuable customer data is underutilized.

### Objectives

1. **Recommendation System Development:**
   - Data gathering and analysis.
   - Characterizing books using various features.
   - Dashboard and API development.

2. **Goals:**
   - Marketing integration for promotions.
   - Customer feedback integration for continuous improvement.

## Database

The project includes a `BookStore` database with 7 tables of CSV files. The main, `books.csv`, was scrapped from Zangak Store's webpage, it includes around 20,000 books' information. The rest of the tables are generated. You can find scraping and generating scripts in the `ipynb` folder.

## API Interface

FastAPI is used for an intuitive interface allowing customers and bookstore owners to request books, adjust data, or add new books.

## Models

### Matrix Factorization Model (model.py)

The `model.py` file implements a recommendation system using matrix factorization. It recommends the best 5 books based on genre and rating.

#### Usage:

1. **Run the Matrix Factorization Model:**
   - Execute the `model.py` script to generate book recommendations.
  
2. **Database Interaction:**
   - The script stores the recommendations in a new table called `recommendations` inside the `BookStoreRec` database.

## Getting Started

1. **Clone Repository:**

git clone https://github.com/GorMkrtchyan7/Marketing_Analytics_Group3.git



2. **Install Dependencies:**

pip install -r requirements.txt


3. **Database Setup:**
- Import CSV files into the `BookStore` database.

4. **Run FastAPI Server:**
- Make sure you are in the directory `bookstore/api`.
- Run the following script to open the Swagger: `python run.py`.
- After the code is run, check the terminal. You will find (http://127.0.0.1:8000). Press Ctrl and right-click to open it in the browser.
- Next to http://127.0.0.1:8000, add http://127.0.0.1:8000/docs and press enter.
- GET, POST, PUT available for the `books.csv`.
- There is also the commented part of the code connecting BookStore.db inside apy.py. 

