from typing import Iterable
import os

def format_text(text: str) ->  None:
    print(f'\t{text}')

def menu():
    format_text('\nSelect an option:\n')
    format_text('[m] Upload multiple files')
    format_text('[s] Upload a single file')
    format_text('[i] Manual Input')
    format_text('[q] Quit')

def choice(valid_options: Iterable[str]) -> str:
    error = False
    while True:
        text = 'Enter an option: ' if not error else 'ERROR: Option not found. Enter a valid option: '

        menu()
        option = input(f'\n{text}').lower()
        
        if option not in valid_options:
            error = True
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            return option