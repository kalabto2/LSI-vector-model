# import numpy as np
from numpy import amax as np_amax
from numpy import count_nonzero as np_count_nonzero
from numpy import log2 as np_log2
from numpy import array as np_array
from numpy import float as np_float
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix


def term_weightening(freqMatrix: np_array):
    """
    VERSION TO DENSE MATRIX -- OLD
    Modify term by document Matrix. To elements adds weight according to following equation:
        w = tf * idf = tf * log2(n/df)
    :return numpy array
    """
    n = freqMatrix.shape[1]  # number of all documents
    maxF = np_amax(freqMatrix, axis=1)  # array; max frequency of terms in all documents
    tf = (freqMatrix.T / maxF).T  # array; normalized term frequency of term ti in document dj
    df = np_count_nonzero(freqMatrix, axis=1)  # array of numbers of documents containing term ti
    idf = np_log2(n/df)  # array of  inverse document frequency of term ti
    w = (tf.T * idf).T  # final term by document matrix with weight

    print(n)
    print(freqMatrix)
    print(maxF)
    print(tf)
    print(w)

    return w


def add_term_weights(f: coo_matrix):
    """
    Modify term by document Matrix. To elements adds weight according to following equation:
        w = tf * idf = tf * log2(n/df)
            * f ij = frequency of term t i in document d j
            * tf ij = f ij / max i {f ij }
            * df i = document frequency of term t i = number of documents containing term t i
            * idf i = inverse document frequency of term t i = log 2 (n / df i ), where n is the total number of docs.
    :return coo_matrix of term-by-document with weights
    """
    print("Adding weights to terms")
    n = f.shape[1]  # number of all documents
    maxF = np_amax(f, axis=1)  # coo_matrix; max frequency of terms in all documents # FIXME ma byt nejspis pocet termu v danem dokumentu ... pak by bylo ve fci 'axis=0'
    print("1")
    tmp1 = [1] * f.shape[1]
    print("2")
    tmp = csr_matrix.multiply(csr_matrix(maxF), csr_matrix([1] * f.shape[1]))  # helping variable; todo too slow
    print("3")
    rows = f.row
    cols = f.col
    data = [c/tmp[a, b] for a, b, c in zip(f.row, f.col, f.data)]

    tf = coo_matrix((data, (rows, cols)), shape=(f.shape[0], f.shape[1]), dtype=np_float)
    print("4")
    df = coo_matrix.getnnz(f, axis=1)  # np.array;
    idf = np_log2(n / df)  # np.array;
    w = tf.copy()
    w.data *= idf[w.row]

    return w  # coo_matrix


def add_weight_to_query(bow: coo_matrix, query: coo_matrix, verbose: bool = True):    # TODO uplne nevim, jestli to delam spravne ...
    """
    Weightens query same way as function 'add_term_weights'
    """

    if(verbose):
        print("Adding weights to query")
    n = bow.shape[1]  # number of all documents
    maxF = np_amax(bow, axis=1)
    tf = coo_matrix(query / maxF)
    df = coo_matrix.getnnz(bow, axis=1)
    idf = np_log2(n / df)  # np.array;
    w = tf.copy()
    w.data *= idf[w.row]
    return w
