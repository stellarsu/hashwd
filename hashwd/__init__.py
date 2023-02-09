# __init__.py


from generate import generate_password
from clear import clear_clipboard
from parameters import MIN_WORDS, MAX_WORDS, MIN_NUMBERS, MAX_NUMBERS, MIN_SYMBOLS, MAX_SYMBOLS, SYMBOLS, DICTIONARY_FILE, WORDS_DEFAULT, NUMBERS_DEFAULT, SYMBOLS_DEFAULT
from pyperclip import copy
<<<<<<< Updated upstream
from generate import generate_password
from clear import clear_clipboard
from parameters import MIN_WORDS, MAX_WORDS, MIN_NUMBERS, MIN_SYMBOLS, MAX_SYMBOLS, MAX_SYMBOLS, DICTIONARY_FILE, WORDS_DEFAULT, NUMBERS_DEFAULT, SYMBOLS_DEFAULT
=======
from random import randint, random, sample
from argparse import ArgumentParser
from sys import exit
from os import path
from re import match
>>>>>>> Stashed changes
