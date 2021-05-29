# -*- coding: utf-8 -*-
# @Time    : 2019-11-16 16:47
# @Author  : jinhang
# @File    : xgboost_improvement.py

# -*- coding: utf-8 -*-
# @Time    : 2019-11-14 17:29
# @Author  : jinhang
# @File    : get_features.py

from collections import OrderedDict
import re
import xgboost as xgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier


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
            tweet = re.sub(r'\bRT\b', ' ', tweet)
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
    # f_output = open(output_path, 'w')
    feature_matrix = []
    y_list = []
    for line in f_input:
        line = line.decode('windows-1252')
        if line == '\n' or line == '\r\n':  # Skip empty lines
            continue
        tweet_id, tweet, category = line.strip().split("\t")
        tweet = re.sub(r'https?://[\S]+', '', tweet)  # Remove links from text
        tweet = tweet.lower()  # lower case
        tweet = re.sub(r'[^\w#@]', ' ', tweet)
        tweet = re.sub(r'\brt\b', ' ', tweet)
        tweet = re.sub(r'\bRT\b', ' ', tweet)
        tweet = tweet.split()
        # features_set = set()
        features_list = []
        for term in uni_term_dict:
            if term in tweet:
                feature = 1
            else:
                feature = 0
            features_list.append(feature)
        assert len(features_list) == len(uni_term_dict)
        feature_matrix.append(features_list)
        y_list.append(str(class_dict[category]))
    f_input.close()
    return feature_matrix, y_list
    # f_output.close()


def xgb_improvement(x_train, y_train, x_test, y_test):

    x_train = np.array(x_train)
    x_test = np.array(x_test)
    model = xgb.XGBClassifier(max_depth=5, learning_rate=0.1, n_estimators=1000, seed=0, objective='multi:softmax')
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    average_accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    print('average accuracy: {}'.format(average_accuracy))
    print('macro f1: {}'.format(macro_f1))


def decision_tree_improvement(x_train, y_train, x_test, y_test):

    x_train = np.array(x_train)
    x_test = np.array(x_test)
    clf = DecisionTreeClassifier(random_state=0)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    average_accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    print('average accuracy: {}'.format(average_accuracy))
    print('macro f1: {}'.format(macro_f1))


def random_forest_improvement(x_train, y_train, x_test, y_test):

    x_train = np.array(x_train)
    x_test = np.array(x_test)
    model = RandomForestClassifier(n_estimators=1000, random_state=0, n_jobs=-1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    average_accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    print('average accuracy: {}'.format(average_accuracy))
    print('macro f1: {}'.format(macro_f1))


def naive_bayes_improvement(x_train, y_train, x_test, y_test):

    x_train = np.array(x_train)
    x_test = np.array(x_test)
    clf = MultinomialNB()
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    average_accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    print('average accuracy: {}'.format(average_accuracy))
    print('macro f1: {}'.format(macro_f1))


if __name__ == "__main__":
    train_path = './data/tweetsclassification/Tweets.14cat.train'
    out_path = './data/feats.dic'
    test_path = './data/tweetsclassification/Tweets.14cat.test'
    read_tweet(train_path, out_path)

    features_path = './data/feats.dic'
    categories_path = './data/classIDs.txt'
    train_out_path = './data/feats.train'
    test_out_path = './data/feats.test'
    train_matrix, y_train = convert_features(features_path, categories_path, train_path, train_out_path)
    test_matrix, y_test = convert_features(features_path, categories_path, test_path, test_out_path)
    # xgb_improvement(train_matrix, y_train, test_matrix, y_test)
    # decision_tree_improvement(train_matrix, y_train, test_matrix, y_test)
    # random_forest_improvement(train_matrix, y_train, test_matrix, y_test)
    naive_bayes_improvement(train_matrix, y_train, test_matrix, y_test)




