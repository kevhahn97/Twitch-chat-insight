from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json
import codecs
from konlpy.tag import Okt

filename = input("filename: ")
with open(filename+'.json', 'r', encoding='utf-8-sig') as data_file:
    data = json.load(data_file)

nlpy = Okt()
docs = list()
chats = list()

#data = data[0:50000]
for contents in data:
    noun = nlpy.nouns(contents["contents"])
    if len(noun) != 0:
        docs.append(' '.join(noun))
        chats.append(contents["contents"])
print(docs)

tfidf_vectorizer = TfidfVectorizer(min_df=1)
tfidf_matrix = tfidf_vectorizer.fit_transform(docs)

document_distances = np.array((tfidf_matrix * tfidf_matrix.T).toarray())
document_distances -= np.eye(document_distances.shape[0])

# numpy 에서 거리가 th 이상이면 그 가로세로 인덱스를 사전에 넣는다
# 그 사전을 채팅으로 바꿔서 출력한다

clusters = list()

idx_x = np.where(document_distances > 0.7)[0]
idx_y = np.where(document_distances > 0.7)[1]
for idx in range(len(idx_x)):
    x = idx_x[idx]
    y = idx_y[idx]
    if y <= x:
        continue
    cluster_exist = False
    for cluster_idx in range(len(clusters)):
        if x in clusters[cluster_idx]:
            cluster_exist = True
            clusters[cluster_idx].add(y)
            break
    if cluster_exist == False:
        cluster = {x, y}
        clusters.append(cluster)

cluster_lens = list()
for idx in range(len(clusters)):
    cluster_lens.append((len(clusters[idx]), idx))
cluster_lens.sort(reverse=True)

outputfile = codecs.open('output.txt', 'w', encoding='utf-8')
for _, idx in cluster_lens:
    outputfile.write("---------------------------------------\n")
    for chat in clusters[idx]:
        outputfile.write(chats[chat]+'\n')
outputfile.close()
print("")