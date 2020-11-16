#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 19:10:47 2020

@author: mason
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

year_proportions = pd.read_csv('/home/mason/Metis/project-4/year_prop.csv')
yearly_totals = pd.read_csv('/home/mason/Metis/project-4/year_totals.csv')
month_totals = pd.read_csv('/home/mason/Metis/project-4/monthly_totals.csv')
post_df = pd.read_csv('/home/mason/Metis/project-4/post_df.csv')

post_df.date = pd.to_datetime(post_df.date)

# time series plot of total number of posts in each year
sns.set_palette('Blues', 1, .4)
sns.set_style('white')
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(yearly_totals.link, linewidth=10)
ax.set_ylim((0,10000))
ax.set_yticklabels([0, 2000, 4000, 6000, 8000, 10000],Fontsize=18)
ax.set_xticklabels(range(2004, 2022, 2), fontsize=18)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Bar graph showing the total number of posts that fall under each topic in the 'recruitment' category
sns.set_palette('Blues', 1, .9)
sns.set_style('white')
fig, ax = plt.subplots(figsize=(20, 10))
ax.bar(['Interview Prep',
         'Financial Modeling', 
         'Group Comparisons', 
         'Recruiting Threads', 
         'Resumes'],
        month_totals[['2','5', '6', '7', '11']].sum())
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_yticklabels(np.arange(0, 4500, 500),Fontsize=18)
ax.set_xticklabels(['Interview Prep',
         'Financial Modeling', 
         'Group Comparisons', 
         'Recruiting Threads', 
         'Resumes'], fontsize=18)

# density plots for recruitment threads topic in each year from 2016-2020
plt.figure(figsize=(20, 10))
sns.set_palette('Blues')
sns.set_style('ticks')
for year in range(2016, 2021): # iterate through each year and get the number of topic 7 posts for each month that year
    series_7 = post_df[(post_df.date.dt.year == year) & (post_df.topic == 7)].groupby([post_df.date.dt.month, 'topic']).link.count()
    df_7 = series_7.reset_index(level=1)
    counts = []
    for month in df_7.index: # append each month to a list for however many posts were made that month
        for i in range(int(df_7.link.loc[month,])):
            counts.append(month)
    sns.distplot(counts, hist=False, kde_kws=dict(linewidth=10)) # create a density plot for each year
    sns.despine()
    plt.xticks(range(0, 13), fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlim((0, 12))

# time series plot showing the total number of topic 0 posts for each month across the entire observed time period
sns.set_palette('Greens', 1, .9)
sns.set_style('white')
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(month_totals['0'], linewidth=10)
ax.set_yticklabels(np.arange(375, 600, 25),fontsize=18)
ax.set_xticklabels(range(0, 14, 2), fontsize=18)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# time series plot showing the proportion of topic 0 posts to total posts for each year
fig, ax = plt.subplots(figsize=(20, 10))
sns.set_palette('Greens', 1, .9)
sns.set_style('white')
ax.plot(year_proportions['0'], linewidth=10)
ax.set_yticklabels([.04, .06, .08, .10, .12, .14, .16, .18],fontsize=18)
ax.set_xticklabels(range(2004, 2022, 2), fontsize=18)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# time series plots showing the proportion of posts under recruitment category to total posts for each topic in each year
sns.set_palette('Greys', 4, .3)
sns.set_style('white')
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(year_proportions[['2', '5', '6', '11']], linewidth=6)
ax.plot(year_proportions['7'], linewidth=10, color='royalblue')
ax.legend(['Interviews', 'Financial Modeling', 'Group Comps', 'Resumes', 'Recruitment Threads'])
ax.set_yticklabels([0, .02, .04, .06, .08, .10, .12],fontsize=18)
ax.set_xticklabels(range(2004, 2022, 2), fontsize=18)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# time series plots showing the proportion of posts under industries category to total posts for each topic for each year
sns.set_palette('cubehelix', 3, .9)
sns.set_style('white')
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(year_proportions[['8', '9', '17']], linewidth=10)
ax.legend(['Consulting', 'Real Estate', 'Trading'], fontsize=18)
ax.set_yticklabels([0, .01, .02, .03, .04, .05, .06, .07, .08],fontsize=18)
ax.set_xticklabels(range(2004, 2022, 2), fontsize=18)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
