# -*- coding: utf-8 -*-
# @Time    : 2020-08-07 02:00
# @Author  : jinhang
# @File    : statistic_tweet_emoji_number.py

import os
import pandas as pd
import re
import advertools
# setting for display
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('max_colwidth', 100)

id_list_all = list()
emoji_list_all = list()
filename = './data/UserEmojisTweets.csv'
users = pd.read_csv(filename, sep=',', dtype='unicode', index_col=0, lineterminator='\n')
users = users[['author_user_id', 'text']]
users.text.fillna('', inplace=True)
id_list_all.extend(users['author_user_id'])

emoji_summary = advertools.extract_emoji(users.text)
emojis_list = emoji_summary['emoji']
emoji_list_all.extend(emojis_list)

data = pd.DataFrame({'author_user_id': id_list_all,
                     'emoji_list': emoji_list_all})
data.to_csv('tweets_emoji.csv')