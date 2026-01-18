import streamlit as st
import Recommendation_System as rs
import time

st.set_page_config(page_title = 'Recommendation System' , page_icon='🎬')

@st.cache_data(show_spinner=False)
def get_poster(movieId):
    url = rs.fetch_image(movieId)
    # Do not cache placeholders
    if "via.placeholder.com" in url:
        st.write('FAILED')
        return None
    return url

st.write('# Recommendation System')

if 'movie_name' not in st.session_state:
    st.session_state.movie_name = ''

if 'movie_Id' not in st.session_state:
    st.session_state.movie_Id = 0

if 'movie_list' not in st.session_state:
    st.session_state.movie_list = list()

if 'movie_sim' not in st.session_state:
    st.session_state.movie_sim = list()

if 'movie_sim_id' not in st.session_state:
    st.session_state.movie_sim_id = list()


st.session_state.movie_list = rs.movie_name()
st.session_state.movie_name = st.selectbox('Search:',options=st.session_state.movie_list)

if st.button(label='Recommend'):
    st.session_state.movie_Id = rs.get_id(st.session_state.movie_name)

    st.session_state.movie_sim, st.session_state.movie_sim_id = rs.get_similer_movies(st.session_state.movie_Id)
    col1,col2,col3,col4,col5 = st.columns(5)
    col = [col1,col2,col3,col4,col5]
    for i in range(5):
        with col[i]:
            url = get_poster(st.session_state.movie_sim_id[i])
            if url is None:
                url = "https://via.placeholder.com/300x450?text=No+Image"
            st.image(url)
            st.write(st.session_state.movie_sim[i])
            time.sleep(.2)



    