import os

def terminal_cleaner():
    if os.name == "nt":
        # For Windows
        os.system("cls")
    else:
        # For Mac and Linux
        os.system("clear")

