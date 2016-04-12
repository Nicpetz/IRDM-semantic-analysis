from scipy.sparse import dok_matrix, csc_matrix, rand


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

    print("Matrix complete.                    ")
    return csc_matrix(matrix)


def cost(a, b):
    """
    Function takes two sparse matrices and
    returns total Euclidian distance between all vectors
    :param a: sparse matrix 1
    :param b: sparse matrix 2
    :return: Euclidian distance
    """
    diff = a - b
    diff = diff.multiply(diff)
    diff = diff.sum()
    return diff


def factorise(M, topics=10, iterations=50, init_density=0.01):
    """
    Factorise function computes Non-negative Matrix Factorisation of input data
    :param M: input data matrix (data instances (tweets) are columns
    :param topics: number of topics required in output
    :param iterations: maximum number of training iterations
    :param init_density: density of initialised weight matrices W and H (proportion or non-zero values)
    :return W: component feature matrix - component vectors found in columns of matrix
    :return H: matrix for reconstruction of original data from component features
    """
    # v = dok_matrix(v)
    terms = M.shape[0]
    instances = M.shape[1]

    # Initialize the weight and feature matrices with random values
    # W: terms x topics sized matrix
    W = rand(terms, topics, density=init_density, format='csc')
    # H: topics x instances sized matrix
    H = rand(topics, instances, density=init_density, format='csc')

    # Repeat iterative algorithm maximum 'iterations' number of times
    for i in range(iterations):
        print("Iteration: {}/{}       ".format(i + 1, iterations), end='\r')
        # E step
        # WH: terms x instances sized matrix
        WH = W * H

        # Calculate the current difference between factorisation and actual
        temp_cost = cost(M, WH)

        # End if matrix perfectly factorised
        if temp_cost == 0:
            break

        # Update feature matrix
        # Hn: topics x instances matrix
        Hn = W.transpose() * M
        # Hd: topics x instances matrix
        Hd = W.transpose() * W * H
        Hd.data[:] = 1 / Hd.data

        # H: topics x instances matrix
        H = H.multiply(Hn).multiply(Hd)

        # Update weights matrix
        # Wn: terms x topics matrix
        Wn = M * H.transpose()
        # Wd: terms x topics matrix
        Wd = W * H * H.transpose()
        Wd.data[:] = 1/Wd.data

        # W: terms x topics matrix
        W = W.multiply(Wn).multiply(Wd)
    print('Successfuly factorised')
    return dok_matrix(W), dok_matrix(H)


def evaluate(W, term_dict, print_output=True):
    """
    Evaluate W matrix from nnmf,
    :param W: W matrix
    :param term_dict: id to term reference dictionary
    :return: list of topics containing terms and relative values
    """
    items = W.items()
    topics = [[] for i in range(W.shape[1])]
    for index, value in items:
        term_value = (term_dict[str(index[0])], value)
        topics[index[1]].append(term_value)
    if print_output:
        for i, t in enumerate(topics):
            print("Topic {}: ".format(i+1))
            for term, value in t[:-1]:
                print(term + ",", end=' ')
            print('{}\n'.format(t[-1][0]))

    return topics
