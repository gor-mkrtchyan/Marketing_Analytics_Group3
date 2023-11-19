import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.decomposition import TruncatedSVD

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
    idx = books_data.loc[books_data['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 similar books
    book_indices = [i[0] for i in sim_scores]
    recommended_books = books_data.iloc[book_indices].copy()  # Create a copy to avoid modifying the original DataFrame
    return recommended_books

# Get user input for the book title
title_to_recommend = input("Enter a book title: ")
recommendations = get_recommendations(title_to_recommend, books)
recommendations

