import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./cleaned_reviews_sum.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['review'])
print(Tfidf_matrix.shape)

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/tfidf_movie_review.mtx', Tfidf_matrix)







