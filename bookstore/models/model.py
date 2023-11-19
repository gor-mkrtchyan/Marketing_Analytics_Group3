import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD
import sqlite3

# Assuming you have already loaded the 'books' DataFrame
books = pd.read_csv('../../data/books.csv')
books['content'] = books['title'] + ' ' + books['author_id'].astype(str) + ' ' + books['genre']

# TF-IDF Vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(books['content'])

# Include the 'rating' as a numerical feature
rating_matrix = books['rating'].values.reshape(-1, 1)

combined_matrix = pd.concat([pd.DataFrame(tfidf_matrix.toarray()), pd.DataFrame(rating_matrix)], axis=1)

svd = TruncatedSVD(n_components=100)  # Adjust the number of components as needed
tfidf_matrix_reduced = svd.fit_transform(tfidf_matrix)

# Compute cosine similarity
cosine_sim = linear_kernel(tfidf_matrix_reduced, tfidf_matrix_reduced)

def get_recommendations(title, books_data):
    matching_books = books_data.loc[books_data['title'] == title]

    if matching_books.empty:
        print(f"No books found with title: {title}")
        return pd.DataFrame()  # Return an empty DataFrame

    idx = matching_books.index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Check if there are similar books to recommend
    if len(sim_scores) < 2:
        print(f"No similar books found for: {title}")
        return pd.DataFrame()  # Return an empty DataFrame

    sim_scores = sim_scores[1:6]  # Get top 5 similar books
    book_indices = [i[0] for i in sim_scores]
    recommended_books = books_data.iloc[book_indices].copy()

    # Create a DataFrame to store the results
    result_df = pd.DataFrame({'input_book_title': [title] * len(recommended_books),
                              'recommended_book_title': recommended_books['title'].tolist(),
                              'author_id': recommended_books['author_id'].tolist(),
                              'genre': recommended_books['genre'].tolist(),
                              'price': recommended_books['price'].tolist(),
                              'rating': recommended_books['rating'].tolist(),
                              'similarity_score': [i[1] for i in sim_scores]})

    return result_df


# Get user input for the book title
title_to_recommend = input("Enter a book title: ")
recommendations = get_recommendations(title_to_recommend, books)

# Define the SQLite database file path
db_path = 'BookStoreRec.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Check if the Recommendations table already exists
check_table_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='recommendations';"
cursor.execute(check_table_query)
table_exists = cursor.fetchone()

# Create the Recommendations table if it doesn't exist
if not table_exists:
    create_table_query = '''
    CREATE TABLE recommendations (
        input_book_title TEXT,
        recommended_book_title TEXT,
        author_id INTEGER,
        genre TEXT,
        price REAL,
        rating REAL,
        similarity_score REAL
    )
    '''
    try:
        cursor.execute(create_table_query)
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f"Error creating table: {e}")

# Save recommendations to the database
try:
    recommendations.to_sql('recommendations', conn, if_exists='append', index=False)
    print("Recommendations saved to the database.")
except Exception as e:
    print(f"Error saving recommendations to the database: {e}")

# Close the database connection
conn.close()
