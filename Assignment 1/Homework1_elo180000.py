#########################################
# File: Homework1_elo180000.py          #
# Author: Ethan Ong - elo180000         #
# Date: 2/4/2023                        #
# Title: Text Processing with Python    #
#########################################

import sys
import pathlib
import re
import pickle


# Class that holds employee information
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Display the information of the employee
    def display(self):
        print("Employee id: ", self.id)
        print("\t", self.first, "", self.mi, "", self.last)
        print("\t", self.phone, "\n")


# Function for processing data from the input file
def process(text):
    # Gets rid of the header line from CSV file
    inputLines = text[0:]
    # Creates list for employees
    employees = {}

    # Reads the rest of the lines in the CSV file
    for line in inputLines:
        list = line.split(',')

        # Stores the input from file
        last = list[0]
        first = list[1]
        mi = list[2]
        id = list[3]
        phone = list[4]

        # Capitalizes the first and last name for the first letter and the rest to lower case
        last = last[0].capitalize() + last[1:].lower()
        first = first[0].capitalize() + first[1:].lower()

        # Notify the middle initial to be an uppercase letter, If there is no middle initial it is marked with an X
        if len(mi) != 1:
            mi = 'X'

        # REGEX format for ID and while loop if the user doesn't input the ID correct
        IdFormat = re.match(r'[A-Za-z]{2}\d{4}', id)
        while not IdFormat != re.match(r'[A-Za-z]{2}\d{4}', id):
            print("Invalid ID: " + id)
            print("The ID format should be 2 letters followed by 4 digits")
            id = input("Pleases enter a valid ID: ")
            IdFormat = re.match(r'[A-Za-z]{2}\d{4}', id)

        # REGEX format for Phone number and while loop if the user doesn't input the Phone number correct
        PhoneFormat = re.match(r'\d{3}-\d{3}-\d{4}', phone)
        while not PhoneFormat != re.match(r'\d{3}-\d{3}-\d{4}', phone):
            print("Phone " + phone + " is invalid")
            print("Enter phone number in the form 123-456-7890")
            phone = input("Enter phone number: ")
            PhoneFormat = re.match(r'\d{3}-\d{3}-\d{4}', phone)

        # Stores everything in dictionary of people
        employees[id] = Person(last, first, mi, id, phone)

    return employees


if __name__ == '__main__':
    # User needs to specify the relative path 'data/data.csv' in the sysarg.
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    # Read the file if the sysarg is done correctly
    fp = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(fp), 'r') as f:
        text_in = f.read().splitlines()

    # Ignore the header
    persons = process(text_in[1:])

    # pickle the persons and reads it
    pickle.dump(persons, open('persons.p', 'wb'))
    persons_in = pickle.load(open('persons.p', 'rb'))

    # Outputs employees from the pickled dict and make sure it was unpickled using the display funct.
    print("\nEmployee List:\n")
    for person in persons_in.values():
        person.display()
