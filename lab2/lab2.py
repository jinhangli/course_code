'''
Author: Sharon Goldwater 
Date: 2014-09-01, updated 2017-09-15 for Python 3
Copyright: This work is licensed under a Creative Commons
Attribution-NonCommercial 4.0 International License
(http://creativecommons.org/licenses/by-nc/4.0/): You may re-use,
redistribute, or modify this work for non-commercial purposes provided
you retain attribution to any previous author(s).

This file defines the functions used in Lab 2, which can be used to
count words in files, make a Zipf plot or histogram, and compute and
plot MLU.
'''

#This line imports a special data type called defaultdict, which you
#can use like a dictionary except that it assigns a default value to
#any item that has not yet been accessed/assigned. To use it, you need
#to provide the data type that will be stored in the defaultdict, so
#that it knows what default value to use.  We will store integers,
#which have default value 0.
from collections import defaultdict

#This line allows us to use various plotting functions (see code)
import matplotlib.pyplot as plt

def get_word_counts(fnames):
    '''
    get_word_counts takes a list of filenames (strings) as arguments
    and returns a defaultdict which contains the count of each unique
    word in those files. The current implementation only counts words
    spoken by the mother, and assumes the files will be formatted as
    in the Providence corpus of CHILDES.
    '''
    word_counts = defaultdict(int) #defaultdict of integers (see note above)
    for fname in fnames:
        print('Opening ', fname)
        with open(fname,'r') as infile:
            for line in infile:
                if line[0:4] == '*MOT': #look for lines spoken by mother
                    line = line.strip() #strip off any leading or final whitespace
                    tokens = line.split() #get a list of the word tokens (split on whitespace)
                    for tok in tokens:
                        word_counts[tok] += 1 #add count to dictionary. 
                        # note that word_counts[tok] will default to 0
                        # if not previously accessed because we used a
                        # defaultdict.
    return word_counts

def zipf_plot(word_counts, maxRank=0):
    '''
    zipf_plot takes a dictionary of word counts as an argument and
    makes a two scatter plots of the rank vs. frequency of words (aka
    Zipf plots). One plot has log-log axes, the other does not.  The
    second (optional) argument can be used to plot only the top ranked
    words (up to maxRank). If maxRank is 0 (the default), all words
    will be plotted.
    '''
    #We will use the 'plot' function of matplotlib to create a scatter
    #plot. 'plot' requires two lists, X and Y, as its two required
    #arguments, corresponding to the x positions and y positions of
    #the data points, and will plot points at (X[0], Y[0]),
    #(X[1],Y[1]), etc. Here we want to plot rank versus frequency, so
    #X should be the ranks, and Y should be the frequencies at each
    #rank. The third (optional) argument to 'plot' specifies the color
    #and style of the data points (or lines) to use. Here we use black
    #('k') dots ('.')

    #Note: All the functions preceded by 'plt' come from the
    #matplotlib library. There are actually two interfaces for this
    #library - the one we use here looks a lot like Matlab, which some
    #people may already be familiar with. There is also a more
    #object-oriented interface which you can look up if interested but
    #we won't use it here.

    num_wds = len(word_counts) # total number of word types
    #First make the list of sorted frequencies
    sorted_counts = sorted(word_counts.values(), reverse=True)
    # Now make the list of ranks, which is just the list of
    # integers from 1 to the number of words.
    x_pos = range(1, num_wds+1) # gives a list from 1 to (number of words)
    if maxRank > 0: #only plot words up to rank maxRank
        x_pos = x_pos[:maxRank]
        sorted_counts = sorted_counts[:maxRank]
    #the following commands create the plots
    plt.clf() # clear previous plots (if any)
    plt.subplot(1,2,1) #specify the first plot in a 1x2 set of plots
    plt.plot(x_pos, sorted_counts, 'k.') # create the scatter plot

    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.title('Words from *MOT utterances, linear axes')
    
    plt.subplot(1,2,2) #specify the second plot in a 1x2 set of plots
    plt.xscale('log') #set x axis to log scale. Must do *before* creating plot
    plt.yscale('log') #set y axis to log scale. 
    plt.plot(x_pos, sorted_counts, 'k.') # create the scatter plot
    plt.xlabel('Rank')
    plt.ylabel('Frequency')
    plt.title('Words from *MOT utterances, log axes')
    plt.show() #display the set of plots

def get_mlus(fnames):
    '''
    get_mlus takes a list of filenames as an argument and returns a
    list of MLU values, one for each file in the list, where each MLU
    is computed based on the child's utterances in the file. It
    assumes the file format used in the Providence corpus.
    '''
    mlus = []
    for fname in fnames:
        print('Opening ', fname)
        nutts = 0
        ntoks = 0
        with open(fname,'r') as infile:
            for line in infile:
                if line[0:4] == '*CHI': # alternatively: if line.startswith('*CHI'):
                    line = line.strip()
                    tokens = line.split()
                    assert len(tokens) >= 3 # code will exit if this check fails
                    ntoks += len(tokens)-3
                    nutts += 1
        assert nutts > 0  # code will exit if this check fails
        mlus.append(ntoks/nutts)
    return mlus

def plot_mlus(mlus, labels):
    '''
    plot_mlus takes a list of MLU values and a list of labels as
    arguments. It makes a line plot of the MLU values, with each
    value labelled on the x-axis with the corresponding label.
    '''
    plt.clf()
### students must fill in the rest

### to here.
    plt.show()


#### main body of code ####

import sys
if len(sys.argv) < 2:
    print('You must provide at least one filename argument')
    sys.exit(1) #exit program with error code
fnames = sys.argv[1:] #get input arguments from shell command line


###for first part of lab

word_counts = get_word_counts(fnames)
zipf_plot(word_counts)

###for second part of lab

# next line uses a 'list comprehension' which is covered later in CPSLP.
short_fnames = [fname[-9:-4] for fname in fnames] 
### fill in below to generate MLU plots:
