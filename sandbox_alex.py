""" A script for playing around
notes:
Total 1953447 tweets
Total 2875223 unique terms

"""
from Util.Import import load_file, get_files
from nnmf import *
import json

import regex
import re
import pandas as pd
from emoji import UNICODE_EMOJI
import unicodedata as ud

paths = get_files('./data/')
length = len(paths)
matrix = []


# for i, path in enumerate(paths):
#     print("Loading matrix: {0:0.2f}%".format((i / length) * 100), end='\r')
#     data = load_file(path)
#     matrix += data['vector'].tolist()
# print("Matrix loaded.")
# del data

matrix = load_file(paths[0])
matrix = matrix['vector'].tolist()

matrix = build_sparse_matrix(matrix, 2875223, verbose=True)

w, h = factorise(matrix)

print("Success!")
print(w.A)

