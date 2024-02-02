import pandas as pd
import re
from konlpy.tag import Okt

okt = Okt()
cleaned_sentences = []

df = pd.read_csv('./reviews_32mb.csv')
print(df.head())
print(df.info())

df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])

print(stopwords)

for review in df.reviews:
    review = re.sub('[^가-힣]', ' ', review)
    tokened_review = okt.pos(review, stem=True) #pos = 품사 태깅 #morphs = 태깅
    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])
    print(df_token.head())
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Adjective') |
                        (df_token['class'] == 'Verb')]
    words = []
    for word in df_token.word:
        print(word)
        if 1 < len(word):
            if word not in stopwords:
                words.append(word)

    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)

df['reviews'] = cleaned_sentences
df.dropna(inplace=True)
df.to_csv('./cleaned_32mb_reviews.csv', index=False)

df = pd.read_csv('./cleaned_32mb_reviews.csv')
df.dropna(inplace=True)

df.to_csv('./cleaned_32mb_reviews.csv', index=False)

print(df.head())




