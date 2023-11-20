import re

from pynput.keyboard import Controller, Key


keyboard = Controller()


def click_enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    
    
def keyboard_ctrl_c():
    with keyboard.pressed(Key.ctrl_l):
        keyboard.press('c')
        keyboard.release('c')
        

def keyboard_ctrl_a():
    with keyboard.pressed(Key.ctrl_l):
        keyboard.press('a')
        keyboard.release('a')
        

def perform_difference_between(arguments=''):
    """
    replace `dif X Y Z` with `What is the difference between X, Y, Z, ...?`
    """
    words_list = re.split(r'[,;\s]+', arguments) # split on comma, semicolon or whitespace
    words_list = [x for x in words_list if x != 'and'] # remove 'and'
    words_quoted = ', '.join(f'"{word}"' for word in words_list[:-1])
    words_quoted += f', and "{words_list[-1]}"'
    command = f"What is the difference between {words_quoted}?"
    keyboard_ctrl_a()
    keyboard.type(command)


def perform_python_manage_runserver(arguments=''):
    """
    replace `pmr` with `python manage.py runserver *args`
    """
    keyboard_ctrl_a()
    command = 'python manage.py runserver'
    keyboard.type(command + ' ' + arguments)


def perform_python_manage_makemigrations(arguments=''):
    """
    replace `pmmm` with `python manage.py makemigrations *args`
    """
    keyboard_ctrl_a()
    command = 'python manage.py makemigrations'
    keyboard.type(command + ' ' + arguments)


def perform_python_manage_migrate(arguments=''):
    """
    replace `pmm` with `python manage.py migrate *args`
    """
    keyboard_ctrl_a()
    command = 'python manage.py migrate'
    keyboard.type(command + ' ' + arguments)


def perform_search_youtube(arguments=''):
    """
    Find a video on YouTube by search query:\n
    https://www.youtube.com/results?search_query=
    """
    keyboard_ctrl_a()
    command = 'https://www.youtube.com/results?search_query='
    keyboard.type(command + arguments)


def perform_search_merriam_webster(arguments=''):
    """
    Find a word on Merriam-Webster:\n
    https://www.merriam-webster.com/dictionary/
    """
    keyboard_ctrl_a()
    command = 'https://www.merriam-webster.com/dictionary/'
    keyboard.type(command + arguments)


def perform_search_cambridge_dictionary(arguments=''):
    """
    Find a word on Cambridge Dictionary:\n
    https://dictionary.cambridge.org/dictionary/english/
    """
    keyboard_ctrl_a()
    command = 'https://dictionary.cambridge.org/dictionary/english/'
    keyboard.type(command + arguments)
    