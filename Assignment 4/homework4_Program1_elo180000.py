#############################################################
# File: Homework4_program1_elo180000.py                     #
# Author: Ethan Ong (ELO180000)                             #
# Date: 3/3/2023                                            #
# Purpose: CS 4395 - Homework 4 (N-grams Language Models)   #
#############################################################

import pathlib
import pickle

from nltk import word_tokenize
from nltk.util import ngrams


def ngrams_dict_generator(filepath):
    # Reads file from path
    dataFile = open(pathlib.Path.cwd().joinpath(filepath), encoding='utf-8', mode='r')

    # Removes the newlines
    data = dataFile.read()
    data = data.replace('\n', '')
    text_tokens = word_tokenize(data)

    # Create bigram and unigram
    unigrams = ngrams(text_tokens, 1)
    bigrams = ngrams(text_tokens, 2)

    # Create unigrams and bigrams dictionary sets
    unigram_dict = {}
    for u in set(unigrams):
        unigram_dict[u[0]] = data.count(u[0])
    bigram_dict = {}
    for b in set(bigrams):
            bigram_dict[b[0]] = data.count(b[0])

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    # Calls the files need so it can be pickled
    english_uni_dict, english_bi_dict = ngrams_dict_generator('data/LangId.train.English')
    pickle.dump(english_uni_dict, open('English_Uni_Dict.p', 'wb'))
    pickle.dump(english_bi_dict, open('English_Bi_Dict.p', 'wb'))

    french_uni_dict, french_bi_dict = ngrams_dict_generator('data/LangId.train.French')
    pickle.dump(french_uni_dict, open('French_Uni_Dict.p', 'wb'))
    pickle.dump(french_bi_dict, open('French_Bi_Dict.p', 'wb'))

    italian_uni_dict, italian_bi_dict = ngrams_dict_generator('data/LangId.train.Italian')
    pickle.dump(italian_uni_dict, open('Italian_Uni_Dict.p', 'wb'))
    pickle.dump(italian_bi_dict, open('Italian_Bi_Dict.p', 'wb'))