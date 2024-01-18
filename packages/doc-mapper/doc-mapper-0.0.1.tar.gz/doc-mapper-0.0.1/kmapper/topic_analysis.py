from gensim import corpora, models

def topic_analysis(texts:list):
    '''
    Topic分析を行う関数

    args:
        texts: テキストのリスト

    return:
        topic_list: Topicのリスト
        topic_probabilities: 文書ごとのTopicの所属確率を格納したリスト
    '''

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    hdp = models.HdpModel(corpus, dictionary, random_state=0)
    topic_list = hdp.print_topics(num_words=10)
    topic_probabilities = [hdp[doc] for doc in corpus]

    return topic_list, topic_probabilities
