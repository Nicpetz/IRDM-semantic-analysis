import math


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

    avg = total / count

    return avg


def MakeIDF(query, docs):
    """
    Cacuates the IDF portion of the code in which the inverse distribution function is calculated for each query
    """
    IDF = {}
    N = len(docs.keys())
    for term in query:
        if term not in IDF:
            n = 0
            for key in docs:
                if term in docs[key].keys():
                    n += 1
            idf = math.log((N - n + 0.5)/(n + 0.5), 2)
            IDF[term] = idf
    return IDF


def termFreq(term, doc):
    """
    Checks for a given term within the document and if it is present returns its frequency
    """
    if term in doc.keys():
        return doc[term]
    else:
        return 0.0


def calcBM25(query, doc, IDF, k, b, avgdl):
    """
    Iterates through the keys of the query scoring each individually before returning the sum of these scores
    """
    score = 0.0

    for key in query:
        numer = termFreq(key, doc) * (k + 1.0)
        denom = termFreq(key, doc) + (k * (1.0 - b) + (b * DocLength(doc) / avgdl))
        score += IDF[key] * (numer / denom)

    return score


def BM25(tweets, query, k, b):
    """
    Iterates through all queries and then all docs calculating the BM25 scores for each query, saving these, having been
    ordered in the set file path.
    """
    avgdl = AvgDocLength(tweets)
    IDF = MakeIDF(query, tweets)

    scores = {}
    for d in tweets:
        score = calcBM25(query, tweets[d], IDF, k, b, avgdl)
        scores[d] = score

    return scores

