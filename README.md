# IRDM-sentiment-analysis

This repository is for the 2016 UCL Information Retrieval and Data Mining group coursework project.

Group members are:

1. Barnaby Brien
2. Henrik Ebenhag
3. Alexander Lilburn
4. Derek Lukacsko

---

### Pre-requisites
This package uses **Python 3** and requires `numpy`, `pandas` and `scipy`. All are easily installable via pypi:  
>`pip install ...`

---

### Introduction
The following package uses NNMF, or non-negative matrix factorisation, 
to extract general themes and topics from data pulled from Twitter.

The dataset includes just under 2 million tweets from around the Greater London area
from the latter part of 2015.

The implementation takes advantage of the sparsity of the bag-of-words tweet representation
to enable the data to be processed on most local machines.

The **W** and **H** matrices are learned via the iterative algorithm described in 
[Lee & Seung](http://www.columbia.edu/~jwp2128/Teaching/W4721/papers/nmf_nature.pdf)'s
article in _Nature_. The columns of **W** contain the basis vectors or components of the tweets.
These can be considered as themes or topics of co-occurring words.

