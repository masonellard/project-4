#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:41:42 2020

@author: mason
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import pickle

with open('wso_links.pickle','rb') as read_file:
    links_list = pickle.load(read_file)

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
    try:
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
    except:
        return None
        
import time
import random
from tqdm import tqdm

post_data = []
count = 0
for link in tqdm(links_list[9500:16000]):
    post_data.append(post_dict(link))
    count += 1
    if count % 100 == 0:
        with open('wso_post_data21.pickle', 'wb') as to_write:
            pickle.dump(post_data, to_write)
    time.sleep(.5+random.random())
