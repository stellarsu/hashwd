# Import modules
import argparse
import pyperclip
from pyperclip import copy
import requests
import re
import hashwd
from hashwd import generate_password, clear_clipboard
import pass_defaults
from pass_defaults import WORDS_DEFAULT, NUMBERS_DEFAULT, SYMBOLS_DEFAULT, SYMBOLS, DICTIONARY_FILE


def main():
    # Use argparse to handle commands and arguments
    parser = argparse.ArgumentParser(
        description="Generate a strong, random password using a list of words and optional numbers and symbols.",
        epilog="")
    sub_parsers = parser.add_subparsers(title="subcommands", dest="command", required=True, help="")
    generate_parser = sub_parsers.add_parser("generate",
                                             help="generate a new password with or without arguments; hashwd generate")
    generate_parser.add_argument("-w", "--words", type=int,
                                 help="number of words in the password; hashwd generate -w 3")
    generate_parser.add_argument("-n", "--numbers", type=int,
                                 help="number of numbers in the password; hashwd generate -n 2 -w 2")
    generate_parser.add_argument("-s", "--symbols", type=int,
                                 help="number of symbols in the password; hashwd generate -s 2")
    generate_parser.add_argument("-c", "--copy", action="store_true",
                                 help="copy the password to the clipboard; hashwd generate -cw 2")
    generate_parser.add_argument("-S", "--show", action="store_true",
                                 help="print the password to the console; hashwd generate -Sw 2")
    generate_parser.add_argument("-P", "--prompt", action="store_true",
                                 help="prompts to input the values for number of words, numbers, "
                                      "and symbols; hashwd generate -PSc")
    clear_parser = sub_parsers.add_parser("clear", help="clear the clipboard after a password is copied; hashwd clear")
    defaults_parser = sub_parsers.add_parser("defaults",
                                             help="reset the default password generated with no arguments; "
                                                  "hashwd defaults")
    defaults_parser.add_argument("-a", "--all", action="store_true",
                                 help="update the max values for numbers and symbols, "
                                      "also update the file path of the dictionary file; hashwd defaults -a")

    args = parser.parse_args()

    # Handle the defaults command for modifying application defaults
    if args.command == "defaults":
        # Read the contents of the pass_defaults.py file into a string
        with open("pass_defaults.py", "r") as file:
            defaults_contents = file.read()

        print("Enter new default value for number of words. The current value is {}:"
              .format(pass_defaults.WORDS_DEFAULT))
        new_default_words = input()
        if new_default_words:
            pass_defaults.WORDS_DEFAULT = int(new_default_words)
            # Replace the current value of WORDS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"pass_defaults.WORDS_DEFAULT = \d+", "WORDS_DEFAULT = {}".format(WORDS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_words = pass_defaults.WORDS_DEFAULT

        print("Enter new default value for number of numbers. The current value is {}:"
              .format(NUMBERS_DEFAULT))
        new_default_numbers = input()
        if new_default_numbers:
            pass_defaults.NUMBERS_DEFAULT = int(new_default_numbers)
            # Replace the current value of NUMBERS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"pass_defaults.NUMBERS_DEFAULT = \d+", "pass_defaults.NUMBERS_DEFAULT = {}".format(pass_defaults.NUMBERS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_numbers = pass_defaults.NUMBERS_DEFAULT

        print("Enter new default value for number of symbols. The current value is {}:"
              .format(pass_defaults.SYMBOLS_DEFAULT))
        new_default_symbols = input()
        if new_default_symbols:
            pass_defaults.SYMBOLS_DEFAULT = int(new_default_symbols)
            # Replace the current value of SYMBOLS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"pass_defaults.SYMBOLS_DEFAULT = \d+", "pass_defaults.SYMBOLS_DEFAULT = {}".format(pass_defaults.SYMBOLS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_symbols = pass_defaults.SYMBOLS_DEFAULT

        if args.all:
            print("Enter new default value for maximum number of symbols. The current value is {}:"
                  .format(pass_defaults.MAX_SYMBOLS))
            new_max_symbols = input()
            if new_max_symbols:
                pass_defaults.MAX_SYMBOLS = int(new_max_symbols)
                # Replace the current value of MAX_SYMBOLS in the string with the new value
                defaults_contents = re.sub(r"pass_defaults.MAX_SYMBOLS = \d+", "pass_defaults.MAX_SYMBOLS = {}".format(pass_defaults.MAX_SYMBOLS),
                                           defaults_contents)
            else:
                new_max_symbols = pass_defaults.MAX_SYMBOLS
            print("Enter new default value for maximum number of numbers. The current value is {}:"
                  .format(pass_defaults.MAX_NUMBERS))
            new_max_numbers = input()
            if new_max_numbers:
                pass_defaults.MAX_NUMBERS = int(new_max_numbers)
                # Replace the current value of MAX_NUMBERS in the string with the new value
                defaults_contents = re.sub(r"pass_defaults.MAX_NUMBERS = \d+", "pass_defaults.MAX_NUMBERS = {}".format(pass_defaults.MAX_NUMBERS),
                                           defaults_contents)
            else:
                new_max_numbers = pass_defaults.MAX_NUMBERS
            print("Enter new filepath for dictionary file. The current path is {}:"
                  .format(pass_defaults.DICTIONARY_FILE))
            new_dictionary_file = input()
            if new_dictionary_file:
                pass_defaults.DICTIONARY_FILE = new_dictionary_file
                # Replace the current value of DICTIONARY_FILE in the string with the new value
                defaults_contents = re.sub(r"pass_defaults.DICTIONARY_FILE = '.*?'", "pass_defaults.DICTIONARY_FILE = '{}'"
                                           .format(pass_defaults.DICTIONARY_FILE), defaults_contents)
        else:
            new_dictionary_file = pass_defaults.DICTIONARY_FILE

        # Write the modified string back to the pass_defaults.py file
        with open("pass_defaults.py", "w") as file:
            file.write(defaults_contents)
            exit()

    # Clear the clipboard and exit when the clear command is used
    if args.command == "clear":
        hashwd.clear_clipboard()
        exit()
    # Set default values for the number of words, numbers, and symbols within main
    num_words = pass_defaults.WORDS_DEFAULT
    num_numbers = pass_defaults.NUMBERS_DEFAULT
    num_symbols = pass_defaults.SYMBOLS_DEFAULT

    # Use custom values instead of the default value if specified
    if args.words:
        num_words = args.words if args.words else pass_defaults.WORDS_DEFAULT
    if args.numbers:
        num_numbers = args.numbers if args.numbers else pass_defaults.NUMBERS_DEFAULT
    if args.symbols:
        num_symbols = args.symbols if args.symbols else pass_defaults.SYMBOLS_DEFAULT

    # The --prompt argument allows user to specify the values for the number of words, numbers, and symbols
    if args.prompt:
        while True:
            num_words = input("How many words?:")
            if num_words == "":
                num_words = pass_defaults.WORDS_DEFAULT
                break
            try:
                num_words = int(num_words)
                if 1 <= num_words <= 99:
                    break
                else:
                    print("Enter a number between 1 & 99.")
            except ValueError:
                print("Enter a valid number.")
        while True:
            num_numbers = input("How many numbers? 0-9: ")
            if num_numbers == "":
                num_numbers = pass_defaults.NUMBERS_DEFAULT
                break
            try:
                num_numbers = int(num_numbers)
                if 0 <= num_numbers <= pass_defaults.MAX_NUMBERS:
                    break
                else:
                    print("Enter a number between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")
        while True:
            num_symbols = input("How many symbols? 0-10: ")
            if num_symbols == "":
                num_symbols = pass_defaults.SYMBOLS_DEFAULT
                break
            try:
                num_symbols = int(num_symbols)
                if 0 <= num_symbols <= 9:
                    break
                else:
                    print("Enter a symbols between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")
    # Generate a password
    if args.command == "generate":
        hashwd.generate_password(pass_defaults.DICTIONARY_FILE, word_quantity=pass_defaults.WORDS_DEFAULT,
                          number_quantity=pass_defaults.NUMBERS_DEFAULT, symbol_quantity=pass_defaults.SYMBOLS_DEFAULT)

        password = hashwd.generate_password(pass_defaults.DICTIONARY_FILE, num_words, num_numbers, num_symbols)

        if args.copy:
            pyperclip.copy(password)
        if args.show:
            print(password)

    # Modify the defaults values for generating a default password
    if args.command == "defaults":
        # Read the contents of the pass_defaults.py file into a string
        with open("pass_defaults.py", "r") as file:
            defaults_contents = file.read()

    # Clear the clipboard and exit when the clear command is used
    if args.command == "clear":
        hashwd.clear_clipboard()
        exit()


if __name__ == "__main__":
    main()
