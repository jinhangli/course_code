'''
Author: Sharon Goldwater 
Date: 2014-09-01
Copyright: This work is licensed under a Creative Commons
Attribution-NonCommercial 4.0 International License
(http://creativecommons.org/licenses/by-nc/4.0/): You may re-use,
redistribute, or modify this work for non-commercial purposes provided
you retain attribution to any previous author(s).

This file defines the functions used in Lab 2, which can be used to
count words in files, make a Zipf plot or histogram, and compute and
plot MLU.
'''
from __future__ import division
from collections import defaultdict
import sys
import matplotlib.pyplot as plt

##This is a new function that uses list comrehensions to compute MLU
##for a single file
def get_mlu(fname):
    '''
    compute_mlu takes a filename as an argument and returns the MLU of
    the child in that file. It assumes the file format used in the
    Providence corpus.
    '''
    print('Opening', fname)
    with open(fname,'r') as infile:
        lines = infile.readlines()
        lines = [line.strip() for line in lines if line[0:4] == '*CHI']
        nutts = len(lines)
        tokens = [token for line in lines for token in line.split()]
        ntoks = len(tokens) - 3*nutts
    return ntoks/nutts

##This function is identical to the one in lab2-sol.py   
def plot_mlus(mlus, labels):
    '''
    plot_mlus takes a list of MLU values and a list of labels as
    arguments. It makes a line plot of the MLU values, with each
    value labelled on the x-axis with the corresponding label.
    '''
    plt.clf()
    x_pos = range(len(mlus))
    plt.plot(x_pos, mlus)
    plt.xticks(x_pos, labels, rotation = 90)
    plt.ylim(0,6)
    plt.ylabel('Mean length of utterance')
    plt.show()

if len(sys.argv) < 2:
    print('You must provide at least one filename argument')
    sys.exit(1) #exit program with error code
fnames = sys.argv[1:] #get input arguments from shell command line
short_fnames = [fname[-9:-4] for fname in fnames]

##Here is a new line that computes mlus using list comprehension on the new function.
mlus = [get_mlu(fname) for fname in fnames]

plot_mlus(mlus, short_fnames)

