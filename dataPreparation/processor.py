import nltk
# import os
from os import getcwd
# import numpy as np
from numpy import array as np_array
from numpy import argsort as np_argsort
from numpy import empty as np_empty
from numpy import intc as np_intc
from numpy import searchsorted as np_searchsorted
from numpy import unique as np_unique
from numpy import repeat as np_repeat
from numpy import where as np_where
from numpy import zeros as np_zeros
from scipy.sparse import coo_matrix
try:
    nltk.data.path.append(getcwd() + "/stopwords")
    nltk.find("stopwords", ".")
except LookupError:
    nltk.download("stopwords", "./stopwords")
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def preprocess_data(documents: dict) -> dict:
    """Preprocess data. Returns dictionary in format: <Title>: <BoW document>"""
    print("Processing data")
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = set(stopwords.words('english'))
    p_stemmer = PorterStemmer()
    texts = {}
    for title, text in documents.items():
        raw = text.lower()
        tokens = tokenizer.tokenize(raw)
        stopped_tokens = [i for i in tokens if i not in en_stop]
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        texts[title] = stemmed_tokens
    return texts


def get_matrix(documents: dict) -> (coo_matrix, list, list):
    """Returns Term by Document matrix represented as pd.DataFrame """
    print("Creating matrix")
    vocab = set()
    non_zero = 0
    for document in documents.values():
        unique_terms = set(document)
        vocab |= unique_terms
        non_zero += len(unique_terms)

    titles = list(documents.keys())
    titles = np_array(titles)
    vocab = np_array(list(sorted(vocab)))
    vocab_sorter = np_argsort(vocab)
    titles_cnt = len(titles)
    terms_cnt = len(vocab)
    data = np_empty(non_zero, dtype=np_intc)  # all non-zero term frequencies at data[k]
    rows = np_empty(non_zero, dtype=np_intc)  # row index for kth data item (kth term freq.)
    cols = np_empty(non_zero, dtype=np_intc)

    index = 0  # current index in the sparse matrix data
    # go through all documents with their terms
    for docname, terms in documents.items():
        # find indices into  such that, if the corresponding elements in  were
        # inserted before the indices, the order of  would be preserved
        # -> array of indices of  in
        term_indices = vocab_sorter[np_searchsorted(vocab, terms, sorter=vocab_sorter)]

        # count the unique terms of the document and get their vocabulary indices
        uniq_indices, counts = np_unique(term_indices, return_counts=True)
        n_vals = len(uniq_indices)  # = number of unique terms
        ind_end = index + n_vals  # to  is the slice that we will fill with data

        data[index:ind_end] = counts  # save the counts (term frequencies)
        rows[index:ind_end] = uniq_indices  # save the column index: index in
        doc_idx = np_where(titles == docname)  # get the document index for the document name
        cols[index:ind_end] = np_repeat(doc_idx, n_vals)  # save it as repeated value

        index = ind_end  # resume with next document -> add data to the end

    dtm = coo_matrix((data, (rows, cols)), shape=(terms_cnt, titles_cnt), dtype=np_intc)

    return dtm, vocab.tolist(), titles.tolist()


def query_to_document(query: list, vocab: list):
    """
    Creates term-by-document (with element as frequency of occurrences in doc)
    :param query: preprocessed list of terms representing query
    :param vocab: all terms, which database know
    """
    a = np_zeros((len(vocab), 1))
    for term in query:
        if term in vocab:
            a[vocab.index(term)][0] += 1
    queryMatrix = coo_matrix(a)

    return queryMatrix  # matrix of shape: all_terms_in_all_docs x 1




