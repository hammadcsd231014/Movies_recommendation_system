import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
    # Aapki nayi API key yahan daal di hai
    API_KEY = "f12e52ac08613af7386386940735d164" 
    
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}')
        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500" + data['poster_path']
        else:
            # Agar poster nahi hai, toh default image
            return "https://via.placeholder.com/500x750.png?text=Poster+Not+Available"
    except Exception as e:
        # Agar network error ho
        return "https://via.placeholder.com/500x750.png?text=Error+Fetching+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        # Yeh .id wala error bhi theek hai
        movie_id = movies.iloc[i[0]].id 
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# --- File Loading ---
try:
    # Yeh file name 'movies_dict.pkl' bhi theek hai
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    
except FileNotFoundError:
    st.error("Error: 'movies_dict.pkl' ya 'similarity.pkl' file nahi mili.")
    st.info("Yaqeen karein ke yeh files aapki 'app.py' ke saath ek hi folder mein hain.")
    st.stop()
except Exception as e:
    st.error(f"File load karne mein error: {e}")
    st.stop()

# --- Streamlit UI ---
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    try:
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
            
    except IndexError:
        st.error("Error: Yeh movie aapke dataset mein nahi mili.")
    except Exception as e:
        st.error(f"Recommendation mein koi masla hua hai: {e}")