# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dmMgJPsghzfrrIq1xobX0-9QZnA4gS1x
"""

# Install required libraries
!pip install scikit-surprise

# Step 1: Import Libraries
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# Step 2: Load MovieLens 100k Data (or you can upload your own)
# Download movies and ratings CSVs if you have them
from urllib.request import urlretrieve

urlretrieve('https://raw.githubusercontent.com/susanli2016/Machine-Learning-with-Python/master/movies.csv', 'movies.csv')
urlretrieve('https://raw.githubusercontent.com/susanli2016/Machine-Learning-with-Python/master/ratings.csv', 'ratings.csv')

movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

print("Movies dataset:")
print(movies.head())
print("\nRatings dataset:")
print(ratings.head())

# Step 3: Prepare Data for Surprise
reader = Reader(rating_scale=(0.5, 5.0))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

# Step 4: Train/Test Split
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Step 5: Build and Train the Model
model = SVD()
model.fit(trainset)

# Step 6: Evaluate the Model
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
print(f"\nModel RMSE: {rmse:.4f}")

# Step 7: Recommend Top 5 Movies for a User
def get_top_n_recommendations(user_id, n=5):
    # Get list of all movie IDs
    all_movie_ids = movies['movieId'].unique()

    # Get movies already rated by user
    rated_movies = ratings[ratings['userId'] == user_id]['movieId'].values

    # Filter out already rated movies
    movies_to_predict = [movie for movie in all_movie_ids if movie not in rated_movies]

    # Predict ratings for all unrated movies
    predictions = [model.predict(user_id, movie_id) for movie_id in movies_to_predict]

    # Sort movies by predicted rating
    predictions.sort(key=lambda x: x.est, reverse=True)

    # Get top N movie IDs
    top_movie_ids = [int(pred.iid) for pred in predictions[:n]]

    # Get movie titles
    recommended_movies = movies[movies['movieId'].isin(top_movie_ids)][['title', 'genres']]

    return recommended_movies

# Example: Recommend movies for user with userId=1
user_id = 1
recommended = get_top_n_recommendations(user_id)
print(f"\nTop 5 movie recommendations for user {user_id}:")
print(recommended)