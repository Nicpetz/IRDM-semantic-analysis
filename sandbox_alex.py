""" A script for playing around
"""
from Util.Import import load_file, get_files
import regex
import re
import pandas as pd
from emoji import UNICODE_EMOJI
import unicodedata as ud

paths = get_files('./Twitter/')


data = load_file(paths[0])
# print(data['text'][4])
# for i in data['text'][4]:
    # print(ud.category(i))

print(data.columns)



