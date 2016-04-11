from scipy.sparse import dok_matrix, rand, linalg


def build_sparse_matrix(list_of_dicts, vector_length, orient='columns', verbose=False):
    """
    Function for building sparse matrix from list of dicts
    :param list_of_dicts: list of dictionaries representing sparse vectors
    :param vector_length: number of values in dense representation of sparse vector
    :param orient: build matrix by rows or columns - default is columns
    :return: sparse matrix
    """
    if orient == 'columns':
        columns = len(list_of_dicts)
        matrix = dok_matrix((vector_length, columns))
        for column, vector in enumerate(list_of_dicts):
            if verbose:
                print("Building matrix {0:0.2f}%".format((column / columns) * 100), end='\r')
            for term in vector.keys():
                matrix[int(term), column] = vector[term]
    elif orient == 'rows':
        rows = len(list_of_dicts)
        matrix = dok_matrix(shape=(rows, vector_length))
        for row, vector in enumerate(list_of_dicts):
            if verbose:
                print("Building matrix {0:0.2f}%".format((row / rows) * 100), end='\r')
            for term in vector.keys():
                matrix[row, term] = vector[term]
    else:
        raise ValueError('Orient must be either \'columns\' or \'rows\'')
    if verbose:
        print("Matrix complete")
    return matrix


def cost(a, b):
    """
    Function takes two sparse matrices and
    returns total Euclidian distance between all vectors
    :param a: sparse matrix 1
    :param b: sparse matrix 2
    :return: Euclidian distance
    """
    dif = 0
    rows, columns = a.shape
    for i in range(rows):
        for j in range(columns):
            # Euclidean Distance
            dif += (a[i, j] - b[i, j]) ** 2
    return dif


def factorise(v, topics=10, iterations=50):
    """
    Factorise function computes Non-negative Matrix Factorisation of input data
    :param v: input data matrix (data instances (tweets) are columns
    :param topics: number of topics required in output
    :param iterations: maximum number of training iterations
    :return w: component feature matrix - component vectors found in columns of matrix
    :return h: matrix for reconstruction of original data from component features
    """
    v = dok_matrix(v)
    terms = v.shape[0]
    instances = v.shape[1]

    # Initialize the weight and feature matrices with random values
    # w: terms x topics sized matrix
    w = rand(terms, topics, density=0.001, format='dok')
    # h: topics x instances sized matrix
    h = rand(topics, instances, density=0.001, format='dok')

    # Repeat E and M step  maximum 'iterations' number of times
    for i in range(iterations):
        print("Iteration: {}".format(i + 1))
        # E step
        # wh: terms x instances sized matrix
        wh = w * h

        # Calculate the current difference between factorisation and actual
        temp_cost = cost(v, wh)

        if i % 10 == 0:
            print(temp_cost)

        # End if matrix perfectly factorised
        if temp_cost == 0:
            break

        # M step
        # Update feature matrix
        # hn: topics x instances matrix
        hn = w.transpose() * v
        # hd: topics x instances matrix
        hd = w.transpose() * w * h

        # h: topics x instances matrix
        h = (h * hn) * linalg.inv(hd)

        # Update weights matrix
        # wn: terms x topics matrix
        wn = v * h.transpose()
        # wd: terms x topics matrix
        wd = w * h * h.transpose()

        # w: terms x topics matrix
        w = (w * wn) * linalg.inv(wd)

    return w, h
