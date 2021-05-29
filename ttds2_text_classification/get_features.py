# -*- coding: utf-8 -*-
# @Time    : 2019-11-14 17:29
# @Author  : jinhang
# @File    : get_features.py

from collections import OrderedDict
import re


def read_tweet(input_path, output_path):

    uni_term_dict = OrderedDict()
    term_id = 1
    with open(input_path, 'rb') as file:
        for line in file:
            line = line.decode('windows-1252')
            if line == '\n' or line == '\r\n':  # Skip empty lines
                continue
            tweet_id, tweet, category = line.strip().split("\t")
            tweet = re.sub(r'https?://[\S]+', '', tweet)  # Remove links from text
            tweet = tweet.lower()   # lower case
            # print(tweet)
            tweet = re.sub(r'[^\w#@]', ' ', tweet)
            tweet = re.sub(r'\brt\b', ' ', tweet)
            # tweet = re.sub(r'\bRT\b', ' ', tweet)
            tweet = tweet.split()
            for term in tweet:
                if term not in uni_term_dict:
                    uni_term_dict[term] = term_id
                    term_id += 1
    # print(term_id)
    with open(output_path, 'w') as f:
        for term in uni_term_dict:
            f.write('{}\t{}\n'.format(term, uni_term_dict[term]))


def convert_features(feat_dic_path, cate_dic_path, input_path, output_path):

    uni_term_dict = OrderedDict()
    class_dict = OrderedDict()

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
    for line in f_input:
        line = line.decode('windows-1252')
        if line == '\n' or line == '\r\n':  # Skip empty lines
            continue
        tweet_id, tweet, category = line.strip().split("\t")
        tweet = re.sub(r'https?://[\S]+', '', tweet)  # Remove links from text
        tweet = tweet.lower()  # lower case
        tweet = re.sub(r'[^\w#@]', ' ', tweet)
        tweet = re.sub(r'\brt\b', ' ', tweet)
        # tweet = re.sub(r'\bRT\b', ' ', tweet)
        tweet = tweet.split()
        features_set = set()
        for term in tweet:
            if term not in uni_term_dict:
                continue
            else:
                features_set.add(int(uni_term_dict[term]))
        features_set = sorted(features_set)
        # print(features_set)
        f_output.write(str(class_dict[category]) + ' ')
        for term_id in features_set:
            f_output.write(str(term_id) + ':1 ')
        f_output.write('#' + str(tweet_id) + '\n')
    f_input.close()
    f_output.close()


if __name__ == "__main__":
    train_path = './data/tweetsclassification/Tweets.14cat.train'
    out_path = './data/feats.dic'
    test_path = './data/tweetsclassification/Tweets.14cat.test'
    read_tweet(train_path, out_path)

    features_path = './data/feats.dic'
    categories_path = './data/classIDs.txt'
    train_out_path = './data/feats.train'
    test_out_path = './data/feats.test'
    convert_features(features_path, categories_path, train_path, train_out_path)
    convert_features(features_path, categories_path, test_path, test_out_path)



