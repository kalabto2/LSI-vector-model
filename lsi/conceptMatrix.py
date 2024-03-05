# import numpy as np
from numpy import array as np_array
from numpy import transpose as np_transpose
from scipy.sparse import coo_matrix, eye
from scipy.sparse.linalg import svds
from scipy.sparse.linalg import inv
import time


def singular_value_decomposition(A: coo_matrix, k: int=250):
    """
    Decompose matrix A to matrices according to:
        A = U*S*V^T
    where   * U contains eigenvectors of matrix A * A^T
            * V contains eigenvectors of matrix A^T * A
            * S contains eigenvalues on its diagonal in descending order
    :param A: term-document matrix
    :return: U, S, V^T
    """

    time_start = time.time()
    print("Calculating SVD")
    # k = 50  # TODO funkce na zjisteni 'k'
    print(" docs count : {0}, K: {1}".format(min(A.shape), k))
    u, s, vt = svds(A, k=k)
    S = coo_matrix(eye(k))
    S.data = S.data * s[::-1]  # sorted descending ...
    print("SVD time: {0}".format(time.time() - time_start))
    return u, S, vt


def query_to_concept(q, S: coo_matrix, U: np_array, verbose: bool = True):
    """
    Projects query into a concept space according to equation:
        q_conceptSpace = S^(-1) * U^T * q_docSpace
    :param q: query in space of documents
    :param S: S matrix from SVD
    :param U: U matrix from SVD
    :return: computed value of concept-query
    """
    if verbose:
        print("Projecting query into space of concepts")
    qConcept = inv(S.tocsc()) * np_transpose(U) * q
    return qConcept


def get_concept_by_document_matrix(S: coo_matrix, VT, verbose: bool = True):
    """
    returns concept-by-document matrix
    """
    if verbose:
        print("Projecting BoW matrix into space of concepts")
    D = S * VT
    return D
