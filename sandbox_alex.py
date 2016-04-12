""" A script for playing around
notes:
Total 1953447 tweets
"""
from Util.Import import load_new_file, get_files
from nnmf import *
import json

import regex
import re
import pandas as pd
from emoji import UNICODE_EMOJI
import unicodedata as ud

paths = get_files('./data/')
length = len(paths)

with open('id_to_term_dictionary.txt', 'r') as f:
    dict = json.load(f)

unique_terms = len(dict.keys())

# Uncomment to run factorisation on entire dataset
# matrix = []
# for i, path in enumerate(paths):
#     print("Loading matrix: {0:0.2f}%".format((i / length) * 100), end='\r')
#     data = load_new_file(path)
#     matrix += data['vector'].tolist()
# print("Matrix loaded.")
# del data

matrix = load_new_file(paths[0])
matrix = matrix['vector'].tolist()

matrix = build_sparse_matrix(matrix, unique_terms, verbose=True)

w, h = factorise(matrix, topics=5, iterations=20, init_density=0.1)

print("Successfuly factorised!")

evaluate(w, dict)

