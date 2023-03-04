#############################################################
# File: Homework4_program2_elo180000.py                     #
# Author: Ethan Ong (ELO180000)                             #
# Date: 3/3/2023                                            #
# Purpose: CS 4395 - Homework 4 (N-grams Language Models)   #
#############################################################

import pickle

from nltk import word_tokenize
from nltk.util import ngrams


# Function to calculate the probability of each language
def compute_probability(line, dict_unigram, dict_bigram, V):
    probability = 1
    for bigram in line:
        if bigram in dict_bigram:
            bi = dict_bigram[bigram]
        else:
            bi = 0
        if bigram[0] in dict_unigram:
            uni = dict_unigram[bigram[0]]
        else:
            uni = 0
        probability = probability * ((bi + 1) / (uni + V))

    return probability


if __name__ == '__main__':
    # Reads the pickle files from program 1
    english_bigram = pickle.load(open('English_Bi_Dict.p', 'rb'))
    enlgish_unigram = pickle.load(open('English_Uni_Dict.p', 'rb'))

    french_bigram = pickle.load(open('French_Bi_Dict.p', 'rb'))
    french_unigram = pickle.load(open('French_Uni_Dict.p', 'rb'))

    italian_bigram = pickle.load(open('Italian_Bi_Dict.p', 'rb'))
    italian_unigram = pickle.load(open('Italian_Uni_Dict.p', 'rb'))

    # Gets the total length
    V = len(enlgish_unigram) + len(french_unigram) + len(italian_unigram)

    # Opens the files and reads each line
    test = open('data/LangId.test', 'r').readlines()
    sol = open('data/LangId.sol', 'r').readlines()
    results = open('data/LangIDSolution.result', 'w')

    line_number = 1
    incorrect_lines = 0
    # For each file it calculates the probability and outputs
    for line in test:

        unigrams = word_tokenize(line)
        bigrams = list(ngrams(unigrams, 2))

        prob_english = compute_probability(bigrams, enlgish_unigram, english_bigram, V)
        print(prob_english)
        prob_french = compute_probability(bigrams, french_unigram, french_bigram, V)
        print(prob_french)
        prob_italian = compute_probability(bigrams, italian_unigram, italian_bigram, V)
        print(prob_italian)

        # Outputs the highest probability for the 3 languages into LangIDSolution.result
        if prob_english < prob_french and prob_english < prob_italian:
            results.write(str(line_number) + " English" + "\n")
            if sol[line_number - 1] != str(str(line_number) + " English" + "\n"):
                incorrect_lines += 1

            line_number += 1
        elif prob_french < prob_english and prob_french < prob_italian:
            results.write(str(line_number) + " French" + "\n")
            if sol[line_number - 1] != str(str(line_number) + " French" + "\n"):
                incorrect_lines += 1

            line_number += 1
        elif prob_italian < prob_french and prob_italian < prob_english:
            results.write(str(line_number) + " Italian" + "\n")
            if sol[line_number - 1] != str(str(line_number) + " Italian" + "\n"):
                incorrect_lines += 1

            line_number += 1
        else:
            results.write(str(line_number) + " " + "\n")
            if sol[line_number - 1] != str(str(line_number) + " " + "\n"):
                incorrect_lines += 1

            line_number += 1

    # Calculate Accuracy and output Accuracy and Incorrect lines
    accuracy_percentage = ((300 - incorrect_lines) / 300) * 100
    print("Accuracy: " + str(accuracy_percentage) + '%')
    print("Incorrect: " + str(incorrect_lines))
