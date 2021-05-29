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

def get_mlus(fnames, spkr='*CHI'): ##note use of default val for second arg.
    '''
    get_mlus takes a list of filenames as an argument and returns a
    list of MLU values, one for each file in the list, where each MLU
    is computed based on the utterances of the speaker identified by
    the spkr variable (by default the child). It assumes the file
    format used in the Providence corpus.
    '''
    mlus = []
    for fname in fnames:
        print ('Opening', fname)
        nutts = 0
        ntoks = 0
        with open(fname,'r') as infile:
            for line in infile:
                if line.startswith(spkr): ##this is the only line we changed.
                    line = line.strip()
                    tokens = line.split()
                    assert len(tokens) >= 3 # code will exit if this check fails
                    ntoks += len(tokens)-3
                    nutts += 1
        assert nutts > 0  # code will exit if this check fails
        mlus.append(ntoks/nutts)
    return mlus

def plot_mot_chi_mlus(mot_mlus, chi_mlus, labels):
    '''
    plot_mot_chi_mlus takes a list of MLU values and a list of labels as
    arguments. It makes a line plot of the MLU values, with each
    value labelled on the x-axis with the corresponding label.
    '''
    plt.clf()
    x_pos = range(len(labels))

    plt.subplot(2,1,1)
    plt.plot(x_pos, mot_mlus)
    plt.xticks(x_pos, labels, rotation = 90)
    plt.ylim(0,8)
    plt.ylabel('Mean length of utterance')
    plt.title('Mother MLU')

    plt.subplot(2,1,2)
    plt.plot(x_pos, chi_mlus)
    plt.xticks(x_pos, labels, rotation = 90)
    plt.ylim(0,6)
    plt.ylabel('Mean length of utterance')
    plt.title('Child MLU')

    plt.show()

import sys
if len(sys.argv) < 2:
    print('You must provide at least one filename argument')
    sys.exit(1) #exit program with error code
fnames = sys.argv[1:] #get input arguments from shell command line
short_fnames = [fname[-9:-4] for fname in fnames]

chi_mlus = get_mlus(fnames, '*CHI')
mot_mlus = get_mlus(fnames, '*MOT')
plot_mot_chi_mlus(mot_mlus, chi_mlus, short_fnames)
