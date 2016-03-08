""" A script for playing around and *trying* to make magic happen
"""
from Util.Import import load_file, get_files


paths = get_files()
data = load_file(paths[0])

tweets = ' '.join(data['text'])

print(tweets)