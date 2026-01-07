import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown
MOVIE_DICT_FILE = "movie_dict.pkl"
MOVIE_DICT_URL = "https://drive.google.com/file/d/1kfvUr8PtI15YORwlHYUFAWF7WDr-oUne/view?usp=sharing"

if not os.path.exists(MOVIE_DICT_FILE):
    gdown.download(MOVIE_DICT_URL, MOVIE_DICT_FILE, quiet=False)


PKL_FILE = "similarity.pkl"
GDRIVE_URL = "https://drive.google.com/file/d/1ePOkhHZfZj_U2OPn60ZVWuEOK0XhcIKa/view?usp=sharing"

if not os.path.exists(PKL_FILE):
    gdown.download(GDRIVE_URL, PKL_FILE, quiet=False)


API_KEY = "YOUR_NEW_API_KEY"   # ↓ this you must change

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=fe3686aa58c1e3494e8ed6f2c3cbf536&language=en-US"
        data = requests.get(url, timeout=10).json()
        poster_path = data.get("poster_path", None)
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path
        return "https://via.placeholder.com/300x450.png?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450.png?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
