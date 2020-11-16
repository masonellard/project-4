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

def comments_dict_list(links):
    '''
    Parameters
    ----------
    links : list of strings
        A list of specific links (without base url) to forum discussion pages on Wall
        Street Oasis.

    Returns
    -------
    comment_data : list of dictionaries
        A list of dictionaries each holding the link, comment, upvotes, downvotes, and 
        original post date for a specific comment under a forum discussion on Wall 
        Street Oasis.
        
    '''
    
    comment_data = [] # list to store dictionaries in
    base_url = 'https://www.wallstreetoasis.com'
    headers = ['link', 'comment', 'upvotes', 'downvotes', 'date']
    count = 0
    for link in tqdm(links):
        count += 1
        if count % 100 == 0: # pickle the data we scraped so far for every 100 links
            with open('wso_comment_data.pickle', 'wb') as to_write:
                pickle.dump(comment_data, to_write)
        try:
            response = requests.get(base_url + link)
            page = response.text
            soup = BeautifulSoup(page)
            
            comment = ''
            upvotes = 0
            downvotes = 0
            # iterate through each comment on the page and extract the text
            for comments in soup.find_all(class_='comment-content'):
                try:
                    comment = comments.find(class_='field-name-comment-body').text
                    for votes in comments.find_all(class_='badge'): # checking for values for upvotes and downvotes
                        if 'badge-success' in votes['class']:
                            upvotes = votes.text
                        else:
                            downvotes = votes.text  
                except:
                    None
                
                # creating a dictionary for each comment and appending them to the list
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
