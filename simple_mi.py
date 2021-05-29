# -*- coding: utf-8 -*-
# @Time    : 2020-06-23 00:37
# @Author  : jinhang
# @File    : simple_mi.py
import ast
import pandas as pd
import preprocessing
import numpy as np


word_voc_user_des_non_emoji_path = 'result/descriptions/english_word_vocabulary_user_des_non_emoji.txt'
word_voc_user_des_emoji_path = 'result/descriptions/english_word_vocabulary_user_des_emoji.txt'
word_voc_user_tweet_non_emoji_path = 'result/tweets/english_word_vocabulary_user_tweet_non_emoji.txt'
word_voc_user_tweet_emoji_path = 'result/tweets/english_word_vocabulary_user_tweet_emoji.txt'

with open(word_voc_user_des_non_emoji_path) as f:
    next(f)
    term_frequency_dict = dict([ast.literal_eval(line) for line in f])
vocabulary = set(term_frequency_dict.keys())

with open(word_voc_user_des_emoji_path) as f:
    next(f)
    term_frequency_dict = dict([ast.literal_eval(line) for line in f])
vocabulary.update(set(term_frequency_dict.keys()))

with open(word_voc_user_tweet_non_emoji_path) as f:
    next(f)
    term_frequency_dict = dict([ast.literal_eval(line) for line in f])
vocabulary.update(set(term_frequency_dict.keys()))

with open(word_voc_user_tweet_emoji_path) as f:
    next(f)
    term_frequency_dict = dict([ast.literal_eval(line) for line in f])
vocabulary.update(set(term_frequency_dict.keys()))
vocabulary = list(vocabulary)
vocabulary.sort()
vocabulary = [term for term in vocabulary if term[:1] not in '0123456789']

word_mi_score_data = []
for word in vocabulary:
    word_mi_score_data.append([word, 0.0, 0.0, 0.0, 0.0])
word_score_df = pd.DataFrame(word_mi_score_data, columns=['word', 'score_des_emoji', 'score_des_non_emoji',
                                                          'score_tweet_emoji', 'score_tweet_non_emoji'])
del word_mi_score_data, vocabulary

user_emojis_description_path = "cleaned_data/UserEmojisDescription.csv"
user_without_emojis_description_path = "cleaned_data/UserWithoutEmojisDescription.csv"
user_emojis_tweet_path = "cleaned_data/UserEmojisTweets.csv"
user_without_emojis_tweet_path = "cleaned_data/UserWithoutEmojisTweets.csv"

doc_label_data = []
label_1 = 'des_emoji'
label_2 = 'des_non_emoji'
label_3 = 'tweet_emoji'
label_4 = 'tweet_non_emoji'
labels = [label_1, label_2, label_3, label_4]

des_data = pd.read_csv(user_emojis_description_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
des_data['cleaned_dec'].fillna('', inplace=True)
dec_specific_language_data = des_data[des_data.lang == 'English']
dec_specific_language_data.reset_index(drop=True, inplace=True)
cleaned_des = dec_specific_language_data['cleaned_dec']
for des in cleaned_des:
    hashtags_per, words_per = preprocessing.tokenization_english(des)
    doc_label_data.append([words_per, label_1])

des_data = pd.read_csv(user_without_emojis_description_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
des_data['cleaned_dec'].fillna('', inplace=True)
dec_specific_language_data = des_data[des_data.lang == 'English']
dec_specific_language_data.reset_index(drop=True, inplace=True)
cleaned_des = dec_specific_language_data['cleaned_dec']
for des in cleaned_des:
    hashtags_per, words_per = preprocessing.tokenization_english(des)
    doc_label_data.append([words_per, label_2])
del des_data, dec_specific_language_data, cleaned_des

tweet_data = pd.read_csv(user_emojis_tweet_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
tweet_data['text'].fillna('', inplace=True)
tweet_specific_language_data = tweet_data[tweet_data.lang == 'English']
tweet_specific_language_data.reset_index(drop=True, inplace=True)
cleaned_tweet = tweet_specific_language_data['text']
for tweet in cleaned_tweet:
    hashtags_per, words_per = preprocessing.tokenization_english(tweet)
    doc_label_data.append([words_per, label_3])

tweet_data = pd.read_csv(user_without_emojis_tweet_path, sep=',', dtype='unicode', lineterminator='\n', index_col=0)
tweet_data['text'].fillna('', inplace=True)
tweet_specific_language_data = tweet_data[tweet_data.lang == 'English']
tweet_specific_language_data.reset_index(drop=True, inplace=True)
cleaned_tweet = tweet_specific_language_data['text']
for tweet in cleaned_tweet:
    hashtags_per, words_per = preprocessing.tokenization_english(tweet)
    doc_label_data.append([words_per, label_4])
del tweet_data, tweet_specific_language_data, cleaned_tweet

doc_label_df = pd.DataFrame(doc_label_data, columns=['doc', 'label'])
del doc_label_data
n = len(doc_label_df)

for label in labels:
    score_insert_label = 'score_' + label
    doc_label = doc_label_df[doc_label_df.label == label]
    doc_non_label = doc_label_df[doc_label_df.label != label]

    for i in range(len(word_score_df)):
        print(label + ' ' + str(i))
        word = word_score_df['word'][i]
        n11, n01, n10, n00 = 0, 0, 0, 0
        mi_score = 0.0
        for doc in doc_label.doc:
            if word in doc:
                n11 += 1
            else:
                n01 += 1
        for doc in doc_non_label.doc:
            if word in doc:
                n10 += 1
            else:
                n00 += 1
        n1_ = n10 + n11
        n_1 = n01 + n11
        n0_ = n00 + n01
        n_0 = n00 + n10
        if n11 != 0:
            mi_score += (float(n11) / n) * np.log2(float(n * n11) / (n1_ * n_1))
        if n01 != 0:
            mi_score += (float(n01) / n) * np.log2(float(n * n01) / (n0_ * n_1))
        if n10 != 0:
            mi_score += (float(n10) / n) * np.log2(float(n * n10) / (n1_ * n_0))
        if n00 != 0:
            mi_score += (float(n00) / n) * np.log2(float(n * n00) / (n0_ * n_0))
        word_score_df.at[i, score_insert_label] = mi_score

print(word_score_df)
word_score_df.to_csv('result/descriptions/word_mi_score_original.csv')
