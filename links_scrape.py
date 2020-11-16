#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 10:16:10 2020

@author: mason
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pickle


def get_links(page_list):
    '''
    A function that retreves links for specific forum discussion pages on
    Wall Street Oasis

    Parameters
    ----------
    page_list : list of integers
        pages of forums that you wish to pull discussions from.

    Returns
    -------
    links : list of strings
        list of links to specific forum discussions on Wall Street Oasis.

    '''
    
    links = [] # list to store links in
    base_url = 'https://www.wallstreetoasis.com/tracker/nocompany?page='
    
    for page in page_list:
        try:
            response = requests.get(base_url+str(page))
            page = response.text
            soup = BeautifulSoup(page)
            
            # iterate through each forum post on the page and retrieve that post's link
            for forum in soup.find('tbody').find_all(class_ = 'views-field views-field-title-with-tooltip'):
                links.append(forum.find('a').get('href'))
        except:
            None
    return links

page_list = list(np.arange(0, 1503, 3)) # retrieving every 3rd page from 0 to 1500 (500 pages)
links_list = get_links(page_list)

links_list = list(set(links_list)) # getting rid of duplicates


with open('wso_links.pickle', 'wb') as to_write:
    pickle.dump(links_list, to_write)
