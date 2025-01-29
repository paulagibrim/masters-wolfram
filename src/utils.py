# File: utils.py
# Creation: 28/01/2025
# Last update: 28/01/2025
# Author: @paulagibrim
# Description: This file contains utility functions for the project.

def custom_print(text: str, color:str='white'):
    if color == 'white':
        print(text)

    elif color == 'red':
        print(f"\033[31m{text}\033[0m")

    elif color == 'green':
        print(f"\033[32m{text}\033[0m")

    elif color == 'yellow':
        print(f"\033[33m{text}\033[0m")

    elif color == 'blue':
        print(f"\033[34m{text}\033[0m")

    elif color == 'purple':
        print(f"\033[35m{text}\033[0m")

    elif color == 'cyan':
        print(f"\033[36m{text}\033[0m")

    elif color == 'gray':
        print(f"\033[37m{text}\033[0m")

    else:
        raise ValueError("Invalid color. Please use one of the following options: 'white', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'gray'.")

def paint(color, text):
    if color == 'white':
        return text

    elif color == 'red':
        return f"\033[31m{text}\033[0m"

    elif color == 'green':
        return f"\033[32m{text}\033[0m"

    elif color == 'yellow':
        return f"\033[33m{text}\033[0m"

    elif color == 'blue':
        return f"\033[34m{text}\033[0m"

    elif color == 'purple':
        return f"\033[35m{text}\033[0m"

    elif color == 'cyan':
        return f"\033[36m{text}\033[0m"

    elif color == 'gray':
        return f"\033[37m{text}\033[0m"

    else:
        raise ValueError("Invalid color. Please use one of the following options: 'white', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan', 'gray'.")