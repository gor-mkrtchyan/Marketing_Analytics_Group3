#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.cluster import KMeans


# In[2]:


os.getcwd()


# In[3]:


df= pd.read_csv('bookss.csv')
df.head()


# As we can see below our data has null values, so we should try to deal it somehow.We'll use 2 different imputers for categorical and numerical features.

# In[4]:


df.isnull().sum()


# In[5]:


numerical_imputer = SimpleImputer(strategy='mean')
categorical_imputer = SimpleImputer(strategy='most_frequent')


# In[6]:


numerical_features = ['price', 'pages_number', 'rating']
categorical_features = ['language', 'cover_type', 'genre']

user_book_features = {
    'price': 5000,
    'pages_number': 500,
    'rating': 5,
    'language': 'Armenian',
    'cover_type': 'Hardcover',
    'genre': 'Romance'
}


# # Option 1 | using cosine similarity

# The preprocessing stage follows where we impute the NAN values and scale the data.

# In[7]:


user_features_df = pd.DataFrame([user_book_features])
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([
            ('imputer', numerical_imputer),
            ('scaler', StandardScaler())
        ]), numerical_features),
        ('cat', Pipeline([
            ('imputer', categorical_imputer),
            ('encoder', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_features)
    ]
)

preprocessor.fit(df)

user_vector = preprocessor.transform(user_features_df)
book_vectors = preprocessor.transform(df)

similarity_scores = cosine_similarity(user_vector, book_vectors)

top_indices = similarity_scores.argsort()[0][-5:]


# In[8]:


recommended_titles = df.loc[top_indices]['title']

print(recommended_titles)


# 

# # Option 2| using K-MEANS and SVM

# In[9]:


number_of_clusters = 5
X = preprocessor.fit_transform(df)
kmeans = KMeans(n_clusters= number_of_clusters, random_state=42)
df['cluster_column'] = kmeans.fit_predict(X)

svm_model = SVC(kernel='linear', decision_function_shape='ovr', class_weight='balanced')
svm_model.fit(X, df['cluster_column'])

user_features_df = pd.DataFrame([user_book_features])
user_vector = preprocessor.transform(user_features_df)
user_cluster = svm_model.predict(user_vector)

cluster_books_df = df[df['cluster_column'] == user_cluster[0]]

cluster_books_vectors = preprocessor.transform(cluster_books_df)
similarity_scores = cosine_similarity(user_vector, cluster_books_vectors)

top_indices = similarity_scores.argsort()[0][-5:][::-1]

recommended_titles = cluster_books_df.iloc[top_indices]['title']

print(recommended_titles)


# In[ ]:




