""" A script for running and testing nnmf
notes:
Total 1953447 tweets
"""
from Util.Import import load_new_file, get_files
from nnmf import *
import json


number_of_files = 5
number_of_topics = 5
iterations = 20
matrix_density = 0.1


if __name__ == "__main__":
    paths = get_files('./data/')
    length = len(paths)

    with open('id_to_term_dictionary.txt', 'r') as f:
        dict = json.load(f)

    unique_terms = len(dict.keys())

    # Uncomment to run factorisation on entire dataset
    matrix = []
    for i, path in enumerate(paths[:number_of_files]):
        print("Loading matrix: {0:0.2f}%".format((i / length) * 100), end='\r')
        data = load_new_file(path)
        matrix += data['vector'].tolist()
    print("Matrix loaded.")
    del data

    # matrix = load_new_file(paths[0])
    # matrix = matrix['vector'].tolist()

    matrix = build_sparse_matrix(matrix, unique_terms, verbose=True)

    w, h = factorise(matrix, topics=number_of_topics, iterations=iterations, init_density=matrix_density)

    evaluate(w, dict)

