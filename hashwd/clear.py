# Description: This file contains the function to clear the clipboard when the clear command is used
# Import modules and functions
import pyperclip


# Create the function to clear the clipboard when the clear command is used
def clear_clipboard():
    pyperclip.copy("")  # Copy an empty string to the clipboard to wipe it
