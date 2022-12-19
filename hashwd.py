# Import necessary modules
import random
import pyperclip
import argparse
from defaults import WORDS_DEFAULT, NUMBERS_DEFAULT, SYMBOLS_DEFAULT, DICTIONARY_FILE, SYMBOLS, MAX_SYMBOLS, MIN_SYMBOLS, MAX_WORDS, MIN_WORDS, MAX_NUMBERS, MIN_NUMBERS
import re


# Function to generate a random password
def generate_password(dictionary, word_quantity=WORDS_DEFAULT, number_quantity=NUMBERS_DEFAULT, symbol_quantity=SYMBOLS_DEFAULT):
    # read the file line by line and generate the password using only the words that are needed
    words = []
    with open(dictionary, "r") as temp_dictionary_file:
        for line in temp_dictionary_file:
            words.append(line.strip())
    password_words = random.sample(words, k=word_quantity)

    # Choose a random index and capitalize the word at that index in the original list of words
    random_index = random.randint(0, len(password_words) - 1)
    password_words[random_index] = password_words[random_index].capitalize()

    # Create a list to store the password elements
    password_elements = []

    # Add the words to the password_elements list, filtering out any words that are shorter than 5 characters
    password_elements.extend([word for word in password_words if len(word) >= 5])

    # Randomly place the numbers and symbols at the beginning or end of the password
    if random.random() < 0.5:
        password_elements.insert(0, "".join(random.sample(SYMBOLS, k=symbol_quantity)))
        password_elements.insert(0, "".join([str(num) for num in random.sample(range(0, 9), k=number_quantity)]))
    else:
        password_elements.append("".join(random.sample(SYMBOLS, k=symbol_quantity)))
        password_elements.append("".join([str(num) for num in random.sample(range(0, 9), k=number_quantity)]))

# Join the elements in the password_elements list into a single string, and numbers/symbols are joined without spaces
    password_generated = "".join([str(elem) if elem.isnumeric() or elem in SYMBOLS else f"{elem} " for elem in password_elements])

    return password_generated


# Create the function to clear the clipboard when the clear command is used
def clear_clipboard():
    pyperclip.copy("")


