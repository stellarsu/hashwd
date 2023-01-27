# Import modules and functions
import random
import pyperclip
import hashwd


# Function to generate a random password
def generate_password(dictionary, word_quantity=hashwd.pass_defaults.WORDS_DEFAULT,
                      number_quantity=hashwd.pass_defaults.NUMBERS_DEFAULT,
                      symbol_quantity=hashwd.pass_defaults.SYMBOLS_DEFAULT):
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
        password_elements.insert(0, "".join(random.sample(hashwd.pass_defaults.SYMBOLS, k=symbol_quantity)))
        password_elements.insert(0, "".join([str(num) for num in random.sample(range(0, 9), k=number_quantity)]))
    else:
        password_elements.append("".join(random.sample(hashwd.pass_defaults.SYMBOLS, k=symbol_quantity)))
        password_elements.append("".join([str(num) for num in random.sample(range(0, 9), k=number_quantity)]))

# Join the elements in the password_elements list into a single string, and numbers/symbols are joined without spaces
    password_generated = "".join([str(elem) if elem.isnumeric() or elem in hashwd.pass_defaults.SYMBOLS
                                  else f"{elem} " for elem in password_elements])

    return password_generated  # Return the generated password


# Create the function to clear the clipboard when the clear command is used
def clear_clipboard():
    pyperclip.copy("")
