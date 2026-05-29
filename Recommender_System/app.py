import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
# redeploy fix

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #0f0f0f,
        #1a1a1a,
        #111111
    );
    color: white;
}

/* Main Title */
h1 {
    text-align: center;
    color: white;
    font-size: 65px;
    font-weight: bold;
    margin-bottom: 35px;

    text-shadow:
        0px 0px 10px rgba(255,0,0,0.7),
        0px 0px 20px rgba(255,0,0,0.5);
}

/* Selectbox Label */
label {
    color: white !important;
    font-size: 20px !important;
    font-weight: 600;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 12px;
    backdrop-filter: blur(10px);
    color: white;
}

/* Recommend Button */
.stButton>button {

    background: linear-gradient(
        to right,
        #ff416c,
        #ff4b2b
    );

    color: white;

    border: none;
    border-radius: 12px;

    padding: 12px 35px;

    font-size: 18px;
    font-weight: bold;

    transition: all 0.3s ease;

    box-shadow: 0px 4px 15px rgba(255,75,75,0.4);
}

/* Button Hover */
.stButton>button:hover {

    transform: translateY(-3px) scale(1.03);

    box-shadow: 0px 8px 25px rgba(255,75,75,0.7);
}

/* Movie Titles */
h3 {

    color: white;

    text-align: center;

    font-size: 24px;

    font-weight: 600;

    margin-top: 15px;

    min-height: 80px;
}

/* Posters */
img {

    border-radius: 18px;

    transition: all 0.3s ease;

    box-shadow:
        0px 5px 18px rgba(0,0,0,0.5);
}

/* Poster Hover */
img:hover {

    transform: scale(1.05);

    box-shadow:
        0px 10px 30px rgba(255,255,255,0.25);
}

/* Remove Streamlit top spacing */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)




def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=3d526c31c1f940104a139a1134d3a806&language=en-US"

    for i in range(5):   # retry 5 times

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            data = response.json()#Converts JSON into Python dictionary.

            # check poster exists
            if 'poster_path' in data and data['poster_path']:#and data['poster_path'] check Does poster_path contain actual value?

                full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']

                return full_path

            else:
                return "https://via.placeholder.com/500x750?text=No+Poster"

        except Exception as e:

            print(e)

            time.sleep(1)

    return "https://via.placeholder.com/500x750?text=No+Poster"
 
             
    
    
def recommend(movie):
    movie_index= movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    movies_list= sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    
    recommended_movies =[]
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        if pd.isna(movie_id):
            continue
        recommended_movies.append(movies.iloc[i[0]].title)
        
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies = pickle.load(open(os.path.join(BASE_DIR, 'movie.pkl'), 'rb'))

similarity = pickle.load(open(os.path.join(BASE_DIR, 'similarity.pkl'), 'rb'))

st.title("Movie Recommender System")

selected_movie_name=st.selectbox(
    'Select A Movie',
    ['Choose a Movie']+ list(movies['title'].values)# Value mean only name
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)#Creates 5 columns.To show movies side-by-side.

    for i in range(5):
        with cols[i]:
            st.markdown(f"<h3>{names[i]}</h3>", unsafe_allow_html=True)#This will show movie name 
            
            st.image(posters[i],width=200)