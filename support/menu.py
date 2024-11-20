from typing import Iterable

def format_text(text: str) -> str:
    return f'\t{text}'

def menu():
    print(format_text('\nSelect an option:\n'))
    print(format_text('[m] Upload multiple files'))
    print(format_text('[s] Upload a single file'))
    print(format_text('[q] Quit'))

def choice(valid_options: Iterable[str]) -> str:
    while True:
        option = input(format_text('\nEnter an option: ')).lower()

        if option not in valid_options:
            print(format_text('ERROR: Option not found.'))
        else:
            return option