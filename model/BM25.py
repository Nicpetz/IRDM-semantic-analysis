import math
from Util.adhoc_vectoriser import vectorise


def DocLength(Doc):
    """
    Calculates length of a document
    """
    return sum(Doc.values())


def AvgDocLength(Docs):
    """
   Calculates average length of all documents within a set
    """
    count = 0
    total = 0

    for Doc in Docs:
        total += DocLength(Doc)
        count += 1

    try:
        avg = total / count
    except:
        raise ZeroDivisionError("Query not in corpus")

    return avg


def MakeIDF(query, docs):
    """
    Cacuates the IDF portion of the code in which the inverse distribution function is calculated for each query
    """
    IDF = {}
    N = len(docs.keys())
    for term in query.keys():
        if term not in IDF:
            n = 0
            for key in docs:
                if str(term) in docs[key].keys():
                    n += 1
            idf = math.log((N - n + 0.5)/(n + 0.5), 2)
            IDF[term] = idf
    return IDF


def termFreq(term, doc):
    """
    Checks for a given term within the document and if it is present returns its frequency
    """
    if str(term) in doc.keys():
        return doc[str(term)]
    else:
        return 0.0


def calcBM25(query, doc, IDF, k, b, avgdl):
    """
    Iterates through the keys of the query scoring each individually before returning the sum of these scores
    """
    score = 0.0

    for key in query.keys():
        numer = termFreq(str(key), doc) * (k + 1.0)
        denom = termFreq(str(key), doc) + (k * (1.0 - b) + (b * DocLength(doc) / avgdl))
        score += IDF[key] * (numer / denom)

    return score


def BM25(data, keywords, k, b, max_tweets):
    """
    Iterates through all queries and then all docs calculating the BM25 scores for each query, saving these, having been
    ordered in the set file path.
    """
    matrix = []
    query_v = vectorise(keywords)
    IDF = MakeIDF(query_v, data.vector)
    avgD = AvgDocLength(data.vector)
    data["BM25"] = data.vector.apply(lambda x: calcBM25(query_v, x, IDF, k, b, avgD))
    data = data.sort_values("BM25", ascending=False)
    data = data.reset_index()
    try:
        matrix += data['vector'][0:max_tweets].tolist()
        return data, matrix
    except:
        matrix += data['vector'].tolist()
        return data, matrix
