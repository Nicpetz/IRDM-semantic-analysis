from Util.Import import load_new_file, load_original_file, get_files
import unicodedata as ud
import re
import json
import math

class Vectoriser:
    """
    Class for building vectors from tweets
    """
    def __init__(self):
        self.dictionary = {}
        self.id_reference = {}
        self.idf = {}
        self.n_dt = {}
        self.document_count = 0
        self._id = 0

    def generate_id(self):
        """
        :return: numbers incrementing by 1 each time function is called
        """
        self._id += 1
        return self._id

    def count(self, string):
        """
        Counts documents containing each word in string and builds id/term dictionaries
        :param string: text sentence
        :return: null
        """
        self.document_count += 1
        string = self.tokeniser(string)
        processed = []
        for word in string:
            try:
                id = self.dictionary[word]
            except KeyError:
                id = self.generate_id()
                self.dictionary[word] = id
                self.id_reference[id] = word
            if word not in processed:
                try:
                    self.n_dt[id] += 1
                except KeyError:
                    self.n_dt[id] = 1

    def build_idf(self):
        """
        Computes inverse document frequency as a class attribute
        :return: null
        """
        self.idf = {term_id: math.log(self.document_count / self.n_dt[term_id], 2) for term_id in self.n_dt.keys()}

    def vectorise(self, string):
        """
        convert string into a bag of words vector
        :param string: text sentence
        :return: sparse vector in dictionary format
        """
        sentence = self.tokeniser(string)
        vector = {}

        for word in sentence:
            id = self.dictionary[word]
            try:
                vector[id] += 1
            except KeyError:
                vector[id] = 1

        for k in vector.keys():
            vector[k] *= self.idf[k]

        return vector

    def add_vector(self, df):
        """
        add vector to dataframe
        :param df: dataframe with no vector
        :return: dataframe with vector
        """
        df['vector'] = df['text'].map(lambda text: self.vectorise())
        return df

    def tokeniser(self, string):
        """
        split full sentence into list of tokens
        :param string: text sentence
        :return: list of tokens
        """
        # TODO: develop tokeniser
        string = string.lower()
        list = string.split()
        return list

# get filenames for original data and new processed data
files = get_files('./Twitter')
new_files = get_files()

# initialise vectoriser tool
vec = Vectoriser()
no_files = len(files)

# loop over original data to build term dictionaries and count term frequencies
for i, file in enumerate(files):
    if i % 20 == 0:
        print("Building IDF: {}/{} files\r".format(i+1, no_files), end='\r')
    data = load_original_file(file)
    data = data[['username', 'date', 'text', 'profileLocation', 'latitude', 'longitude']]
    data.text.map(lambda tweet: vec.count(tweet))
    if i == no_files - 1:
        print("Building IDF: Complete")

# save id/term dictionaries in json format
with open('term_to_id_dictionary.txt', 'w') as fp:
    json.dump(vec.dictionary, fp)

with open('id_to_term_dictionary.txt', 'w') as fp:
    json.dump(vec.id_reference, fp)

# calculate inverse document frequency from documents
vec.build_idf()

# add vector to data, drop unnecessary columns and save data to new path
for i, file in enumerate(files):
    if i % 20 == 0:
        print("Adding vector to data: {}/{} files\r".format(i+1, no_files), end='\r')
    data = load_original_file(file)
    data = data[['username', 'date', 'text', 'profileLocation', 'latitude', 'longitude']]
    data = vec.add_vector(data)
    if i == no_files - 1:
        print("Vectorising: Complete")
    data.to_json(new_files[i], orient='index')



