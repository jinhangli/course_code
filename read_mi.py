# -*- coding: utf-8 -*-
# @Time    : 2020-06-28 19:53
# @Author  : jinhang
# @File    : read_mi.py
import pandas as pd
import emoji
import plotly.graph_objects as go
import pandas as pd
import ast
from collections import OrderedDict
# setting for display
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)


def mi_score_sort_emoji(path, on, number):
    score = pd.read_csv(path, sep=',', index_col=0)
    score.sort_values(by=[on], ascending=False, inplace=True)
    score.reset_index(drop=True, inplace=True)
    for i in range(len(score[:number])):
        print(i+1)
        print(score['word'][i], score[on][i])
        print(emoji.demojize(score['word'][i]))
        print(score['word'][i].encode("unicode_escape"))
        print('-----')


def mi_score_sort_word(path, on, number):
    score = pd.read_csv(path, sep=',', index_col=0)
    score.sort_values(by=[on], ascending=False, inplace=True)
    score.reset_index(drop=True, inplace=True)
    print(score[:number])
    for i in range(len(score[:number])):
        print(i+1)
        print(score['word'][i], score[on][i])
        print('-----')


if __name__ == '__main__':

    '''emoji language mi score'''
    # path = 'result/emoji_language_top4_des_mi_score_original.csv'
    path_2 = 'result/language_x_emoji_top4_des_mi_score.csv'
    # mi_score_sort_emoji(path, on='score_English', number=20)
    mi_score_sort_emoji(path_2, on='score_Japanese', number=20)
    # mi_score_sort_emoji(path, on='score_Spanish', number=10)
    # mi_score_sort_emoji(path, on='score_Portuguese', number=10)

    # emoji_user_des_non_emoji_path = 'result/descriptions/emoji_vocabulary_user_des_emoji.txt'
    # with open(emoji_user_des_non_emoji_path) as f:
    #     next(f)
    #     term_frequency_dict = OrderedDict([ast.literal_eval(line) for line in f])
    # top_emoji_list = list(term_frequency_dict.keys())[:5]
    # for i in top_emoji_list:
    #     print(i)
    #     print(emoji.demojize(i))
    #     print(i.encode("unicode_escape"))

    '''token top emoji mi score'''
    # path_top_emoji = 'result/top_emoji_x_token_5_mi_score.csv'
    # mi_score_sort_word(path_top_emoji, on='score_2', number=40)

    # path_token_emoji = 'result/word_mi_score_original.csv'
    # mi_score_sort_word(path_token_emoji, on='score_des_emoji', number=40)
    # mi_score_sort_word(path_token_emoji, on='score_des_non_emoji', number=50)
    # mi_score_sort_word(path_token_emoji, on='score_tweet_non_emoji', number=100)
    # mi_score_sort_word(path_token_emoji, on='score_tweet_emoji', number=200)
