#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 15:58:15 2020

@author: mason
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import pickle


# Retrieving page links

def get_links(page_list):
    
    links = []
    base_url = 'https://www.wallstreetoasis.com/tracker/nocompany?page='
    
    for page in page_list:
        try:
            response = requests.get(base_url+str(page))
            page = response.text
            soup = BeautifulSoup(page)
            
            for forum in soup.find('tbody').find_all(class_ = 'views-field views-field-title-with-tooltip'):
                links.append(forum.find('a').get('href'))
        except:
            None
    return links

page_list = list(np.arange(0, 1503, 3))
links_list = get_links(page_list)

links_list = list(set(links_list))


with open('wso_links.pickle', 'wb') as to_write:
    pickle.dump(links_list, to_write)
    


# Retrieving OP post

def get_posts(soup):
    
    try:
        post = soup.find(class_ = 'post-wrap').find(property='content:encoded').text
        return post
    except:
        None
        
    


def post_upvotes(soup):
    
    upvotes = 0    
    try:
        for votes in soup.find(class_='post-footer').find_all(class_='badge'):
            if 'badge-success' in votes['class']:
                upvotes = votes.text
            else:
                pass
        return upvotes
    except:
        None
    
    


def post_downvotes(soup):
    
    downvotes = 0    
    try:
        for votes in soup.find(class_='post-footer').find_all(class_='badge'):
            if 'badge-success' not in votes['class']:
                downvotes = votes.text
            else:
                    pass
        return downvotes        
    except:
        None
        
    


def get_date(soup):
    
    try:
        date = soup.find(class_='created pr-4').text.replace('\n', '')
        return date
    except:
        None
        
    


def post_dict(link):
    
    base_url = 'https://www.wallstreetoasis.com'
    response = requests.get(base_url + link)
    page = response.text
    soup = BeautifulSoup(page)
    
    headers = ['link', 'post', 'upvotes', 'downvotes', 'date']
    
    op_dict = dict(zip(headers, [link,
                                get_posts(soup),
                                post_upvotes(soup),
                                post_downvotes(soup), 
                                get_date(soup)]))
    
    return op_dict

import time
import random
from tqdm import tqdm

post_data = []
count = 0
for link in tqdm(links_list[:1000]):
    post_data.append(post_dict(link))
    count += 1
    if count % 100 == 0:
        with open('wso_post_data.pickle', 'wb') as to_write:
            pickle.dump(post_data, to_write)
    time.sleep(.5+random.random())

post_df = pd.DataFrame(post_data)

post_df.isna().sum()

post_df.dropna(how='any', inplace=True)

post_df.head()
# Retrieving comments

def comments_dict_list(links):
    
    comment_data = []
    base_url = 'https://www.wallstreetoasis.com'
    headers = ['link', 'comment', 'upvotes', 'downvotes', 'date']
    count = 0
    for link in links:
        count += 1
        if count % 100 == 0:
            with open('wso_comment_data.pickle', 'wb') as to_write:
                pickle.dump(comment_data, to_write)
        try:
            response = requests.get(base_url + link)
            page = response.text
            soup = BeautifulSoup(page)
            
            comment = ''
            upvotes = 0
            downvotes = 0
            for comments in soup.find_all(class_='comment-content'):
                try:
                    comment = comments.find(class_='field-name-comment-body').text
                    for votes in comments.find_all(class_='badge'):
                        if 'badge-success' in votes['class']:
                            upvotes = votes.text
                        else:
                            downvotes = votes.text  
                except:
                    None
            
                if comment:
                    comment_dict = dict(zip(headers, [link,
                                                      comment,
                                                      upvotes,
                                                      downvotes,
                                                      get_date(soup)]))
                    comment_data.append(comment_dict)
        except:
            None            
    return comment_data



for link in links_list:
    for comment in get_comments(soup):
        comments_dict 
