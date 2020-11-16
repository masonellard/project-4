#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:58:15 2020

@author: mason
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import re 
import string
from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD, NMF
from gensim import models, matutils
from corextopic import corextopic as ct

def display_topics(model, feature_names, no_top_words, topic_names=None):
    for ix, topic in enumerate(model.components_):
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '",topic_names[ix],"'")
        print(", ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]]))

# Importing data pickle files

with open('wso_post_data.pickle','rb') as read_file:
    data0 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data1.pickle','rb') as read_file:
    data1 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data2.pickle','rb') as read_file:
    data2 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data21.pickle','rb') as read_file:
    data21 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data.pickle3','rb') as read_file:
    data3 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data4.pickle','rb') as read_file:
    data4 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data41.pickle','rb') as read_file:
    data41 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data5.pickle','rb') as read_file:
    data5 = pickle.load(read_file)

with open('/home/mason/Metis/project-4/wso_post_data51.pickle','rb') as read_file:
    data51 = pickle.load(read_file)
    
# filtering any 'None' values out of data

data0 = list(filter(lambda a: a != None, data0))
data1 = list(filter(lambda a: a != None, data1))
data2 = list(filter(lambda a: a != None, data2))
data21 = list(filter(lambda a: a != None, data21))
data3 = list(filter(lambda a: a != None, data3))
data4 = list(filter(lambda a: a != None, data4))
data41 = list(filter(lambda a: a != None, data41))
data5 = list(filter(lambda a: a != None, data5))
data51 = list(filter(lambda a: a != None, data51))

post_df = pd.DataFrame(data0+data1+data2+data21+data3+data4+data41+data5+data51)

# dropping NaNs
post_df.isna().sum()
post_df.dropna(how='any', inplace=True)

# for many forums, the title is just as important as the post. Lets combine the two..
title_format = lambda x: x.replace('/forums/', '').replace('-', ' ')
post_series = post_df.link.map(title_format) + ' ' + post_df.post

# ridding text data of numbers, capitalized letters, and line breaks
alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
line_breaks = lambda x: x.replace('\n', '')

post_series = post_series.map(alphanumeric).map(punc_lower).map(line_breaks)
post_series.head()

# Lets add some stop words to the existing 'english' list
stop_words = text.ENGLISH_STOP_WORDS.union(['know', 
                                            'don', 
                                            'think', 
                                            'does', 
                                            'hi', 
                                            've', 
                                            'thanks', 
                                            'like', 
                                            'http', 
                                            'https', 
                                            'www', 
                                            'just', 
                                            'deleted', 
                                            'wondering'])

# I'm going to create both a count and tfidf vectorizer and compare results
cv = text.CountVectorizer(stop_words = stop_words, ngram_range=(1, 1))
tfidf = text.TfidfVectorizer(stop_words = stop_words, sublinear_tf=True)

X_cv = cv.fit_transform(post_series)
X_tf = tfidf.fit_transform(post_series)

X_cv.shape
X_tf.shape

# LSA

# Lets start with two topics and see how we do
lsa = TruncatedSVD(2)
topic_cv = lsa.fit_transform(X_cv)
display_topics(lsa, cv.get_feature_names(), 10)
lsa.explained_variance_ratio_ # a list of the explained variance ratio per topic
 
# Now lets increase the number of topics, and see if we can pick an optimal number
# based on the explained variance ratios of additional topics

lsa = TruncatedSVD(20) # increasing number of topics to 20
lsa.fit_transform(X_cv)
plt.plot(lsa.explained_variance_ratio_) # graphing the explained variance ratios
plt.xticks(list(range(len(lsa.explained_variance_ratio_))))
display_topics(lsa, cv.get_feature_names(), 10)

# There appeared to be an 'elbow' around 2-3 topics when graphing the explained variance ratios
lsa = TruncatedSVD(3) # reducing number of topics to 3
topic_cv = lsa.fit_transform(X_cv)
display_topics(lsa, cv.get_feature_names(), 10)
lsa.explained_variance_ratio_

# We'll repeat the same process, but this time with the tfidf vectorizer
# First, lets plot the elbow curve for 20 topics
lsa = TruncatedSVD(20)
topic_tf = lsa.fit_transform(X_tf)
plt.plot(lsa.explained_variance_ratio_)
plt.xticks(list(range(len(lsa.explained_variance_ratio_))))

# This 'elbow' looked much less defined. Lets reduce number of topics to 4
lsa = TruncatedSVD(4)
topic_tf = lsa.fit_transform(X_tf)
display_topics(lsa, tfidf.get_feature_names(), 10)

# NMF

nmf = NMF(2) # Setting initial number of topics to 2

# Comparing results from count vectorizer and tfidf vectorizer
topic_cv = nmf.fit_transform(X_cv)
display_topics(nmf, cv.get_feature_names(), 10)

topic_tf = nmf.fit_transform(X_tf)
display_topics(nmf, tfidf.get_feature_names(), 10)

nmf = NMF(20) # increasing number of topics to 20

# Again, lets compare results between cv and tfidf
nmf.fit_transform(X_cv)
display_topics(nmf, cv.get_feature_names(), 10)

topic_cv = nmf.fit_transform(X_tf)
display_topics(nmf, tfidf.get_feature_names(), 10)

# Looks like we got much more separation with the count
# vectorizer, so we'll pickle that for later

nmf.fit_transform(X_cv) # fitting nmf to the cv for the pickle file
display_topics(nmf, cv.get_feature_names(), 10)

with open('nmf.pickle', 'wb') as to_write:
    pickle.dump(nmf, to_write)

# LDA

corpus = matutils.Sparse2Corpus(X_cv.transpose()) # creating a corpus with the count vectorizer
id2word = dict((v, k) for k, v in cv.vocabulary_.items())

lda = models.LdaModel(corpus=corpus, num_topics=10, id2word=id2word, passes=10)
lda.print_topics()

corpus = matutils.Sparse2Corpus(X_tf.transpose()) # creating a corpus with the tfidf vectorizer
id2word = dict((v, k) for k, v in tfidf.vocabulary_.items()) 

lda = models.LdaModel(corpus=corpus, num_topics=10, id2word=id2word, passes=10)
lda.print_topics()

# Corex

words = list(np.asarray(cv.get_feature_names())) # retrieving list of words in count vectorizer

# Fitting first corex model with 6 topics, no anchors
model = ct.Corex(n_hidden=6, words=words, seed=1)
model.fit(X_cv, words=words)

# displaying topics
topics = model.get_topics()
for n,topic in enumerate(topics):
    topic_words,_ = zip(*topic)
    print('{}: '.format(n) + ','.join(topic_words))

# Fitting corex model with 10 topics, 2 sets of weak anchors
model = ct.Corex(n_hidden=10, words=words, seed=1)
model.fit(X_cv, words=words,
          anchors=[['school', 'target', 'gpa'],
                   ['work', 'life', 'balance']], anchor_strength=2)

# displaying new topics
topics = model.get_topics()
for n,topic in enumerate(topics):
    topic_words,_ = zip(*topic)
    print('{}: '.format(n) + ','.join(topic_words))


# Appears that we got the best results from the 20-topic NMF model
# lets read in the pickle file and prepare some dataframes to do visualizations with

with open('nmf.pickle','rb') as read_file:
    nmf = pickle.load(read_file)

topic_cv = nmf.transform(X_cv)

# Creating a 'topic' column in post_df, and setting it equal to that post's topic with highest probability
post_df['topic'] = 0
for ind, row in enumerate(topic_cv):
    max_prob = 0
    for i, j in enumerate(row):
        if j > max_prob:
            max_prob = j
            topic = i
    post_df.loc[post_df.index[ind],'topic'] = topic
    
post_df.date = pd.to_datetime(post_df.date)

# 9 topics stand out as the best topics from our model for inference purposes. Lets keep them in a list
best_topics = ['0', '2', '5', '6', '7', '8', '9', '11', '16', '17', '18']

# First, lets make a dataframe holding total counts for each topic in 'best_topics' by month 
month_totals = pd.concat([post_df[['date', 'topic']].loc[post_df[post_df.topic == int(topic)].index, ].groupby(post_df.date.dt.month).count().topic for topic in best_topics], axis = 1)
month_totals.columns = best_topics

# Next, we count total number of posts by year
yearly_totals = post_df.groupby([post_df.date.dt.year]).link.count()

# Then, we count total number of posts by year and topic
topic_by_year = post_df.groupby([post_df.date.dt.year, 'topic']).link.count()
topic_year_df = topic_by_year.reset_index(level=1)

# We can use the previous two dataframes to calculate the proportion of posts belonging to each topic, each year
year_proportions = pd.concat([topic_year_df[topic_year_df['topic'] == int(topic)].link / yearly_totals.loc[topic_year_df[topic_year_df['topic'] == int(topic)].index,] for topic in best_topics], axis=1)
year_proportions.columns = best_topics
year_proportions.head()

# Now lets write the appropriate dataframes to csv's so we can use them in our visualizations
year_proportions.to_csv('/home/mason/Metis/project-4/year_prop.csv')
yearly_totals.to_csv('/home/mason/Metis/project-4/year_totals.csv')
month_totals.to_csv('/home/mason/Metis/project-4/monthly_totals.csv')
post_df.to_csv('/home/mason/Metis/project-4/post_df.csv')