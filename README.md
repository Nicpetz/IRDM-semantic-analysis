# IRDM-Semantic-Analysis

This repository is for the 2016 UCL Information Retrieval and Data Mining group coursework project.

Group members are:

1. Barnaby Brien
2. Henrik Ebenhag
3. Alexander Lilburn
4. Derek Lukacsko

---

### Pre-requisites
This package uses **Python 3** and requires `numpy`, `pandas`, `scipy` and `stop_words`. All are easily installable via pypi:  
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
article in _Nature_. The columns of **W** contain the basis vectors or components making up all of the tweets.
These co-occurring word vectors can then be considered as themes or topics: a property that is facilitated
by the sparseness of the resulting matrix.

The matrix **H** then forms the encodings on which the basis vectors may be combined to reconstruct an
approximation of the original data. Interestingly, this can provide a foundation for identifying trends over time.

To provide an explanatory example, for the comparison of topic volume between two days, one would take the tweets from
those two days, and run NNMF over this matrix. Then, by taking the **H** matrix and splitting it into the sections
corresponding to the respective days, and calculating the mean of the encoding of each topic in those two
resulting sub-**H** matrices, one can then compare the means from each day to get a measure for the proportion of
Twitter volume each topic accounted for on either day.

Implementation coming soon.

