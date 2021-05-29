# -*- coding: utf-8 -*-
# @Time    : 2019-11-14 22:06
# @Author  : jinhang
# @File    : evaluation.py
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support as score


def classification_evaluation(pred_path, truth_path, output_path):
    y_pred = []
    y_true = []
    distinct_classes = set()
    with open(pred_path, 'r') as file:
        for line in file:
            pred_y = line.strip().split(' ')[0]
            y_pred.append(pred_y)
    with open(truth_path, 'r') as file:
        for line in file:
            truth_y = line.strip().split(' ')[0]
            y_true.append(truth_y)
            distinct_classes.add(int(truth_y))
    distinct_classes = list(distinct_classes)
    for i in range(len(distinct_classes)):
        distinct_classes[i] = str(distinct_classes[i])

    average_accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average='macro')
    print('average accuracy: {}'.format(average_accuracy))
    print('macro f1: {}'.format(macro_f1))
    precision, recall, fscore, support = score(y_true, y_pred, labels=list(distinct_classes))

    print('for each classes as below:')
    print(distinct_classes)
    print('precision: {}'.format(precision))
    print('recall: {}'.format(recall))
    print('f_1 score: {}'.format(fscore))

    with open(output_path, 'w') as f:
        f.write('Accuracy = {:.3f}\n'.format(average_accuracy))
        f.write('Macro-F1 = {:.3f}\n'.format(macro_f1))
        f.write('Results per class:\n')
        for i in range(len(distinct_classes)):
            f.write('{}: P={:.3f} R={:.3f} F={:.3f}\n'.format(i, precision[i], recall[i], fscore[i]))


if __name__ == "__main__":
    pred_path = './pred.out'
    truth_path = './feats.test'
    output_path = './data_improved/Eval.txt'
    classification_evaluation(pred_path, truth_path, output_path)
