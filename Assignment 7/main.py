import nltk
import random
import os
import pickle
import pandas as pd
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

wnl = WordNetLemmatizer()
Porterstemmer = PorterStemmer()

def process(userInput):
    # Lowercase user input
    tokens = word_tokenize(userInput.lower())
    # stemmer and lemmatizer on tokens
    tokens = [Porterstemmer.stem(t) for t in tokens]
    tokens = [wnl.lemmatize(t) for t in tokens]
    # POS Tagging
    tags = nltk.pos_tag(word_tokenize(userInput))
    pos_tagged = [t[0] for t in tags if t[1] == 'NNP']

    return tokens, pos_tagged


if __name__ == '__main__':
    Data = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(Data, 'uscities.csv'))
    # print(df)
    pd.options.display.max_columns = None
    intents = [
        {'required_words': ['hello', 'hi', 'hey'], 'response': ['Hello, What is your name?',
                                                                'Hi, What is your name?',
                                                                'Hey, What is your name?']},
        {'required_words': ['name'], 'response': ['How may I help you']},
        {'required_words': ['random'], 'response': ['Here is a Random City you could visit:']},
        {'required_words': ['cit'], 'response': ['The state of this city is:']},
        {'required_words': ['favorit'], 'response': ['This is also my favorite city', 'This is not my favorite city']},
        {'required_words': ['thanks', 'thank'], 'response': ['It is my pleasure.', 'No problem!', 'You are welcome.']},
    ]

    user = {'name': None}
    print('ChatBot: Hello, My name is ChatBot')
    while True:
        # Reading user input
        userInput = input("You: ")
        # Exit
        if userInput.lower() == 'exit':
            print('ChatBot: See you next time!')
            # Saves the user's data once exit from program
            if user['name'] is not None:
                file_name = user['name'] + '.txt'
                file = open(file_name, 'wb')
                pickle.dump(user, file)
                file.close()
            break
        required_words, entity = process(userInput)
        received_answer = False
        for int in intents:
            for intentsReqWord in int['required_words']:
                if intentsReqWord in required_words:
                    if 'name' in required_words:
                        user['name'] = "".join(entity[0])
                        if os.path.exists(user['name'] + '.txt'):
                            file_name = user['name'] + '.txt'
                            f = open(file_name, 'rb')
                            user = pickle.load(f)
                            f.close()
                            print('ChatBot: Its good To talk to you again,', entity[0], '... What would you like to know this time?')
                            print('ChatBot: Your favorite city is', user['favorit'])
                        else:
                            print('ChatBot: ', random.choice(int['response']), " ".join(entity), "?")
                    elif 'random' in required_words:
                        print('ChatBot: ', random.choice(int['response']))
                        city = " ".join(required_words[required_words.index(intentsReqWord) + 1:])
                        result = df.loc[df['city'].str.contains(city, case=False)]
                        print(result.sample())
                    elif 'cit' in required_words:
                        print('ChatBot: ', random.choice(int['response']))
                        state = " ".join(required_words[required_words.index(intentsReqWord) + 1:])
                        result = df.loc[df['city'].str.contains(state, case=False)]
                        print(result.sample())
                    elif 'favorit' in required_words:
                        print('ChatBot: ', random.choice(int['response']))
                        user['favorit'] = userInput[userInput.find(entity[0]):]
                    else:
                        print('ChatBot: ', random.choice(int['response']))
                    received_answer = True
                    break
            if received_answer:
                break
        if not received_answer:
            print('ChatBot: I am sorry, I do not know what you are trying to ask. Please ask again.')