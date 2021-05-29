# -*- coding: utf-8 -*-
# @Time    : 2019-10-13 19:18
# @Author  : jinhang
# @File    : positional_inverted_index.py

from data_preprocess import *
from collections import OrderedDict


def generate_index(path):
    """
    get positional inverted index dict: get preprocessed tokens,
    then record them positions in the documents of the collection

    :param path: the path of the collection
    :return: positional inverted index dict
    """
    index = dict()  # {term: OrderedDict{doc_id: [positions]}}
    doc = parse_xml(path)
    for doc_id in doc:  # process every doc
        terms = stemming(stopping(tokenisation(case_folding(doc[doc_id]))))
        position = 0
        for term in terms:  # process every term occur in one doc
            position += 1
            if term not in index:  # initialization
                index[term] = OrderedDict()
            if doc_id not in index[term]:
                index[term][doc_id] = list()
            index[term][doc_id].append(position)  # append position
    return index


def write_index_to_file(index, path):
    """
    write the index into a file, which will accelerate the search model by using the index in the disk

    :param index: the index dict data structure
    :param path: the path of disk to store the positional inverted index
    :return:
    """
    with open(path, 'w') as f:
        for term in sorted(index.keys()):  # sorted alphabetically
            f.writelines(term + ':\n')     # write the file
            for doc_dict in index[term]:
                f.writelines('\t' + doc_dict + ': ' + ",".join(str(i) for i in index[term][doc_dict]) + '\n')
            f.writelines('\n')
    return None
