import gdown
import streamlit as st

import pickle
import pandas as pd
import requests
  # Move this import to the top

# Function to download files from Google Drive
def download_files():
    # Movie dictionary file
    url_moviedict = 'https://github.com/saranshTISS/movie-recommender-app/releases/download/v1.0.0/movie_dict.pkl'
    output_moviedict = 'movie_dict.pkl'
    gdown.download(url_moviedict, output_moviedict, quiet=False)

    # Similarity file
    url_similarity = 'https://github.com/saranshTISS/movie-recommender-app/releases/download/v1.0.0/similarity.pkl'
    output_similarity = 'similarity.pkl'
    gdown.download(url_similarity, output_similarity, quiet=False)

# Call the download function to fetch files from Google Drive
download_files()

# Fetch poster from TMDB using movie_id
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Recommend movies and their posters
def recommend(movie):
    try:
        # Find the index of the selected movie
        movie_index = movies[movies['title'].str.lower() == movie.lower()].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_posters = []

        # Append recommended movie titles and fetch posters
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id  # Assuming 'movie_id' column exists in movies DataFrame
            recommended_movies.append(movies.iloc[i[0]]['title'])
            recommended_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_posters  # Return list of recommended movies and their posters
    except IndexError:
        st.write(f"Movie '{movie}' not found in the dataset.")
        return [], []

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

# Get user input for movie selection
option = st.selectbox('Type your movie name', movies['title'].values)

if st.button('Recommend'):
    # Call the recommend function with the selected movie name
    recommendations, posters = recommend(option)

    # Display recommended movie titles and posters
    if recommendations:
        col1, col2, col3, col4, col5 = st.columns(5)
        columns = [col1, col2, col3, col4, col5]
        for col, title, poster in zip(columns, recommendations, posters):
            with col:
                st.text(title)
                st.image(poster)
    else:
        st.write("No recommendations found or the movie wasn't in the dataset.")
