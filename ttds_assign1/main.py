# -*- coding: utf-8 -*-
# @Time    : 2019-10-17 03:20
# @Author  : jinhang
# @File    : main.py

from search_model import *


if __name__ == "__main__":

    # using below part to retrain the index.txt;
    # here I already store the index.txt, so keep them annotated.
    # if you want to retrain, please add the trec.5000.xml file first in data_documents first
    """
    data_path = "./data_documents/trec.5000.xml"
    path = "./assign_output/index.txt"
    index = generate_index(data_path)
    write_index_to_file(index, path)
    """

    # using below part to search the queries
    # load the existing index
    index_path = "./assign_output/index.txt"
    index, doc_all_ids_set = load_index(index_path)

    # define the query and result path
    boolean_query_path = "./query/queries.boolean.txt"
    ranked_query_path = "./query/queries.ranked.txt"
    boolean_results_path = './assign_output/results.boolean.txt'
    ranked_results_path = './assign_output/results.ranked.txt'

    # load the boolean queries and do the search
    queries = load_query(boolean_query_path)
    boolean_search_results = boolean_search(index, queries, doc_all_ids_set)
    write_results_to_file(boolean_search_results, boolean_results_path, 'boolean')

    # load the ranked queries and do the search
    queries = load_query(ranked_query_path)
    ranked_search_results = ranked_search(index, queries, doc_all_ids_set)
    write_results_to_file(ranked_search_results, ranked_results_path, 'ranked')
