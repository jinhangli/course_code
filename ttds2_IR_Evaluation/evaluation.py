# -*- coding: utf-8 -*-
# @Time    : 2019-11-06 21:59
# @Author  : jinhang
# @File    : evaluation.py
import os
import re
from collections import OrderedDict
import numpy as np


def precision_k(result_dict, rel_doc_dict, k):
    """
    calculate precision with cut-off at rank k, story each query with results at a dict

    :param result_dict: the system results
    :param rel_doc_dict: the relative documents of queries
    :param k:  the cut-off number
    :return: the precision@k results of queries {query_id : precision@k]
    """
    precision_result = OrderedDict()
    for query_id in result_dict:  # for each query
        retrieval_doc_num = 0
        for i, doc in enumerate(result_dict[query_id]):  # for each doc until k
            if i == k:
                break
            doc_id = doc[0]
            if doc_id in rel_doc_dict[query_id]:  # find the right doc
                retrieval_doc_num += 1
        precision_result[query_id] = float(retrieval_doc_num) / float(k)
    return precision_result


def recall_k(result_dict, rel_doc_dict, k):
    """
     calculate recall with cut-off at rank k, story each query with results at a dict

    :param result_dict: the system results
    :param rel_doc_dict: the relative documents of queries
    :param k:  the cut-off number
    :return: the recall@k results of queries {query_id : recall@k]
    """

    recall_result = OrderedDict()
    for query_id in result_dict:  # for each query
        total_rel_doc_num = len(rel_doc_dict[query_id])  # the number of known relevant docs for query
        retrieval_doc_num = 0
        for i, doc in enumerate(result_dict[query_id]):  # for each doc until k
            if i == k:
                break
            doc_id = doc[0]
            if doc_id in rel_doc_dict[query_id]:  # find the right doc
                retrieval_doc_num += 1
        recall_result[query_id] = float(retrieval_doc_num) / float(total_rel_doc_num)
    return recall_result


def r_precision(result_dict, rel_doc_dict):
    """
    calculate r_precision, story each query with results at a dict
    r_precision , means cut-off at length of the known relevant number of the query

    :param result_dict: the system results
    :param rel_doc_dict: the relative documents of queries
    :return: the r-precision results of queries {query_id : r-precision]
    """

    r_precision_result = OrderedDict()
    for query_id in result_dict:  # for each query
        total_rel_doc_num = len(rel_doc_dict[query_id])  # the number of known relevant docs for query
        retrieval_doc_num = 0
        for i, doc in enumerate(result_dict[query_id]):  # for each doc before until relevant doc numbers
            if i == total_rel_doc_num:
                break
            doc_id = doc[0]
            if doc_id in rel_doc_dict[query_id]:  # find the right doc
                retrieval_doc_num += 1
        r_precision_result[query_id] = float(retrieval_doc_num) / float(total_rel_doc_num)
    return r_precision_result


def average_precision(result_dict, rel_doc_dict):
    """
    calculate average precision, story each query with results at a dict

    :param result_dict: the system results
    :param rel_doc_dict: the relative documents of queries
    :return: the average precision results of queries {query_id : AP]
    """
    ap_result = OrderedDict()
    for query_id in result_dict:  # for each query
        sum_precision = 0
        total_rel_doc_num = len(rel_doc_dict[query_id])  # the number of known relevant docs for query
        retrieval_doc_num = 0
        for i, doc in enumerate(result_dict[query_id]):  # for each doc before until relevant doc numbers
            doc_id = doc[0]
            i += 1
            if doc_id in rel_doc_dict[query_id]:  # find the right doc
                retrieval_doc_num += 1
                sum_precision += float(retrieval_doc_num) / float(i)
        ap_result[query_id] = sum_precision / total_rel_doc_num
    return ap_result


def ndcg_k(result_dict, rel_doc_dict, k):
    """
    calculate the nDCG@k, story each query with results at a dict

    :param result_dict: the system results
    :param rel_doc_dict: the system results
    :param k: the cut-off number
    :return: the nDCG@k results of queries {query_id : nDCG@k]
    """
    ndcg_result = OrderedDict()
    for query_id in result_dict:  # for each query
        dcg = 0
        idcg = 0
        for i, doc in enumerate(result_dict[query_id]):  # for each doc before until relevant doc numbers
            if i == k:  # only calculate top k
                break
            doc_id = doc[0]
            if i == 0:  # the first one does not discount
                if doc_id in rel_doc_dict[query_id]:  # find the right doc
                    dcg += rel_doc_dict[query_id][doc_id]  # get the rel value; else keep sum_gain equals 0
            else:  # others do discount
                if doc_id in rel_doc_dict[query_id]:
                    dcg += rel_doc_dict[query_id][doc_id] / float(np.log2(i + 1))
        for i, rel_doc in enumerate(rel_doc_dict[query_id]):
            if i == k:  # only calculate top k
                break
            if i == 0:  # the first one does not discount
                idcg += rel_doc_dict[query_id][rel_doc]
            else:  # others do discount
                idcg += rel_doc_dict[query_id][rel_doc] / float(np.log2(i + 1))
        ndcg_result[query_id] = float(dcg) / idcg
    return ndcg_result


