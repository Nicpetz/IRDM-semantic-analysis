""" A script for playing around
"""
from Util.Import import load_file, get_files
import pandas as pd

paths = get_files()
data = pd.read_json(paths[1], orient='index')

# print(data.text[4].split()[4].decode('unicode-escape'))



print(data.head())

