import pandas as pd
import numpy as np 

from sklearn.metrics import pairwise_distances

movies = pd.read_csv("D:\\DataSet\\Recomedation System\\ml-latest-small\\ml-latest-small\\movies.csv")
rating = pd.read_csv("D:\\DataSet\\Recomedation System\\ml-latest-small\\ml-latest-small\\ratings.csv")

rating.drop(['timestamp'],axis=1,inplace=True)

movies = movies.merge(rating.groupby('movieId').mean()[['rating']],on='movieId',how='inner')

movies_user = rating.pivot(index='movieId',columns='userId',values='rating').reset_index(drop=True)
movies_user.fillna(value=0,inplace=True)

movies_sim = 1 - pairwise_distances(movies_user,metric='correlation',n_jobs=-1)
movies_sim_df = pd.DataFrame(movies_sim)
movies_sim_df.index = movies_user.index
movies_sim_df.columns = movies_user.index

def get_similer_movies(movieid,nTop = 5):
    movieIdx = movies[movies.movieId == movieid].index
    if len(movieIdx) == 0:
        print('movie not found')
        return 
    else:
        movieIdx = movieIdx[0]
    movies['similarity'] = movies_sim_df.iloc[movieIdx]
    ntop = movies.sort_values(['similarity'],ascending=False)[0:nTop]
    return ntop['title'].values , ntop['rating'].values , ntop['genres'].values ,ntop['Year'].values

def low(x):
    return x.lower()

#movies['title'] = movies['title'].apply(low)

def check(x):
    title = movies[['title']]
    n = title.size
    for i in range(n):
        movie_name = title.iloc[i].values[0]
        movie_name = movie_name.lower()
        x = x.lower()
        if x in movie_name:
            movie_id = movies['movieId'].iloc[i]
            return True,movie_id
    return False,0

def name(x):
    name = x.split(' ')
    year = name[-1]
    name.pop()
    return ' '.join(name)

def get_year(x):
    return x.split(' ')[-1]

year = []
for i in range(movies['title'].size):
    year.append(get_year(movies['title'].iloc[i]))

movies['Year'] = pd.DataFrame(year)

movies['title'] = movies['title'].apply(name)

