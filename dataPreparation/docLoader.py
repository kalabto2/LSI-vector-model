import xml.dom.minidom as md
# import re
from re import sub
# import glob
from glob import glob
# import os
from os import getcwd
from os import mkdir
from os import chdir
from os.path import exists
from os.path import isfile
# import codecs
from codecs import open as codecs_open
# import shutil
from shutil import rmtree
import dataPreparation.processor as pr
import lsi.preparation as prep
import lsi.conceptMatrix as cm
from numpy import savez_compressed
from numpy import load
# import pickle
from pickle import dump
from pickle import DEFAULT_PROTOCOL
from pickle import load as pickle_load
# import scipy
# import scipy.sparse
from scipy.sparse import save_npz
from scipy.sparse import load_npz

def remove_special_characters(directory: str) -> None:
    """Removes unicode uninterpretable characters from sgm files in reuters21578 directory for DOM.
    Clean file is stored as <original_file_name>_copy.sgm in <original_directory>/cleanDocs.
    Also adds root tag <ROOT>"""

    # Initialization
    start_dir = getcwd()
    if exists(start_dir + "/cleanDocs"):
        rmtree(start_dir + "/cleanDocs")
    mkdir(start_dir + "/cleanDocs")
    chdir(directory)

    for tmp_file in glob("*[0-9].sgm"):
        # Removing special chars
        with codecs_open(tmp_file, "r", encoding='utf-8', errors='ignore') as file:
            text = []
            for line in file.readlines():
                text.append(sub(r"&.*;", '', line))

        # Adding root elements
        text[0] = "<ROOT>\n"
        text.append("</ROOT>")

        # Storing results
        out_name = tmp_file[:-4] + "_copy" + tmp_file[-4:]
        with open(start_dir + "/cleanDocs/" + out_name, "w") as out_file:
            for l in text:
                out_file.write(l)

    # Cleanup
    chdir(start_dir)


def get_documents(count: int = 0) -> dict:
    """Gets maximum <count> of documents. If count is not specified (is 0), all documents are processed.
     Returns dictionary where keys are titles and values are documents.
    If document is duplicated in main data it is added only once"""

    ret_documents = {}
    iteration = 0

    # Data preparation
    remove_special_characters("reuters21578")

    # Iterating over all documents
    for tmp_file in glob("./cleanDocs/*_copy.sgm"):
        # Break if count is set and already reached
        if count != 0 and iteration == count:
            break

        # Parsing xml file
        if isfile(tmp_file):
            tmp_doc = md.parse(tmp_file)

        # Getting all REUTERS elements (articles)
        documents = tmp_doc.getElementsByTagName("REUTERS")

        # Iterating over all articles
        for document in documents:
            if count != 0 and iteration == count:
                break
            # Getting TEXT element
            text = document.getElementsByTagName("TEXT")
            for t in text:
                # Saving article only if it is not BRIEF
                if t.getAttribute("TYPE") != "BRIEF" and t.getAttribute("TYPE") != "UNPROC":
                    tmp_title = document.getElementsByTagName("TITLE")
                    tmp_text = document.getElementsByTagName("BODY")
                    title = md.Element
                    body = md.Element
                    for i in tmp_title:
                        title = i.firstChild.nodeValue.strip()
                    for i in tmp_text:
                        body = i.firstChild.nodeValue.strip()
                    ret_documents[title] = body
                    if len(ret_documents) > iteration:
                        iteration += 1
                elif t.getAttribute("TYPE") == "UNPROC":
                    title = t.firstChild.nodeValue.strip()[:50]
                    body = t.firstChild.nodeValue.strip()
                    ret_documents[title] = body
                    if len(ret_documents) > iteration:
                        iteration += 1

    return ret_documents


def load_data(doc_count : int = 0):
    documents = get_documents(doc_count)
    if not (isfile("data/U.npz") and isfile("data/S.npz") and isfile("data/conceptMatrix.npz")
            and isfile("data/values.npz") and isfile("data/terms.pkl")
            and isfile("data/titles.npz") and isfile("data/texts.pkl")):
        texts = pr.preprocess_data(documents)
        values, terms, titles = pr.get_matrix(texts)
        A = prep.add_term_weights(values)
        U, S, VT = cm.singular_value_decomposition(A)
        conceptMatrix = cm.get_concept_by_document_matrix(S, VT)
        savez_compressed("data/U.npz", U)
        save_npz("data/S.npz", S)
        savez_compressed("data/conceptMatrix.npz", conceptMatrix)
        save_npz("data/values.npz", values)
        with open('data/terms.pkl', 'wb') as f:
            dump(terms, f, DEFAULT_PROTOCOL)
        savez_compressed("data/titles.npz", titles)
        with open('data/texts.pkl', 'wb') as f:
            dump(texts, f, DEFAULT_PROTOCOL)
    else:
        dict_data = load('data/U.npz')
        U = dict_data['arr_0']
        S = load_npz("data/S.npz")
        dict_data = load('data/conceptMatrix.npz')
        conceptMatrix = dict_data['arr_0']
        values = load_npz('data/values.npz')
        with open('data/terms.pkl', 'rb') as f:
            terms = pickle_load(f)
        dict_data = load('data/titles.npz')
        titles = dict_data['arr_0']
        with open('data/texts.pkl', 'rb') as f:
            texts = pickle_load(f)

    return documents, U, S, conceptMatrix, values, terms, titles, texts


def recalculate_lsi(promenna, popup):
    promenna.set("Getting documents")
    popup.update_idletasks()
    documents = get_documents()
    promenna.set("Preprocessing documents")
    popup.update_idletasks()
    texts = pr.preprocess_data(documents)
    promenna.set("Creating DTM")
    popup.update_idletasks()
    values, terms, titles = pr.get_matrix(texts)
    promenna.set("Adding term values")
    popup.update_idletasks()
    A = prep.add_term_weights(values)
    promenna.set("Computing SVD")
    popup.update_idletasks()
    U, S, VT = cm.singular_value_decomposition(A)
    promenna.set("Creating concept by document matrix")
    popup.update_idletasks()
    conceptMatrix = cm.get_concept_by_document_matrix(S, VT)
    promenna.set("Saving new data")
    popup.update_idletasks()
    savez_compressed("data/U.npz", U)
    save_npz("data/S.npz", S)
    savez_compressed("data/conceptMatrix.npz", conceptMatrix)
    save_npz("data/values.npz", values)
    with open('data/terms.pkl', 'wb') as f:
        dump(terms, f, DEFAULT_PROTOCOL)
    savez_compressed("data/titles.npz", titles)
    with open('data/texts.pkl', 'wb') as f:
        dump(texts, f, DEFAULT_PROTOCOL)
