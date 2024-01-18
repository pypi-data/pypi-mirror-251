import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage

def clustering(topic_probabilities:list, num_topics:int, labels:list=None):
    '''
    文書のクラスタリングを行う関数

    args:
        topic_probabilities: 文書ごとのTopicの所属確率を格納したリスト
        num_topics: Topicの数

    return:
        dendro: 階層構造を格納した辞書
    '''

    # 文書ごとのTopicの所属確率を行列に変換
    topic_matrix = np.zeros((len(topic_probabilities), num_topics))
    for i, doc in enumerate(topic_probabilities):
        for topic, prob in doc:
            topic_matrix[i, topic] = prob

    # 階層クラスタリングを実行
    Z = linkage(topic_matrix, 'ward')

    # 階層構造を取得
    dendro = dendrogram(Z, no_plot=True, labels=labels)

    return dendro
