# -*- coding: utf-8 -*-
# @Time    : 2019-11-15 00:45
# @Author  : jinhang
# @File    : improvement.py

from collections import OrderedDict
import re
from get_features import convert_features
from nltk.stem.porter import *
from nltk.corpus import stopwords
import urllib
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfTransformer


def read_tweet(input_path, output_path):
    uni_term_dict = OrderedDict()
    term_id = 1
    stop_words = set(stopwords.words('english'))
    with open(input_path, 'rb') as file:
        for line in file:
            line = line.decode('windows-1252')
            if line == '\n' or line == '\r\n':  # Skip empty lines
                continue
            tweet_id, tweet, category = line.strip().split("\t")

            # add line title
            pattern = re.compile(r'https?://[\S]+')  # find url
            link_list = pattern.findall(tweet)
            if len(link_list) != 0:
                for i in range(len(link_list)):
                    link = link_list[i]
                    try:
                        url = urllib.request.urlopen(link, timeout=1).read()
                        html = BeautifulSoup(url)
                        title = html.title.string
                        if title is None:
                            title = ''
                        print(title)
                    except:
                        title = ''
                    tweet = tweet + ' ' + title

            # baseline features
            tweet = re.sub(r'https?://[\S]+', '', tweet)  # Remove links from text
            tweet = tweet.lower()  # lower case
            tweet = re.sub(r'[^\w#@]', ' ', tweet)
            tweet = re.sub(r'\brt\b', ' ', tweet)
            tweet = tweet.split()
            # print(tweet)

            # double hashtags
            double_hashtags_tweet = list()
            for token in tweet:
                match_type = re.match(r'#\w+', token)
                if match_type is not None:
                    match = match_type.group()
                    double_hashtags_tweet.append(token)
                    double_hashtags_tweet.append(match[1:])
                else:
                    double_hashtags_tweet.append(token)
            # print(double_hashtags_tweet)
            tweet = double_hashtags_tweet

            # Remove stopwords
            tweet = [x for x in tweet if x not in stop_words]

            # stem
            stemmer = PorterStemmer()
            tweet = [stemmer.stem(token) for token in tweet]

            for term in tweet:
                if term not in uni_term_dict:
                    uni_term_dict[term] = term_id
                    term_id += 1

    with open(output_path, 'w') as f:
        for term in uni_term_dict:
            f.write('{}\t{}\n'.format(term, uni_term_dict[term]))


def convert_features_changed(feat_dic_path, cate_dic_path, input_path, output_path, tfidf_path):
    uni_term_dict = OrderedDict()
    class_dict = OrderedDict()
    stop_words = set(stopwords.words('english'))

    with open(feat_dic_path, 'r') as f:
        for line in f:
            term, term_id = line.strip().split("\t")
            uni_term_dict[term] = term_id

    with open(cate_dic_path, 'r') as f:
        for line in f:
            category, cate_id = line.strip().split('\t')
            class_dict[category] = cate_id

    f_input = open(input_path, 'rb')
    f_output = open(output_path, 'w')
    # feature_matrix = []
    for line in f_input:
        line = line.decode('windows-1252')
        if line == '\n' or line == '\r\n':  # Skip empty lines
            continue
        tweet_id, tweet, category = line.strip().split("\t")

        # # presence of link
        # presence_link = 0
        # pattern = re.compile(r'https?://[\S]+')  # find url
        # link_list = pattern.findall(tweet)
        # if len(link_list) != 0:
        #     presence_link = 1


        # add line title
        pattern = re.compile(r'https?://[\S]+')  # find url
        link_list = pattern.findall(tweet)
        if len(link_list) != 0:
            for i in range(len(link_list)):
                link = link_list[i]
                try:
                    url = urllib.request.urlopen(link, timeout=1).read()
                    html = BeautifulSoup(url)
                    title = html.title.string
                    if title is None:
                        title = ''
                    print(title)
                except:
                    title = ''
                tweet = tweet + ' ' + title

        # baseline features
        tweet = re.sub(r'https?://[\S]+', '', tweet)  # Remove links from text
        tweet = tweet.lower()
        tweet = re.sub(r'[^\w#@]', ' ', tweet)
        tweet = re.sub(r'\brt\b', ' ', tweet)
        tweet = tweet.split()

        # double hashtags
        double_hashtags_tweet = list()
        for token in tweet:
            match_type = re.match(r'#\w+', token)
            if match_type is not None:
                match = match_type.group()
                double_hashtags_tweet.append(token)
                double_hashtags_tweet.append(match[1:])
            else:
                double_hashtags_tweet.append(token)
        
        # print(double_hashtags_tweet)
        tweet = double_hashtags_tweet

        # baseline features
        tweet = [x for x in tweet if x not in stop_words]

        # stem
        stemmer = PorterStemmer()
        tweet = [stemmer.stem(token) for token in tweet]

    #     features_list = []
    #     for term in uni_term_dict:
    #         feature = tweet.count(term)
    #         features_list.append(feature)
    #     assert len(features_list) == len(uni_term_dict)
    #     feature_matrix.append(features_list)
    # # print(len(feature_matrix))
    # # print(len(feature_matrix[0]))

        features_set = set()
        for term in tweet:
            if term not in uni_term_dict:
                continue
            else:
                features_set.add(int(uni_term_dict[term]))
        features_set = sorted(features_set)
        f_output.write(str(class_dict[category]) + ' ')
        for term_id in features_set:
            f_output.write(str(term_id) + ':1 ')

        # # feature length
        # feature_length = len(features_set)
        # f_output.write(str(len(uni_term_dict)+1) + ':' + str(feature_length) + ' ')
        #
        # # presence of hashtags
        # presence_hashtags = 0
        # for token in tweet:
        #     match_type = re.match(r'#\w+', token)
        #     if match_type is not None:
        #         presence_hashtags = 1
        #         break
        # f_output.write(str(len(uni_term_dict)+2) + ':' + str(presence_hashtags) + ' ')
        #
        # f_output.write(str(len(uni_term_dict)+3) + ':' + str(presence_link) + ' ')

        f_output.write('#' + str(tweet_id) + '\n')

    f_input.close()
    f_output.close()

'''
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(feature_matrix)
    tfidf_scores = tfidf.toarray()
    f_feats = open(output_path, 'r')
    f_out = open(tfidf_path, 'w')
    i = 0
    for line in f_feats:
        line = line.split()
        # print(line)
        class_id = line[0]
        doc_id = line[-1]
        line = line[1:-1]
        f_out.write(class_id + ' ')
        for item in line:
            term, score = item.split(':')
            term = int(term) - 1
            score = tfidf_scores[i][term]
            assert score != 0
            f_out.write(str(term + 1) + ':' + str(score) + ' ')
        i += 1
        f_out.write(str(doc_id) + '\n')
    assert i == len(feature_matrix)
    f_out.close()
'''

if __name__ == "__main__":
    train_path = './data/tweetsclassification/Tweets.14cat.train'
    out_path = './data_improved/feats.dic'
    test_path = './data/tweetsclassification/Tweets.14cat.test'
    read_tweet(train_path, out_path)

    features_path = './data_improved/feats.dic'
    categories_path = './data/classIDs.txt'
    train_out_path = './data_improved/feats.train'
    test_out_path = './data_improved/feats.test'
    tfidf_train = './feats.train'
    tfidf_test = './feats.test'
    convert_features_changed(features_path, categories_path, train_path, train_out_path, tfidf_train)
    convert_features_changed(features_path, categories_path, test_path, test_out_path, tfidf_test)
