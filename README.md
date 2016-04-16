# IRDM-Semantic-Analysis

This repository is for the 2016 UCL Information Retrieval and Data Mining group coursework project.

Group members are Barnaby Brien, Henrik Ebenhag, Alexander Lilburn and Derek Lukacsko.

---

### Pre-requisites
This package uses **Python 3** and requires `numpy`, `pandas`, `scipy`, `statsmodels` and `networkx`. All are easily installable via pypi:  
>`pip install ...`

---

The following package uses NNMF, or non-negative matrix factorisation, 
to extract general themes and topics from data pulled from Twitter.

The dataset includes just under 2 million tweets from around the Greater London area
from the latter part of 2015.

The implementation takes advantage of the sparsity of the bag-of-words tweet representation
to enable the data to be processed on most local machines.

First, the tweets are scored for relevance to a query using the [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 
scoring algorithm. The number of results returned is capped to 1000 for reasons of required computational power.

The tweets are then decomposed into **W** and **H** matrices (described below) via NNMF. This allows representation of
subtopics within the returned tweets.

The **W** and **H** matrices are learned via the iterative algorithm described in 
[Lee & Seung](http://www.columbia.edu/~jwp2128/Teaching/W4721/papers/nmf_nature.pdf)'s
article in _Nature_. The columns of **W** contain the basis vectors or components making up all of the tweets.
These co-occurring word vectors can then be considered as themes or topics: a property that is facilitated
by the sparseness of the resulting matrix.

The matrix **H** then forms the encodings on which the basis vectors may be combined to reconstruct an
approximation of the original data. Displaying these encodings in weighted graph form allows us to visualise
proximity of subtopics as well as the distribution of tweets amongst these suptopics.

### Manual
1. In Terminal, navigate to the project root directory
2. Run `python main.py`.
3. Enter keywords to search data on and number of topics you wish to retrieve.
4. Receive lists of co-occuring words sorted by relevance to each sub-topic.
