import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec
from konlpy.tag import Okt



# 유사도를 측정해서 가장 높은 유사도로 정렬하는 함수
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]
    movieIdx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieIdx, 0]
    return recMovieList


df_reviews = pd.read_csv('./crawling_data/cleaned_one_review.csv')
Tfidf_matrix =mmread('./models/Tfidf_movie_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 영화 리뷰 기반 추천
# print(df_reviews.iloc[383, 0])
# cosine_sim = linear_kernel(Tfidf_matrix[87], Tfidf_matrix)
# print(cosine_sim[0])
# print(len(cosine_sim[0]))
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)

# 키워드 기반 추천

# embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
# keyword = '마블'
# try:
#     sim_word = embedding_model.wv.most_similar(keyword, topn=10)
#     print(sim_word)
#     words = [keyword]
#     for word, _ in sim_word:
#         words.append(word)
#     print(words)
#
#     sentence = []
#     count = 10
#     for word in words:
#         sentence = sentence + [word] * count
#         count -= 1
#     sentence = ' '.join(sentence)
#     print(sentence)
#     sentence_vec = Tfidf.transform([sentence])
#     cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
#     recommendation = getRecommendation(cosine_sim)
#     print(recommendation)
# except:
#     print('다른 키워드를 이용하세요.')

okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

sentence = '화려한 액션과 소름 돋는 반전이 있는 영화'
token_sentence = okt.pos(sentence, stem=True)
sentences = []
sentence_processing = []
words = []


for word, _ in token_sentence:
    sentences.append(word)

for sentence in sentences:
    if len(sentence) > 1:
        if sentence not in stopwords:
            sentence_processing.append(sentence)
print(sentence_processing)

for keyword in sentence_processing:
    try:
        sim_word = embedding_model.wv.most_similar(keyword, topn=10)
        for word, _ in sim_word:
            words.append(keyword)
            words.append(word)
    except:
        print('다른 키워드를 이용하세요.')
sentence = []
for word in words:
    sentence = sentence + [word]
sentence = ' '.join(sentence)
print(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)