if __name__ == "__main__":
    # Use argparse to handle commands and arguments
    parser = argparse.ArgumentParser(
        description="Generate a strong, random password using a list of words and optional numbers and symbols.",
        epilog="")
    parser.add_argument("-d", "--default", action="store_true",
                        help="use default values for number of words, numbers, and symbols")
    parser.add_argument("-w", "--words", type=int, help="number of words in the password")
    parser.add_argument("-n", "--numbers", type=int, help="number of numbers in the password")
    parser.add_argument("-s", "--symbols", type=int, help="number of symbols in the password")
    parser.add_argument("-c", "--copy", action="store_true", help="copy the password to the clipboard")
    parser.add_argument("-a", "--all", action="store_true", help="expand the defaults command to include symbols and update the max values for numbers and symbols")
    parser.add_argument("-D", "--modify-defaults", action="store_true", help="prompts to modify the default values")
    parser.add_argument("-S", "--show", action="store_true", help="print the password to the console")
    parser.add_argument("-P", "--prompt", action="store_true",
                        help="prompts to input the values for number of words, numbers, and symbols")
    parser.add_argument("command", choices=["generate", "clear", "defaults"],
                        help="specify whether to generate a new password, clear the clipboard, or modify defaults")
    args = parser.parse_args()

    # Handle the defaults command for modifying application defaults
    if args.command == "defaults":
        # Read the contents of the defaults.py file into a string
        with open("defaults.py", "r") as file:
            defaults_contents = file.read()

        print("Enter new default value for number of words. The current value is {}:".format(WORDS_DEFAULT))
        new_default_words = input()
        if new_default_words:
            WORDS_DEFAULT = int(new_default_words)
            # Replace the current value of WORDS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"WORDS_DEFAULT = \d+", "WORDS_DEFAULT = {}".format(WORDS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_words = WORDS_DEFAULT

        print("Enter new default value for number of numbers. The current value is {}:".format(NUMBERS_DEFAULT))
        new_default_numbers = input()
        if new_default_numbers:
            NUMBERS_DEFAULT = int(new_default_numbers)
            # Replace the current value of NUMBERS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"NUMBERS_DEFAULT = \d+", "NUMBERS_DEFAULT = {}".format(NUMBERS_DEFAULT),
                                       defaults_contents)
        else:
            new_default_numbers = NUMBERS_DEFAULT

        print("Enter new default value for number of symbols. The current value is {}:".format(SYMBOLS_DEFAULT))
        new_default_symbols = input()
        if new_default_symbols:
            SYMBOLS_DEFAULT = int(new_default_symbols)
            # Replace the current value of SYMBOLS_DEFAULT in the string with the new value
            defaults_contents = re.sub(r"SYMBOLS_DEFAULT = \d+", "SYMBOLS_DEFAULT = {}".format(SYMBOLS_DEFAULT), defaults_contents)
        else:
            new_default_numbers = NUMBERS_DEFAULT

        if args.all:
            print("Enter new default value for maximum number of symbols. The current value is {}:".format(MAX_SYMBOLS))
            new_max_symbols = input()
            if new_max_symbols:
                MAX_SYMBOLS = int(new_max_symbols)
                # Replace the current value of MAX_SYMBOLS in the string with the new value
                defaults_contents = re.sub(r"MAX_SYMBOLS = \d+", "MAX_SYMBOLS = {}".format(MAX_SYMBOLS), defaults_contents)
            else:
                new_max_symbols = MAX_SYMBOLS
            print("Enter new default value for maximum number of numbers. The current value is {}:".format(MAX_NUMBERS))
            new_max_numbers = input()
            if new_max_numbers:
                MAX_NUMBERS = int(new_max_numbers)
                # Replace the current value of MAX_NUMBERS in the string with the new value
                defaults_contents = re.sub(r"MAX_NUMBERS = \d+", "MAX_NUMBERS = {}".format(MAX_NUMBERS), defaults_contents)
            else:
                new_max_numbers = MAX_NUMBERS
            print("Enter new filepath for dictionary file. The current path is {}:".format(DICTIONARY_FILE))
            new_dictionary_file = input()
            if new_dictionary_file:
                DICTIONARY_FILE = new_dictionary_file
                # Replace the current value of DICTIONARY_FILE in the string with the new value
                defaults_contents = re.sub(r"DICTIONARY_FILE = '.*?'", "DICTIONARY_FILE = '{}'".format(DICTIONARY_FILE), defaults_contents)
        else:
            new_dictionary_file = DICTIONARY_FILE

        # Write the modified string back to the defaults.py file
        with open("defaults.py", "w") as file:
            file.write(defaults_contents)
            exit()

    # Clear the clipboard and exit when the clear command is used
    if args.command == "clear":
        clear_clipboard()
        exit()
    # Set default values for the number of words, numbers, and symbols within main
    num_words = WORDS_DEFAULT
    num_numbers = NUMBERS_DEFAULT
    num_symbols = SYMBOLS_DEFAULT

    # Use custom values instead of the default value if specified
    if args.words:
        num_words = args.words
    if args.numbers:
        num_numbers = args.numbers
    if args.symbols:
        num_symbols = args.symbols

    # The --prompt argument allows user to specify the values for the number of words, numbers, and symbols
    if args.prompt:
        while True:
            num_words = input("How many words?:")
            if num_words == "":
                num_words = WORDS_DEFAULT
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
                num_numbers = NUMBERS_DEFAULT
                break
            try:
                num_numbers = int(num_numbers)
                if 0 <= num_numbers <= MAX_NUMBERS:
                    break
                else:
                    print("Enter a number between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")
        while True:
            num_symbols = input("How many symbols? 0-10: ")
            if num_symbols == "":
                num_symbols = SYMBOLS_DEFAULT
                break
            try:
                num_symbols = int(num_symbols)
                if 0 <= num_symbols <= 9:
                    break
                else:
                    print("Enter a symbols between 0 & 9.")
            except ValueError:
                print("Enter a valid number.")

    password = generate_password(DICTIONARY_FILE, num_words, num_numbers, num_symbols)

    # Copy the password to the clipboard
    if args.copy:
        pyperclip.copy(password)
        print("Password copied. Use 'hashwd clear' to clear the clipboard.")
    # Print the password to the terminal if the print flag is set
    if args.show:
        print(password)
