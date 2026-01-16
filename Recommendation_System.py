#import all the neccesory packages

import pandas as pd
import numpy as np 
import ast
from nltk.stem.porter import PorterStemmer
from sklearn.metrics import pairwise_distances
from sklearn.feature_extraction.text import CountVectorizer

#reading the movies and the credit file
movies = pd.read_csv("D:\\DataSet\\Recomedation System\\archive\\tmdb_5000_movies.csv")
credit = pd.read_csv("D:\\DataSet\\Recomedation System\\archive\\tmdb_5000_credits.csv")

#removing all the unnecesory features form the dataframe
movies = movies[['genres','id','keywords','overview','title']]
credit = credit.drop(['movie_id'],axis=1)

#merging movies and credit dataframe 
movies = movies.merge(credit,how='inner',on='title')

#droping all the na values
movies.dropna(inplace=True)

#Converting the genre feature
def clean_genre(x):
    L = []
    for i in ast.literal_eval(x):
        L.append(i['name'])
    return L
#Converting the cast feature
def clean_cast(x):
    L = []
    counter = 0
    for i in ast.literal_eval(x):
        if counter < 3:
            counter += 1
            L.append(i['name'])
        else:
            break
    return L

#Converting the crew feature
def clean_crew(x):
    for i in ast.literal_eval(x):
        if i['job'] == 'Director':
            return [i['name']]

#Removing space between strings   
def remove_space(temp):
    l = []
    for i in temp:
        l.append(i.replace(' ',''))
    return l

def stem(text):
    l = []
    for i in text:
        l.append(PorterStemmer().stem(i))
    return l

#cleaning
movies['genres'] = movies['genres'].apply(clean_genre)
movies['keywords'] = movies['keywords'].apply(clean_genre)
movies['cast'] = movies['cast'].apply(clean_cast)
movies['crew'] = movies['crew'].apply(clean_crew)
movies['overview'] = movies['overview'].apply(lambda x: x.split())

#droping all the null values
movies.dropna(inplace=True)

#Removing blankspace
movies['cast'] = movies['cast'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)

#Creating the tag feature
movies['Tags'] = movies['overview'] + movies['keywords'] + movies['genres'] + movies['cast'] + movies['crew']

#Storing all the neccesory feature into a new dataframe
new_df = movies[['id','title','Tags']]
new_df['Tags'] = new_df['Tags'].apply(stem)
new_df['Tags'] = new_df['Tags'].apply(lambda x: ' '.join(x))

#Vectorizing the tag
cv = CountVectorizer(max_features = 5000,stop_words='english',lowercase=True)
vector = cv.fit_transform(new_df['Tags']).toarray()
vector = pd.DataFrame(vector,index=movies['id'],columns=cv.get_feature_names_out())

#Calculating Similarity
movies_sim = 1 - pairwise_distances(vector,metric='correlation',n_jobs=-1)
movies_sim_df = pd.DataFrame(movies_sim,index=new_df.index,columns=new_df.index)

#Getting top 5 similar movies
def get_similer_movies(movieid,nTop = 5):
    movieIdx = new_df[new_df.id == movieid].index
    if len(movieIdx) == 0:
        print('movie not found')
        return 
    else:
        movieIdx = movieIdx[0]
    new_df['similarity'] = movies_sim_df.iloc[movieIdx]
    ntop = new_df.sort_values(['similarity'],ascending=False)[0:nTop]
    return ntop['title'].values

#returning all the movies name
def movie_name():
    return new_df.title.unique()

#Return the movieId of a specific movie
def get_id(name):
    index = new_df[new_df.title == name].index[0]
    return new_df.id.iloc[index]

