# Analyzing Finance Culture Through Online Communities Using NLP

I scraped 50,000 forum discussion posts from the popular finance job forum: Wall Street Oasis. I performed topic modeling using LSA, NMF, LDA, and CoRex to analyze overall professional and cultural trends in 'high finance'. 

## File Descriptions

### [links_scrape.py](https://github.com/masonellard/project-4/blob/main/links_scrape.py)
A python file that scrapes the 50,000 links to the pages that I scraped the discussion posts from. Stores the links in a pickled python list (links_list.pickle).

### [gcp_post_scrape.py](https://github.com/masonellard/project-4/blob/main/gcp_post_scrape.py)
A python file that scrapes the original post, date, upvotes, and downvotes from the discussion pages. Takes in the list of links from link_scrape.py, and pickles a list of dictionaries containing the aforementioned data. Multiple data files can be seen in [data](https://github.com/masonellard/project-4/blob/main/data) because I ran gcp_post_scrape.py on multiple GCP instances simultaneously.

### [gcp_comment_scrape.py](https://github.com/masonellard/project-4/blob/main/gcp_comment_scrape.py)
A python file that scrapes the comments , original post date, upvotes, and downvotes from the discussion pages. Takes in the list of links from links_scrape.py, and pickles a list of dictionaries containing the aforementioned data. Similar to gcp_post_scrape.py, multiple data files can be seen in [data](https://github.com/masonellard/project-4/blob/main/data) because I ran gcp_comment_scrape.py on multiple GCP instances simultaneously. 

### [WSO.py](https://github.com/masonellard/project-4/blob/main/WSO.py)
A python file that reads in all of the scraped post data, cleans the text data, performs topic modeling, and outputs multiple .csv files to use for visualizations.

### [wso-visualizations.py](https://github.com/masonellard/project-4/blob/main/wso-visualizations.py)
A python file that reads in the .csv files output by WSO.py, and creates data visualizations.

## Results
