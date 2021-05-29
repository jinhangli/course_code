# -*- coding: utf-8 -*-
# @Time    : 2019-11-15 22:51
# @Author  : jinhang
# @File    : find_title_test.py
from gensim.summarization.bm25 import get_bm25_weights

corpus = [
     ["black", "cat", "white", "cat"],
     ["cat", "outer", "space"],
     ["wag", "dog"]
 ]
result = get_bm25_weights(corpus, n_jobs=-1)
print(result)
