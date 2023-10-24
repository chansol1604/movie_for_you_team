# Term Frequency - Inverse Document Frequency
# 많이 나오는 단어의 가중치는 적게, 적게 나오는 단어의 가중치는 크게,
# 따라서 희소한 단어가 같으면 비슷하다고 판단함
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle



df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
df_reviews.info()

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)   #(1935, 46139) = (리뷰의 개수, 모든 리뷰 안의 유니크한 단어의 개수)
                            # 한 문장에서 많이 나오면 큰 값을 주고, 여러 문장에서 많이 나오면 작은 값을 줌

with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)    #mmwrite 매트릭스를 저장하는 함수
# 코사인 유사도: 값이 비슷할 수록 1, 값이 상관없을 수록 0
