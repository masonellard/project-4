#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 23:04:45 2020

@author: mason
"""
from bs4 import BeautifulSoup
import requests
import pickle
from tqdm import tqdm

def get_date(soup):
    
    try:
        date = soup.find(class_='created pr-4').text.replace('\n', '')
        return date
    except:
        None

def comments_dict_list(links):
    
    comment_data = []
    base_url = 'https://www.wallstreetoasis.com'
    headers = ['link', 'comment', 'upvotes', 'downvotes', 'date']
    count = 0
    for link in tqdm(links):
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

with open('wso_links.pickle','rb') as read_file:
    links_list = pickle.load(read_file)
    
comment_list = comments_dict_list(links_list)

with open('wso_comment_data.pickle', 'wb') as to_write:
                pickle.dump(comment_list, to_write)
