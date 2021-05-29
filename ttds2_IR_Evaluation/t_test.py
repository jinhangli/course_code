# -*- coding: utf-8 -*-
# @Time    : 2019-11-14 16:46
# @Author  : jinhang
# @File    : t_test.py

from scipy.stats import ttest_ind


# there are for pair of system need to calculate the p_value

recall_50_first_s2 = [0.667, 1, 1, 0.875, 0.429, 1, 1, 1, 0.9, 0.8]
recall_50_second_s1 = [0.667, 1, 1, 0.875, 0.429, 1, 0.667, 1, 0.9, 0.8]

ap_first_s3 = [0.518, 0.75, 0.056, 0.69, 0.104, 0.465, 0, 1, 0.756, 0.174]
ap_second_s6 = [0.56, 0.615, 0.056, 0.69, 0.104, 0.465, 0, 1, 0.784, 0.174]

ndcg_10_first_s3 = [0.66, 0.832, 0, 0.684, 0.233, 0.132, 0, 0.78, 0.464, 0.417]
ndcg_10_second_s6 = [0.646, 0.695, 0, 0.622, 0.233, 0.132, 0, 0.722, 0.533, 0.417]

ndcg_20_first_s3 = [0.733, 0.897, 0.24, 0.704, 0.233, 0.449, 0, 0.78, 0.584, 0.488]
ndcg_20_second_s6 = [0.719, 0.759, 0.24, 0.652, 0.233, 0.449, 0, 0.722, 0.641, 0.488]

t_statistic_recall, p_value_recall = ttest_ind(recall_50_first_s2, recall_50_second_s1, equal_var=False)
print('recall_50: {}'.format(p_value_recall))

t_statistic_ap, p_value_ap = ttest_ind(ap_first_s3, ap_second_s6, equal_var=False)
print('ap: {}'.format(p_value_ap))

t_statistic_ndcg_10, p_value_ndcg_10 = ttest_ind(ndcg_10_first_s3, ndcg_10_second_s6, equal_var=False)
print('ndcg_10: {}'.format(p_value_ndcg_10))

t_statistic_ndcg_20, p_value_ndcg_20 = ttest_ind(ndcg_20_first_s3, ndcg_20_second_s6, equal_var=False)
print('ndcg_20: {}'.format(p_value_ndcg_20))

