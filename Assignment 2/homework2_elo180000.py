#############################################################
# File: Homework2_elo180000.py                              #
# Author: Ethan Ong (ELO180000)                             #
# Date: 2/17/2023                                           #
# Purpose: CS 4395 - Homework 2 (Word Guessing Game)        #
#############################################################

import sys
import nltk
import random
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

# NLTK Downloads
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

wnl = WordNetLemmatizer()


# Preprocessing raw text
def preprocess(raw):
    # tokenize the lower-case raw text
    tokens = word_tokenize(raw.lower())

    # store the stopword in a list
    stop_words = stopwords.words('english')

    # tokenize the lower-case raw text, reduce the tokens to only those that are alpha, not in the NLTK stopword list, and have length > 5
    tokens = [tk.lower() for tk in word_tokenize(raw) if len(tk) > 5]
    tokens = [tk for tk in tokens if tk not in stop_words]

    # lemmatize the tokens and use set() to make a list of unique lemmas
    unique = (wnl.lemmatize(tk) for tk in tokens)
    unique = list(set(unique))

    # do pos tag tagging on the unique lemmas and print the first 20 tagged
    tags = nltk.pos_tag(unique)

    # create a list of only those lemmas that are nouns
    nouns = [n[0] for n in tags if n[1].startswith("N")]

    # print all information and calculation for lexical diversity
    length_token = len(tokens)
    total_noun = len(nouns)
    calculation_lexical_diversity = ((len(unique)) / (len(tokens)))
    tags = tags[:20]
    print('\nNumber of Tokens:', length_token)
    print('Number of Nouns: %d' % total_noun)
    print("Lexical diversity: %.2f" % calculation_lexical_diversity)
    print('First 20 Tagged Items:', tags)

    return tokens, nouns


# Function for word guessing game
def word_guessing_game(words):
    # user starts with 5 points
    print("Let's play a word guessing game! \nEnter '!' to exit at any time of the game.")
    user_score = 5
    cumulative_score = 0

    # random generator to pick from the 50 words in the list
    pick_random_word = random.choice(words)[0]
    letter =[]

    # replaces every letter with _
    holder = '_'
    for prw in pick_random_word:
        print(holder, end=" ")

    # as long as the user score is above -1
    while user_score > -1:
        user_guess = input("\nGuess a Letter: ")

        # allows user to input either uppercase or lowercase letter
        if user_guess == user_guess.upper():
            user_guess = user_guess.lower()

        # quits the game if user inputs !
        if user_guess == '!':
            print("\nThanks for playing!")
            quit()


        # If user enters the correct letter, 1 point will be added to the user cumulative points, and it will be updated
        if user_guess in pick_random_word:
            user_score += 1
            letter.append(user_guess)
            print("Correct, Score is: ", user_score)
            for prw in pick_random_word:
                if prw in letter:
                    print(prw, end=" ")
                    cumulative_score += 1
                else:
                    print('_', end=" ")
        # if user enters the wrong letter, 1 point will be subtracted, and it will be updated
        else:
            user_score -= 1
            print("Sorry, Guess Again. Score is: ", user_score)
            for prw in pick_random_word:
                if prw in letter:
                    print(prw, end=" ")
                    cumulative_score -= 1
                else:
                    print('_', end=" ")

        # Once the user finish the word and gets it correct, the user will be prompt to guess another word
        if cumulative_score == len(pick_random_word):
            # Ask the user if they want to play again
            print("\n\nGuess another word")
            print("If you like to stop play the word guessing game enter '!'")
            print("\nCurrent Score: ", user_score)

            pick_random_word = random.choice(words)[0]
            letter = []

            holder = '_'
            for h in pick_random_word:
                print(holder, end=" ")
    # If user gets the word wrong, prints the statement and the word.
    # The program ends
    print("\n\nYou did not guess the word correct. The correct word is: ", pick_random_word)


# function to print the most common 50 words
def print_common_words(common_words):
    common_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:50]
    print("50 Most Common Words:")
    for w in range(50):
        common_list.append(common_words[w])
        print(common_words[w])


if __name__ == '__main__':
    # sends the filename to the main program in a sys arg
    # if no file can be read then prints error
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        print('Input file: ', input_file)

        with open('anat19.txt', 'r') as f:
            raw_text = f.read()

        tokens, noun = preprocess(raw_text)
        common_list = []

        # dictionary 
        counts = {t: tokens.count(t) for t in noun}

        # prints the 50 most common words
        print_common_words(counts)

        # word guessing game starts
        word_guessing_game(common_list)
    else:
        print('File name missing')
