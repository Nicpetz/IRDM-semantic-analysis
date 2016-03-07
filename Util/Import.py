import pandas as pd
import json


def load_file(filename):
    """
    Function for loading Twitter data into Pandas DataFrame
    :param filename: str. path to text file in json format
    :return: Pandas DataFrame
    """
    try:
        if filename[-4:] != '.txt':
            raise TypeError('Use .txt file not .csv')
    except:
        raise ValueError('Filename could not be processed. '
                         'Check it is a path to .txt file of Twitter data in json format')
    with open(filename) as f:
        data = json.load(f)
    data = pd.DataFrame(data['tweets'])
    data['date'] = data['date'].map(lambda x: int(x/1000))
    data['date'] = pd.to_datetime(data['date'], unit='s')
    return data
