import pandas as pd
from gensim.models import Word2Vec



df_review = pd.read_csv('./crawling_data/cleaned_one_review.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(reviews[0])

tokens = []
for sentence in reviews:
    token = sentence.split()
    tokens.append(token)
print(tokens[0])

#(tokens, 차원의 수, 끊어서 볼 숫자, 최소 나와야 하는 크기(20번 반복해서 나온 단어만), 사용할 프로세서 개수, 학습 횟수, 알고리즘)
# 끊어서 볼 숫자 ex> {사극, 갖추다, 뻔하다, 흐름} , {갖추다, 뻔하다, 흐름, 배우}. 데이터가 많아야 큰 값을 지정할 수 있음
embedding_model = Word2Vec(tokens, vector_size=100, window=4, min_count=10,
                           workers=10, epochs=100, sg=1)
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))