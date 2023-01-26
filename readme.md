hashwd

Introduction
hashwd is a command-line application that generates strong, random passwords using a list of words and optional numbers and symbols. The password is generated by randomly selecting words from a dictionary file, capitalizing one of the words, and adding optional numbers and symbols at the beginning or end of the password.


Commands
generate: generates a new password using the default or custom parameters
clear: clears the OS clipboard
Arguments
-h, --help: Show the help message and exit
-d, --default: Use default values for number of words, numbers, and symbols
-w, --words: Number of words in the password (must be between 1 and 99)
-n, --numbers: Number of numbers in the password (must be between 0 and 9)
-s, --symbols: Number of symbols in the password (must be between 0 and 9)
-c, --copy: Copy the password to the clipboard
-S, --show: Print the password to the console
-P, --prompt: Prompt for number of words, numbers, and symbols


Usage
To use the script, run the following command in the terminal:
python hashwd.py generate [-h] [-d] [-w W] [-n N] [-s S] [-c] [-S] [-P] [-C]

Generate a password with the default number of words, numbers, and symbols:
python hashwd.py generate

Generate a password with 5 words, 2 numbers, and 3 symbols:
python hashwd.py generate -w 5 -n 2 -s 3

Generate a password and prompt for the number of words, numbers, and symbols. Additionally, print the password to the terminal and copy it to the clipboard automatically:
python hashwd.py -PSc

Clear the clipboard:
python hashwd.py clear


Requirements
Python 3
pyperclip (for copying the password to the clipboard)
requests
argparse
random


License
hashwd is released under the GNU General Public License v3.0.

Credits
hashwd was developed by Jordan Langland, 2023.