""" A script for running and testing nnmf
notes:
Total 1953447 tweets
"""
import json

from Util.Import import load_new_file, get_files
from model.nnmf import *

number_of_files = 1
number_of_topics = 10
iterations = 20
matrix_density = 0.05
convergence = None


if __name__ == "__main__":
    paths = get_files('./data/')

    # Comment out following line to run factorisation on entire dataset
    paths = paths[:number_of_files]

    length = len(paths)

    with open('./dictionaries/id_to_term_dictionary.txt', 'r') as f:
        dict = json.load(f)

    unique_terms = len(dict.keys())

    matrix = []
    for i, path in enumerate(paths):
        print("Loading data: {:0.2%}".format(i / length), end='\r')
        data = load_new_file(path)
        matrix += data['vector'].tolist()
    print("Data loaded.              ")
    del data

    # matrix = load_new_file(paths[0])
    # matrix = matrix['vector'].tolist()

    matrix = build_sparse_matrix(matrix, unique_terms, verbose=True)

    w, h = factorise(matrix, topics=number_of_topics, iterations=iterations, init_density=matrix_density,
                     convergence=convergence)

    evaluate(w, dict)
