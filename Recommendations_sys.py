import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Create a Dataset
movies = {
    'title': [
        'The Matrix', 'Inception', 'Interstellar', 'The Dark Knight',
        'Fight Club', 'Pulp Fiction', 'Forrest Gump', 'The Shawshank Redemption'
    ],
    'genre': [
        'Action Sci-Fi', 'Action Sci-Fi', 'Sci-Fi Drama', 'Action Crime',
        'Drama', 'Crime Drama', 'Drama Romance', 'Drama'
    ]
}

# Create a DataFrame
df = pd.DataFrame(movies)

# Step 2: Define User Preferences
user_preferences = ['Action', 'Sci-Fi', 'Drama']

# Step 3: Calculate Similarity
# Convert genres to a format suitable for vectorization
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(df['genre'])

# Calculate cosine similarity between all movies
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


# Function to recommend movies
def recommend_movies(user_preferences, df, cosine_sim):
    # Convert user preferences to a string
    user_pref_str = " ".join(user_preferences)
    user_pref_vec = tfidf_vectorizer.transform([user_pref_str])

    # Calculate similarity between user preferences and all movies
    user_sim = cosine_similarity(user_pref_vec, tfidf_matrix)

    # Get indices of movies sorted by similarity score
    similar_movies_idx = user_sim.argsort()[0][::-1]

    # Recommend top 5 movies
    recommended_movies = df.iloc[similar_movies_idx][:5]
    return recommended_movies['title']


# Step 4: Make Recommendations
recommendations = recommend_movies(user_preferences, df, cosine_sim)
print("Recommended Movies:")
for movie in recommendations:
    print(movie)
