""" A script for running and testing nnmf
notes:
Total 1953447 tweets
"""
import json
import pandas as pd
import numpy as np
from Util.Import import load_new_file, get_files
from model.nnmf import build_sparse_matrix, factorise, evaluate
from model import search
from model import BM25
from Util.adhoc_vectoriser import vectorise

number_of_files = None
number_of_topics = 10
iterations = 20
max_tweets = 1000
matrix_density = 0.03
convergence = 0.1
search_terms = input('Enter search terms: ')
while len(search_terms) < 1:
    search_terms = input('Please enter one or more keywords: ')


if __name__ == "__main__":

    paths = get_files('./data/')

    # Comment out following line to run factorisation on entire dataset
    if number_of_files is not None:
        paths = paths[:number_of_files]

    length = len(paths)

    with open('./dictionaries/id_to_term_dictionary.json', 'r') as f:
        dict = json.load(f)

    unique_terms = len(dict.keys())
    print("{} total unique terms".format(unique_terms))

    matrix = []
    data = pd.DataFrame()

    keywords = search_terms.split()
    l = len(keywords)
    for i, path in enumerate(paths):
        print("Searching data: {:0.2%}".format(i / length), end='\r')
        data_temp = load_new_file(path)
        arr = "[" + ("keywords[%i].lower() in string.lower() or " * (l-1)) + "keywords[%i].lower() in string.lower()" +\
              " for string in data_temp['text']]"
        arr = eval(arr % tuple([i for i in range(l)]))
        data_temp = data_temp[arr]
        data = pd.concat([data, data_temp])
    print("Data search complete.              ")
    print("{} tweets found for '{}'.\n".format(len(data), search_terms))

    print("Running BM25 to rank data.")
    data, matrix = BM25.BM25(data, keywords, 1.5, 0.5, max_tweets)
    print("Complete. {} tweets returned\n".format(len(data)))

    matrix = build_sparse_matrix(matrix, unique_terms, verbose=True)

    print("Running NNMF factorisation.")
    w, h = factorise(matrix, topics=number_of_topics, iterations=iterations, init_density=matrix_density,
                     convergence=convergence)

    evaluate(w, dict)

    non_zero_prop = np.count_nonzero(h.toarray().sum(axis=0)) / h.shape[1]
    print('Proportion of tweets with at least one topic assigned: {:0.2%}'.format(non_zero_prop))

    # Adjacency matrix code
    # h = h.toarray()
    # h = h[:, np.nonzero(h.sum(axis=0))]
    # h = h[:, 0, :]
    # topic_zero = np.zeros((number_of_topics, number_of_topics))
    # tweet_zero = np.zeros((h.shape[1], h.shape[1]))
    # h_t = h.transpose()
    # top = np.concatenate((topic_zero, h), axis=1)
    # bottom = np.concatenate((h_t, tweet_zero), axis=1)
    # final = np.concatenate((top, bottom))
    #
    # pd.DataFrame(final).to_csv('./sample_output.csv', header=[i for i in range(final.shape[0])], index=[i for i in range(final.shape[0])])
