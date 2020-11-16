#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:41:42 2020

@author: mason
"""

from bs4 import BeautifulSoup
import requests
import pickle

# open the list of links to scrape
with open('wso_links.pickle','rb') as read_file:
    links_list = pickle.load(read_file)

def get_posts(soup):
    '''
    Parameters
    ----------
    soup : BeautifulSoup Object
        Forum discussion page from Wall Street Oasis.
        
    Returns
    -------
    post : string
        Original post on forum discussion page.

    '''    
    
    try:
        post = soup.find(class_ = 'post-wrap').find(property='content:encoded').text
        return post
    except:
        None
        

def post_upvotes(soup):
    '''
    Parameters
    ----------
    soup : BeautifulSoup Object
        Forum discussion page from Wall Street Oasis.

    Returns
    -------
    upvotes : integer
        Number of upvotes for original post.

    '''
    
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
    '''
    Parameters
    ----------
    soup : BeautifulSoup Object
        Forum discussion page from Wall Street Oasis.
        
    Returns
    -------
    downvotes : integer
        Number of downvotes for original post.

    '''
    
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
    '''
    Parameters
    ----------
    soup : BeautifulSoup Object
        Forum discussion page from Wall Street Oasis.
        
    Returns
    -------
    date : string
        Date that original post was posted.

    '''
    
    try:
        date = soup.find(class_='created pr-4').text.replace('\n', '')
        return date
    except:
        None
        
    


def post_dict(link):
    '''
    Parameters
    ----------
    link : string
        Specific link (without base url) to forum discussion page on Wall
        Street Oasis.

    Returns
    -------
    op_dict : dictionary
        A dictionary holding the link, post, upvotes, downvotes, and date
        for a specific forum discussion on Wall Street Oasis.

    '''
    
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

post_data = [] # list to append dictionaries to 
count = 0
for link in tqdm(links_list):
    post_data.append(post_dict(link))
    count += 1
    if count % 100 == 0: # we pickle the data we've scraped so far for every 100 links
        with open('wso_post_data.pickle', 'wb') as to_write:
            pickle.dump(post_data, to_write)
    time.sleep(.5+random.random()) # program will sleep for average of 1 second after each page request
