"""Simple command-line interface for managing a book database."""

import sys
import os


DB_FILE_PATH = ''
VALID_INPUTS = ['1', '2', 'q', 'c']
MAIN_MENU_OPTIONS = [
    '1) Add new book',
    '2) Print current database content in ascending order by publishing year',
    'Q) Exit the program',
    'C) Clear terminal screen'
    ]


def print_border(length: int, char='-'):
    """Prints a line of repeated characters as a border."""
    print(char * length)


def print_inside_box(text_list: list, char=['|', '-']):
    """Prints text inside a bordered box with customizable padding.

    Parameters
    ----------
    text_list : list
        Text to be printed inside box. Each item is printed on its own line.
    char : list, optional
        Borders for the box
    """
    length = len(max(text_list, key=len))
    width = length + 6
    print()
    print_border(length=width, char=char[1])
    for text in text_list:
        padding_right = width - len(text) - 4
        print(f'{char[0]}{" " * 2}{text}{" " * padding_right}{char[0]}')
    print_border(length=width, char=char[1])
    print()


def print_headers(
        headers: list,
        max_title_length: int | str,
        max_author_length: int | str,
        max_isbn_length: int | str,
        max_year_length: int | str,
        border_width: int | str):
    """Prints text inside a bordered box with customizable padding.

    Parameters
    ----------
    headers : list
        Header texts for printing out book database.
    max_title_length : int | str
        Longest title on database as num.
    max_author_length : int | str
        Longest author name on database as num.
    max_isbn_length : int | str
        Longest ISBN on database as num.
    max_year_length : int | str
        Longest year on database as num.
    border_width : int | str
        Width of the border.
    """
    title_padding = max_title_length - len(str(headers[0]))
    author_padding = max_author_length - len(str(headers[1]))
    isbn_padding = max_isbn_length - len(str(headers[2]))
    year_padding = max_year_length - len(str(headers[3]))
    print(f'|{" " * 2}{headers[0]}{" " * title_padding}  ', end='')
    print(f'|{" " * 2}{headers[1]}{" " * author_padding}  ', end='')
    print(f'|{" " * 2}{headers[2]}{" " * isbn_padding}  ', end='')
    print(f'|{" " * 2}{headers[3]}{" " * year_padding}  |')
    print(f'{"-" * border_width}')


def print_db_prettified(db_books: list):
    """Prints the database in a formatted table.

    Parameters
    ----------
    db_books : list
        Book data in a list of lists format [[]]
    """
    headers = ['BOOK', 'WRITER', 'ISBN', 'PUBLISHING YEAR']
    db_books.append(headers)
    max_lengths = [
        max(len(str(item)) for item in data) for data in zip(*db_books)]
    db_books.pop()
    length = sum(max_lengths)
    max_title_length = max_lengths[0]
    max_author_length = max_lengths[1]
    max_isbn_length = max_lengths[2]
    max_year_length = max_lengths[3]
    border_width = length + 21
    print_border(length=border_width)
    print_headers(
        headers,
        max_title_length,
        max_author_length,
        max_isbn_length,
        max_year_length,
        border_width)
    for book_info in db_books:
        title_padding = max_title_length - len(str(book_info[0]))
        author_padding = max_author_length - len(str(book_info[1]))
        isbn_padding = max_isbn_length - len(str(book_info[2]))
        year_padding = max_year_length - len(str(book_info[3]))
        print(f'|{" " * 2}{book_info[0]}{" " * title_padding}  ', end='')
        print(f'|{" " * 2}{book_info[1]}{" " * author_padding}  ', end='')
        print(f'|{" " * 2}{book_info[2]}{" " * isbn_padding}  ', end='')
        print(f'|{" " * 2}{book_info[3]}{" " * year_padding}  |')
    print_border(length=border_width)
    print()


def print_error(error_message: list, char=['!', '!']):
    """Prints an error message inside a bordered box.

    Parameters
    ----------
    error_message : list
        Text to be printed inside box. Each item is printed on its own line.
    char : list, optional
        Borders for the box.
    """
    print_inside_box(error_message, char)


