# import numpy as np
from numpy import array as np_array
from numpy import dot as np_dot
from numpy.linalg import norm as np_linalg_norm

import time


def cosine_similarity(a: np_array, b: np_array):
    dot = np_dot(a, b)
    normA = np_linalg_norm(a)
    normB = np_linalg_norm(b)
    cos = dot / (normA * normB)
    return cos


def get_similar_docs(conceptMatrix: np_array, query: np_array, use_threshold:bool = False, verbose: bool = True):
    """
    Compares query with all docs
    :param conceptMatrix: concept-by-document matrix
    :param query: query in concept-by-document matrix
    :param treshold:
    :return: dict {number_of_document: cosine_similarity_with_query} sorted by value ascending
    """

    time_start = time.time()
    if verbose:
        print("Comparing query with docs")

    result = {}
    i = 0
    for doc in conceptMatrix.T:
        similarity = cosine_similarity(doc, query)
        if use_threshold:
            if similarity > 0.55:
                result[i] = similarity
        else:
            result[i] = similarity
        # result[i] = similarity
        i += 1

    print("Query time: {0}".format(time.time() - time_start))

    return dict(enumerate([(k, v) for k, v in sorted(result.items(), key=lambda item: 1 - abs(item[1]))]))
