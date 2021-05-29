'''
Authors: Henry Thompson, Bharat Ram Ambati, Ida Szubert
Date: 2014-10-01, 2017-10-09
Copyright: This work is licensed under a Creative Commons
Attribution-NonCommercial 4.0 International License
(http://creativecommons.org/licenses/by-nc/4.0/): You may re-use,
redistribute, or modify this work for non-commercial purposes provided
you retain attribution to any previous author(s).
'''

import sys
from pprint import pprint
from collections import defaultdict
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import treebank

import lab5_fix
from lab5_fix import parse_grammar

from nltk.app import rdparser_app as rd


# This function takes a single parsed sentence,
# and prints the parse along with the list of all productions used in it.
def print_parse_info(psent):
    print("\nParsed sentence:\n{}".format(psent))
    print("\nProductions in the sentence:")
    pprint(psent.productions())


def production_distribution(psents):
    """ Creates a frequency distribution of lexical and non-lexical (grammatical) productions
    """
    lexdict = defaultdict(int)
    nonlexdict = defaultdict(int)
    for psent in psents:
        for production in psent.productions():
            if production.is_lexical():
                lexdict[production] += 1
            else:
                nonlexdict[production] += 1
    return lexdict, nonlexdict


def recursive_descent_parser(grammar, sentence, trace=2):
    """ recursive_descent_parser takes grammar and sentence as input and 
    parses the sentence according to the grammar using recursive descent parsing technique.
    
    """
    # Loads the Recursive Descent Parser with the grammar provided
    rdp = nltk.RecursiveDescentParser(grammar, trace=trace)
    # Parses the sentence and outputs a parse tree based on the grammar
    parse = rdp.parse(sentence.split())
    return next(parse)


def app(grammar, sent):
    """ Create a recursive descent parser demo, using a simple grammar and
    text.
    """
    rd.RecursiveDescentApp(grammar, sent.split()).mainloop()


## Main body of code ##

grammar1 = parse_grammar("""
    # Grammatical productions.
     S -> NP VP
     NP -> Pro | Det N | N
     Det -> Art
     VP -> V | V NP | V NP PP
     PP -> Prep NP
   # Lexical productions.
     Pro -> "i" | "we" | "you" | "he" | "she" | "him" | "her"
     Art -> "a" | "an" | "the"
     Prep -> "with" | "in"
     N -> "salad" | "fork" | "mushrooms"
     V -> "eat" | "eats" | "ate" | "see" | "saw" | "prefer" | "sneezed"
     Vi -> "sneezed" | "ran"
     Vt -> "eat" | "eats" | "ate" | "see" | "saw" | "prefer"
     Vp -> "eat" | "eats" | "ate" | "see" | "saw" | "prefer"
    """)

grammar2 = parse_grammar("""
    # Grammatical productions
     S -> NPsg VPsg | NPpl VPpl
     NPpl -> ProPl | Npl | Dpl Npl 
     NPsg -> ProSg | Nsg | Dsg Nsg
     Dpl -> Art
     Dsg -> ArtSg | Art
     VPsg -> Visg | Vtsg NP | Vpsg NP PP
     VPpl -> Vipl | Vtpl NP | Vppl NP PP
     PP -> Prep NP
     NP -> NPsg | NPpl
    # Lexical productions.
     ProSg -> "he" | "she" | "it" | "him" | "her" | "i" | "you"
     ProPl -> "they" | "them" | "we" | "you"
     ArtSg -> "a" | "an"
     Art -> "the"
     Prep -> "with" | "in"
     Nsg -> "salad" | "fork" | "mushroom"
     Npl -> "salads" | "forks" | "mushrooms"
     Visg -> "sneezes"
     Vipl -> "sneeze"
     Vtsg -> "eats" | "ate" | "sees" | "saw" | "prefers"
     Vtpl -> "eat" | "ate" | "see" | "saw" | "prefer"
     Vpsg -> "eats" | "ate" | "sees" | "saw"
     Vppl -> "eat" | "ate" | "see" | "saw"
""")

sentence1 = "he ate salad"
# parse_tree = recursive_descent_parser(grammar1,sentence1,trace=0)
# print_parse_info(parse_tree)
# parse_tree = recursive_descent_parser(grammar1, sentence1)
# parse_tree.draw()
# app(grammar1,sentence1)
# sentence2 = "he ate salad with mushrooms"
# sentence3 = "he ate salad with a fork"

psents = treebank.parsed_sents()
print_parse_info(psents[0])
