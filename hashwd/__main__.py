# Import modules and functions
import argparse
import pyperclip
import re
import os
import hashwd
import parameters
import generate
import clear


# Define functions to handle the commands and arguments from the command line
def set_parameters():
    # Use argparse to handle commands and arguments from the command line
    parser = argparse.ArgumentParser(
        description="\nGenerate a strong, random password using a list of words and optional numbers and symbols.\n\n",
        epilog="\n")
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

    args = parser.parse_args()  # Parse the arguments from the command line
    
    # Get the directory of your script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the parameters.py file
    parameters_path = os.path.join(script_dir, "parameters.py")

    # Modifies the default values used when generating a password with no arguments
    if args.command == "defaults":
        # Open the parameters.py file and read its contents
        with open(parameters_path, "r") as file:
            defaults_contents = file.read()
        # If the -a flag is used, update the max values for numbers and symbols, also update the file path of the dictionary file
        print("Enter new default value for number of words. The current value is {}:"
              .format(parameters.WORDS_DEFAULT))
        new_default_words = input()
        if new_default_words:
            WORDS_DEFAULT = int(new_default_words)
            # Replace the current value of WORDS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"WORDS_DEFAULT = \d+", "WORDS_DEFAULT = {}".format(WORDS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_words = parameters.WORDS_DEFAULT

        print("Enter new default value for number of numbers. The current value is {}:"
              .format(parameters.NUMBERS_DEFAULT))
        new_default_numbers = input()
        if new_default_numbers:
            NUMBERS_DEFAULT = int(new_default_numbers)
            # Replace the current value of NUMBERS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"NUMBERS_DEFAULT = \d+", "NUMBERS_DEFAULT = {}".format(NUMBERS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_numbers = parameters.NUMBERS_DEFAULT

        print("Enter new default value for number of symbols. The current value is {}:"
              .format(parameters.SYMBOLS_DEFAULT))
        new_default_symbols = input()
        if new_default_symbols:
            SYMBOLS_DEFAULT = int(new_default_symbols)
            # Replace the current value of SYMBOLS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"SYMBOLS_DEFAULT = \d+", "SYMBOLS_DEFAULT = {}".format(SYMBOLS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_symbols = parameters.SYMBOLS_DEFAULT

        if args.all:
            print("Enter new default value for maximum number of symbols. The current value is {}:"
                  .format(parameters.MAX_SYMBOLS))
            new_max_symbols = input()
            if new_max_symbols:
                MAX_SYMBOLS = int(new_max_symbols)
                # Replace the current value of MAX_SYMBOLS in the string with the new value
                defaults_contents = re.sub(r"MAX_SYMBOLS = \d+", "MAX_SYMBOLS = {}".format(MAX_SYMBOLS),
                                           defaults_contents)
            else:
                new_max_symbols = parameters.MAX_SYMBOLS
            print("Enter new default value for maximum number of symbols. The current value is {}:"
                  .format(parameters.MAX_SYMBOLS))
            new_max_numbers = input()
            if new_max_numbers:
                MAX_NUMBERS = int(new_max_numbers)
                # Replace the current value of MAX_NUMBERS in the string with the new value
                defaults_contents = re.sub(r"MAX_NUMBERS = \d+", "MAX_NUMBERS = {}".format(MAX_NUMBERS),
                                           defaults_contents)
            else:
                new_max_numbers = parameters.MAX_NUMBERS
            print("Enter new filepath for dictionary file. The current path is {}:"
                  .format(parameters.DICTIONARY_FILE))
            new_dictionary_file = input()
            if new_dictionary_file:
                DICTIONARY_FILE = new_dictionary_file
                # Replace the current value of DICTIONARY_FILE in the string with the new value
                defaults_contents = re.sub(r"DICTIONARY_FILE = '.*?'", "DICTIONARY_FILE = '{}'"
                                           .format(DICTIONARY_FILE), defaults_contents)
            else:
                new_dictionary_file = parameters.DICTIONARY_FILE

            # Write the modified string back to the parameters.py file
            with open(parameters_path, "w") as file:
                defaults_contents = file.write(defaults_contents)
            exit()

        # Clear the clipboard and exit when the clear command is used
        if args.command == "clear":
            clear.clear_clipboard()
        exit()
    # Set default values for the number of words, numbers, and symbols
    num_words = parameters.WORDS_DEFAULT
    num_numbers = parameters.NUMBERS_DEFAULT
    num_symbols = parameters.SYMBOLS_DEFAULT

    # Use custom values instead of the default value if specified
    if args.words:  # If the --words argument is used
        num_words = args.words if args.words else parameters.WORDS_DEFAULT
    if args.numbers:  # If the --numbers argument is used
        num_numbers = args.numbers if args.numbers else parameters.NUMBERS_DEFAULT
    if args.symbols:  # If the --symbols argument is used
        num_symbols = args.symbols if args.symbols else parameters.SYMBOLS_DEFAULT

    # The --prompt argument allows user to specify the values for the number of words, numbers, and symbols
    if args.prompt:
        while True:
            num_words = input("How many words?:")
            if num_words == "":
                num_words = parameters.WORDS_DEFAULT
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
                num_numbers = parameters.NUMBERS_DEFAULT
                break
            try:
                num_numbers = int(num_numbers)
                if 0 <= num_numbers <= parameters.MAX_NUMBERS:
                    break
                else:
                    print("Enter a number between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")
        while True:
            num_symbols = input("How many symbols? 0-10: ")
            if num_symbols == "":
                num_symbols = parameters.SYMBOLS_DEFAULT
                break
            try:
                num_symbols = int(num_symbols)
                if 0 <= num_symbols <= 9:
                    break
                else:
                    print("Enter a symbols between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")
    # Generate a password using the default values if no arguments used
    if args.command == "generate":
        generate.generate_password(parameters.DICTIONARY_FILE,
                                        word_quantity=parameters.WORDS_DEFAULT,
                                        number_quantity=parameters.NUMBERS_DEFAULT,
                                        symbol_quantity=parameters.SYMBOLS_DEFAULT)

        password = generate.generate_password(parameters.DICTIONARY_FILE, num_words, num_numbers,
                                                   num_symbols)  # Generate a password

        # Copy the password to the clipboard if the --copy argument is used
        if args.copy:
            pyperclip.copy(password)
        if args.show:
            print(password)

    # Modify the defaults values for generating a default password
    if args.command == "defaults":
        # Read the contents of the parameters.py file into a string
        with open("parameters.py", "r") as file:
            defaults_contents = file.read()

    # Clear the clipboard and exit when the clear command is used
    if args.command == "clear":
        clear.clear_clipboard()
        exit()

# Run the password_parameters function
if __name__ == "__main__":
    set_parameters()