def ir_eval(system_dict, rel_doc_dict, folder_path):
    """
    do the evaluation, and write the results to the files as required

    :param system_dict:  {system_id:{query_id:{[(doc_id,rank)]}}
    :param rel_doc_dict:  {query_id:{doc_id:{relevant value}}
    :param folder_path:  the output path
    :return:
    """
    all_file_path = "/All.eval"
    f_all = open(folder_path + all_file_path, 'w')
    f_all.write('\tP@10\tR@50\tr-Precision\tAP\tnDCG@10\tnDCG@20\n')
    for system_id in system_dict:
        result_dict = system_dict[system_id]
        # do the calculate for each evaluation
        precision_10_dict = precision_k(result_dict, rel_doc_dict, 10)
        recall_50_dict = recall_k(result_dict, rel_doc_dict, 50)
        r_precision_dict = r_precision(result_dict, rel_doc_dict)
        ap_dict = average_precision(result_dict, rel_doc_dict)
        ndcg_10_dict = ndcg_k(result_dict, rel_doc_dict, 10)
        ndcg_20_dict = ndcg_k(result_dict, rel_doc_dict, 20)

        file_path = "/S" + str(system_id) + ".eval"
        f = open(folder_path + file_path, 'w')
        f.write('\tP@10\tR@50\tr-Precision\tAP\tnDCG@10\tnDCG@20\n')
        for query_id in range(1, 11):
            f.write('{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n'.
                    format(query_id, precision_10_dict[query_id],
                           recall_50_dict[query_id],
                           r_precision_dict[query_id],
                           ap_dict[query_id],
                           ndcg_10_dict[query_id],
                           ndcg_20_dict[query_id]))
        f.write(
            '{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n'.
                format("mean", np.mean(list(precision_10_dict.values())),
                       np.mean(list(recall_50_dict.values())),
                       np.mean(list(r_precision_dict.values())),
                       np.mean(list(ap_dict.values())),
                       np.mean(list(ndcg_10_dict.values())),
                       np.mean(list(ndcg_20_dict.values()))))
        f.close()

        f_all.write('{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n'.
                    format("S" + str(system_id), np.mean(list(precision_10_dict.values())),
                           np.mean(list(recall_50_dict.values())),
                           np.mean(list(r_precision_dict.values())),
                           np.mean(list(ap_dict.values())),
                           np.mean(list(ndcg_10_dict.values())),
                           np.mean(list(ndcg_20_dict.values()))))

    f_all.close()
    return None


def get_input_files(path):
    """
    deal with the input data, turn it to convenient data structure
        {system_id:{query_id:{[(doc_id,rank)]}}}
        {query_id:{doc_id:{relevant value}}}
    :param path: the folder path which contains the results and documents file
    :return: the data structure which contains the information of results and documents
    """
    files_name = os.listdir(path)
    files_name.remove('qrels.txt')
    files_name.sort()
    system_dict = OrderedDict()  # {system_id:{query_id:{[(doc_id,rank)]}}
    rel_doc_dict = OrderedDict()  # {query_id:{doc_id:{relevant value}}

    for filename in files_name:  # read each system results by order
        system_id = int(filename.split('.')[0][1:])
        system_dict[system_id] = OrderedDict()
        result_dict = system_dict[system_id]
        with open(path + '/' + filename, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                line = line.strip().split()
                query_id = int(line[0])
                doc_id = int(line[2])
                rank = int(line[3])
                if query_id not in result_dict:  # initiate the result_dict
                    result_dict[query_id] = list()
                result_dict[query_id].append((doc_id, rank))

    with open(path + '/qrels.txt', 'r') as f:  # read relative documents
        for line in f:
            if line == '\n':
                continue
            line = line.strip().split(':')
            query_id = int(line[0].strip())
            docs = line[1].strip()
            docs = re.findall(r'[(](.*?)[)]', docs)  # find each doc and rank in the brackets
            if query_id not in rel_doc_dict:
                rel_doc_dict[query_id] = OrderedDict()
            for id_value in docs:
                id_value = id_value.split(',')
                doc_id = int(id_value[0])
                value = int(id_value[1])
                rel_doc_dict[query_id][doc_id] = value

    return system_dict, rel_doc_dict


if __name__ == "__main__":
    input_path = './systems'
    output_path = './output'
    results, documents = get_input_files(input_path)
    ir_eval(results, documents, output_path)
