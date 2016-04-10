from Util.Import import load_file, get_files
import unicodedata as ud
import re
import json
import math

class Vectoriser:
    def __init__(self):
        self.dictionary = {}
        self.idf = {}
        self.n_dt = {}
        self.document_count = 0
        self._id = 0

    def generate_id(self):
        self._id += 1
        return self._id

    def count_n_dt(self, string):
        self.document_count += 1
        string = string.split()
        processed = []
        for word in string:
            word = word.lower()
            try:
                id = self.dictionary[word]
            except KeyError:
                id = self.generate_id()
                self.dictionary[word] = id
            if word not in processed:
                try:
                    self.n_dt[id] += 1
                except KeyError:
                    self.n_dt[id] = 1

    def build_idf(self):
        self.idf = {term_id: math.log(self.document_count / self.n_dt[term_id], 2) for term_id in self.n_dt.keys()}

    def vectorise(self, string):
        string = string.split()
        vector = {}

        for word in string:
            word = word.lower()
            id = self.dictionary[word]
            try:
                vector[id] += 1
            except KeyError:
                vector[id] = 1

        for k in vector.keys():
            vector[k] *= self.idf[k]

        return vector

files = get_files('./Twitter')
new_files = get_files()
vec = Vectoriser()
no_files = len(files)
for i, file in enumerate(files):
    if i % 20 == 0:
        print("Building IDF: {}/{} files\r".format(i+1, no_files), end='')
    data = load_file(file)
    data = data[['username', 'date', 'text', 'profileLocation', 'latitude', 'longitude']]
    data.text.map(lambda tweet: vec.count_n_dt(tweet))
    if i == no_files - 1:
        print("Building IDF: Complete")

with open('term_dictionary.txt', 'w') as fp:
    json.dump(vec.dictionary, fp)


vec.build_idf()

for i, file in enumerate(files):
    if i % 20 == 0:
        print("Adding vector to data: {}/{} files\r".format(i+1, no_files), end='')
    data = load_file(file)
    data = data[['username', 'date', 'text', 'profileLocation', 'latitude', 'longitude']]
    data['vector'] = data.text.map(lambda tweet: vec.vectorise(tweet))
    if i == no_files - 1:
        print("Vectorising: Complete")
    data.to_json(new_files[i], orient='index')

print('Saving term to id dictionary')
vec.dictionary.to_json('term_dictionary.txt', orient='index')
print('Complete')