def print_main_menu_ui():
    """Displays the main menu to the user."""
    print_inside_box({'Book Database'})
    print(MAIN_MENU_OPTIONS[0])
    print(MAIN_MENU_OPTIONS[1])
    print(MAIN_MENU_OPTIONS[2])
    print(MAIN_MENU_OPTIONS[3])
    print('')


def take_input() -> str:
    """Prompts the user for an option input.

    Returns
    -------
    str
        User input transformed in to lower case.
    """
    option = input('Type your option and press enter: ')
    return option.lower()


def read_db() -> list | bool:
    """Reads database file to a list.

    Raises
    ------
    FileNotFoundError
        If file is not found from given path.
    ValueError
        If value in the database is saved in wrong format.

    Returns
    -------
    list | False
        Sorted list of database books | False value if error happens.
    """
    db_books = []
    count = 0
    try:
        with open(DB_FILE_PATH, "r") as file:
            for line in file:
                count += 1
                title, author, isbn, year = line.strip().split('/')
                db_books.append([title, author, isbn, year])
    except FileNotFoundError:
        file_not_found_warning = [
            f'File from path: "{DB_FILE_PATH} not found!"',
            'Make sure you gave the path correctly and try again',
            'Returning to main menu...'
            ]
        print_error(file_not_found_warning)
        return False
    except ValueError:
        file_values_corrupt = [
            f'File from path: "{DB_FILE_PATH} has invalid values!"',
            f'Error found on line {count}',
            f'Faulty data was: {line.strip()}',
            'Correct syntax is: Book Name/Author/ISBN/Publishing Year',
            'Returning to main menu...'
            ]
        print_error(file_values_corrupt)
        return False
    db_books.sort(key=lambda x: ''.join(filter(str.isdigit, x[3])))
    return db_books


def print_db_to_terminal(db_books: list):
    """Prints given database content in ascending order by publishing year"""
    print_db_prettified(db_books)


def add_book_to_db():
    """Prompts user for book details and saves them to the database file.

    Raises
    ------
    FileNotFoundError
        If file is not found from given path.
    """
    print_inside_box(['Add new book'])
    book = input('Give books name: ')
    author = input('Give authors name: ')
    isbn = input('Give ISBN: ')
    publishing_year = input('Give publishing year: ')
    while True:
        print_inside_box(['Verify given data before saving to database...'])
        print(f'Book name: {book}')
        print(f'Author: {author}')
        print(f'ISBN: {isbn}')
        print(f'Publishing year: {publishing_year}')
        print_inside_box(['Is given information ok?'])
        print('y) Save to database')
        print('n) Return to main menu')
        print('')
        option = take_input()
        if option == 'y':
            try:
                with open(DB_FILE_PATH, 'a') as file:
                    file.write('\n')
                    file.write(f'{book}/{author}/{isbn}/{publishing_year}')
            except FileNotFoundError:
                file_not_found_warning = [
                    f'File from path: "{DB_FILE_PATH} not found!"',
                    'Make sure you gave the path correctly and try again',
                    'Returning to main menu...'
                ]
                print_error(file_not_found_warning)
            print('save')
            break
        elif option == 'n':
            break
        else:
            continue


def print_db():
    """Displays the book database content."""
    print_inside_box(['Print database!'])
    db_books = read_db()
    if db_books:
        print_db_to_terminal(db_books)


def exit_program():
    """Exits the program."""
    print_inside_box(['Exiting the program. Have a lovely day!'])
    sys.exit()


def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls||clear')


def main_menu():
    """Displays the main menu."""
    commands = {
        '1': add_book_to_db,
        '2': print_db,
        'q': exit_program,
        'c': clear_terminal
    }
    print_main_menu_ui()
    option = take_input()
    action = commands.get(option)
    if action:
        action()
    else:
        invalid_input_warning = [
            f'Invalid input: "{option}"',
            f'Valid inputs are: {', '.join(VALID_INPUTS).upper()}',
            'Returning to main menu...'
        ]
        print_error(invalid_input_warning)


if __name__ == '__main__':
    while True:
        try:
            DB_FILE_PATH = sys.argv[1]
        except IndexError:
            raise IndexError("Please, provide database file as an argument.")
        main_menu()
