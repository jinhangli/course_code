# -*- coding: utf-8 -*-
# @Time    : 2019-07-29 17:33
# @Author  : jinhang
# @File    : split_by_time.py

"""
生成trans 训练数据
先用test数据集测试
按时间进行切割（如果数据量大可以考虑取样训练）
"""

import pandas as pd


def split_train_test(df: pd.DataFrame):
    train_max_time = 1382400-24*3600
    train_df = df.loc[df['timestamp'] < train_max_time, :]
    test_df = df.loc[df['timestamp'] >= train_max_time, :]
    return train_df, test_df


data = pd.read_csv('./CIKM2_data/user_behavior.csv', names=['user', 'item', 'behavior', 'timestamp'])
train_df, test_df = split_train_test(data)
test_df.to_csv('./CIKM2_data/user_behavior_test.csv', sep='\t', header=None, index=None)
train_df.to_csv('./CIKM2_data/user_behavior_train.csv', sep='\t', header=None, index=None)

data = train_df[['user', 'item', 'behavior']]
data.drop_duplicates(inplace=True)
data.reset_index(drop=True, inplace=True)
data_ori = data.copy()

user = data['user']
user.drop_duplicates(inplace=True)  # 去重user 49,896
user.reset_index(drop=True, inplace=True)
user_entity = pd.DataFrame()
user_entity['name'] = user
user_entity['id'] = list(user.index)

item = data.item
item.drop_duplicates(inplace=True)  # 去重item 931,394
item.reset_index(drop=True, inplace=True)
item.index = item.index + len(user)
item_entity = pd.DataFrame()
item_entity['name'] = item
item_entity['id'] = list(item.index)

print(len(user_entity), len(item_entity))
data_entity = user_entity.append(item_entity,ignore_index=True)  # user和item的ID名存在重复，所以要分别转换成trans_id，前面user,后面是item
# 生成entity2id.txt
data_entity.to_csv('./CIKM2_data/test_split/entity2id.txt', sep='\t', header=[str(len(data_entity)), ''], index=None)

data_relation = pd.DataFrame()
data_relation['name'] = ['pv', 'buy', 'cart', 'fav']
data_relation['id'] = list(data_relation.index)
# 生成relation2id.txt
data_relation.to_csv('./CIKM2_data/test_split/relation2id.txt', sep='\t', header=[str(len(data_relation)), ''], index=None)

# 用映射的方法生成trans要求输入的三元组格式
dict_user = dict(user_entity['name'].items())
dict_user = dict(zip(dict_user.values(), dict_user.keys()))
dict_item = dict(item_entity['name'].items())
dict_item = dict(zip(dict_item.values(), dict_item.keys()))
dict_behavior = dict(data_relation['name'].items())
dict_behavior = dict(zip(dict_behavior.values(), dict_behavior.keys()))

data_ori['user'] = data_ori['user'].map(dict_user)
data_ori['item'] = data_ori['item'].map(dict_item)
data_ori['behavior'] = data_ori['behavior'].map(dict_behavior)

data_ori = data_ori.sample(frac=1).reset_index(drop=True)  # 划分为train/valid/test 按8：1：1划分
train = data_ori[0:int(0.8 * len(data_ori))]
valid = data_ori[int(0.8 * len(data_ori)):int(0.9 * len(data_ori))]
test = data_ori[int(0.9 * len(data_ori)):]
train.to_csv('./CIKM2_data/test_split/train2id.txt', sep='\t', header=[str(len(train)), '', ''], index=None)
valid.to_csv('./CIKM2_data/test_split/valid2id.txt', sep='\t', header=[str(len(valid)), '', ''], index=None)
test.to_csv('./CIKM2_data/test_split/test2id.txt', sep='\t', header=[str(len(test)), '', ''], index=None)

print(len(data_entity), len(train), len(valid), len(test))
# 981290 2208384 276048 276049

