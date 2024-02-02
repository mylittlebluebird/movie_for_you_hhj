import pandas as pd
import pickle
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
from konlpy.tag import Okt


def getRecommendation(consine_sim):
    simScore = list(enumerate(consine_sim[-1]))
    simScore = sorted(simScore, key=lambda x : x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recmovieList = df_reviews.iloc[movieIdx, 0]
    return recmovieList[1:11]

df_reviews = pd.read_csv('./cleaned_reviews_sum.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()

with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

print(df_reviews.iloc[11, 0])
print(df_reviews.iloc[11, 1])
cosine_sim = linear_kernel(Tfidf_matrix[0], Tfidf_matrix)
print(cosine_sim[0])
print(len(cosine_sim))
recommendation = getRecommendation(cosine_sim)
print(recommendation)



