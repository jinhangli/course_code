# -*- coding: utf-8 -*-
# @Time    : 2019-10-11 00:06
# @Author  : jinhang
# @File    : data_preprocess.py

from nltk.stem.porter import *
import xml.etree.ElementTree as ET
import re


def case_folding(text):
    """
    make the characters in document and queries be lower case

    :param text: input characters
    :return: lower case characters
    """
    text = text.lower()
    return text


def tokenisation(text):
    """
    get tokens from text, just split on every non-letter and non-digit character

    :param text: can be document or queries in ranked query
    :return: get tokens
    """
    text = re.sub('[^\w\d]', ' ', text)
    text = text.split()
    return text


def stopping(tokens):
    """
    remove the stop words in tokens

    :param tokens: the tokens got from tokenisation function
    :return: tokens without stop words
    """
    stopwords = set()
    with open('./data_documents/englishST.txt') as f:
        for line in f:
            stopwords.add(line.strip('\n'))
    tokens = [x for x in tokens if x not in stopwords]
    return tokens


def stemming(token_list):
    """
    change the tokens into stem form

    :param token_list: the tokens got from stopping
    :return: tokens with stem form
    """
    stemmer = PorterStemmer()
    norm_tokens = [stemmer.stem(token) for token in token_list]
    return norm_tokens


def parse_xml(xml_path):
    """
    parse xml file, adding the header <roots> and footer </roots> to the file first!

    :param xml_path: the path of collection
    :return: a dict {doc_id: doc_headline + doc_content}
    """
    global doc_id, doc_text
    tree = ET.parse(xml_path)
    root = tree.getroot()
    doc = dict()
    for child in root:  # each child = each doc
        doc_headline = ''  # in case that no headline, set headline as empty string beforehand
        for node in child:
            if node.tag == 'DOCNO':
                doc_id = node.text
            if node.tag == 'HEADLINE':
                doc_headline = node.text.strip('\n')
            if node.tag == 'TEXT' or node.tag == 'Text':
                doc_text = node.text
        doc_content = doc_headline + doc_text  # put doc_headline and doc_text together
        doc[doc_id] = doc_content
    return doc