for comments in soup.find_all(class_='comment-content'):
    try:
        print(comments.find(class_='field-name-comment-body').text)
    except:
       None
    try:
        for votes in comments.find_all(class_='badge'):
            if 'badge-success' in votes['class']:
                print('Upvotes:', votes.text)
            else:
                print('Downvotes:', votes.text)        
    except:
        None

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

with open('wso_links.pickle','rb') as read_file:
    links_list = pickle.load(read_file)
    

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

post_df.isna().sum()

post_df.dropna(how='any', inplace=True)

title_format = lambda x: x.replace('/forums/', '').replace('-', ' ')

post_series = post_df.link.map(title_format) + ' ' + post_df.post

import re 
import string

alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())
line_breaks = lambda x: x.replace('\n', '')

post_series = post_series.map(alphanumeric).map(punc_lower)
post_series = post_series.map(line_breaks) 

post_series.head()

from sklearn.feature_extraction import text

stop_words = text.ENGLISH_STOP_WORDS.union(['know', 'don', 'think', 'does', 'hi', 've', 'thanks', 'like', 'http', 'https', 'www', 'just', 'deleted', 'wondering'])

cv = text.CountVectorizer(stop_words = stop_words, ngram_range=(1, 1))
X = cv.fit_transform(post_series).transpose()

from gensim import models, corpora, similarities, matutils

corpus = matutils.Sparse2Corpus(X)

id2word = dict((v, k) for k, v in cv.vocabulary_.items())

lda = models.LdaModel(corpus=corpus, num_topics=7, id2word=id2word, passes=100)

lda.print_topics()

lda.get_topics()

lda.show_topics()

topics = lda.get_document_topics(corpus)

topics[2]
corpus[2]

for i,j in corpus[0]:
    print(id2word[i])

post_df['topic'] = 0
for ind, row in enumerate(topics):
    max_prob = 0
    for i, j in row:
        if j > max_prob:
            max_prob = j
            topic = i
    post_df.loc[post_df.index[ind],'topic'] = topic
    
post_df.date = pd.to_datetime(post_df.date)
    
import matplotlib.pyplot as plt

topic_0 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 0].index, ].groupby(post_df.date.dt.month).count()
topic_1 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 1].index, ].groupby(post_df.date.dt.month).count()
topic_2 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 2].index, ].groupby(post_df.date.dt.month).count()
topic_3 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 3].index, ].groupby(post_df.date.dt.month).count()
topic_4 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 4].index, ].groupby(post_df.date.dt.month).count()
topic_5 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 5].index, ].groupby(post_df.date.dt.month).count()
topic_6 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 6].index, ].groupby(post_df.date.dt.month).count()

plt.plot(topic_0)
plt.plot(topic_1)
plt.plot(topic_2)
plt.plot(topic_3)
plt.plot(topic_4)
plt.plot(topic_5)
plt.plot(topic_6)

topic_0 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 0].index, ].groupby(post_df.date.dt.year).count()
topic_1 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 1].index, ].groupby(post_df.date.dt.year).count()
topic_2 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 2].index, ].groupby(post_df.date.dt.year).count()
topic_3 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 3].index, ].groupby(post_df.date.dt.year).count()
topic_4 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 4].index, ].groupby(post_df.date.dt.year).count()
topic_5 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 5].index, ].groupby(post_df.date.dt.year).count()
topic_6 = post_df[['date', 'topic']].loc[post_df[post_df.topic == 6].index, ].groupby(post_df.date.dt.year).count()

plt.plot(topic_0)
plt.plot(topic_1)
plt.plot(topic_2)
plt.plot(topic_3)
plt.plot(topic_4)
plt.plot(topic_5)
plt.plot(topic_6)




len(corpus)
id2wor
X.shape

lda_corpus = lda[corpus]

lda_docs = [doc for doc in lda_corpus]

lda_docs[:5]

life_posts = post_df.loc[post_df[post_df.topic == 4].index, 'post']

topic_0_posts = post_df.loc[post_df[post_df.topic == 0].index, 'post']

topic_5_posts = post_df.loc[post_df[post_df.topic == 5].index, 'post']
