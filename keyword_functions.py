import re

from pynput.keyboard import Controller, Key


keyboard = Controller()


def click_enter(n=1):
    for _ in range(n):
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)


def click_left(n=1):
    for _ in range(n):
        keyboard.press(Key.left)
        keyboard.release(Key.left)


def click_right(n=1):
    for _ in range(n):
        keyboard.press(Key.right)
        keyboard.release(Key.right)


def click_backspace(n=1):
    for _ in range(n):
        keyboard.press(Key.backspace)
        keyboard.release(Key.backspace)
    
    
def delete_args_and_keyword(n=1):
    for _ in range(n):
        click_backspace()
        
    with keyboard.pressed(Key.ctrl):
        click_backspace(5)
    
    
def keyboard_ctrl_c():
    with keyboard.pressed(Key.ctrl_l):
        keyboard.press('c')
        keyboard.release('c')
        

def keyboard_ctrl_a():
    with keyboard.pressed(Key.ctrl_l):
        keyboard.press('a')
        keyboard.release('a')
        

def perform_difference_between(arguments='', should_click_enter=True):
    """
    replace `dif a, b, c` with `What is the difference between "a", "b", and "c"?`
    """
    words_list = re.split(r'[,;\s]+', arguments) # split on comma, semicolon, or whitespace
    words_list = [x for x in words_list if x != 'and'] if words_list != [''] else [] # remove 'and'
    words_str = ''
    
    if len(words_list) <= 1:
        should_click_enter = False
        if len(words_list) == 0:
            command = 'What is the difference between "word"?'
        if len(words_list) == 1:
            command = f'What is the difference between "{words_list[0]}" and "word"?'
    
    else:
        words_str = ', '.join([f'"{word}"' for word in words_list[:-1]])
        if len(words_list) > 2:
            words_str += ','
            
        words_str += f' and "{words_list[-1]}"'
        command = f"What is the difference between {words_str}?"

    delete_args_and_keyword(n=len(arguments))
    keyboard.type(command)     
    
    if len(words_list) <= 1:
        click_left(2)
        with keyboard.pressed(Key.ctrl_l, Key.shift_l):
            click_left()
        
    return should_click_enter


def perform_python_manage_runserver(arguments='', should_click_enter=True):
    """
    replace `pmr *args` with `python manage.py runserver *args`
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'python manage.py runserver'
    keyboard.type(command + ' ' + arguments)
    
    return should_click_enter


def perform_python_manage_makemigrations(arguments='', should_click_enter=True):
    """
    replace `pmmm *args` with `python manage.py makemigrations *args`
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'python manage.py makemigrations'
    keyboard.type(command + ' ' + arguments)
    
    return should_click_enter


def perform_python_manage_migrate(arguments='', should_click_enter=True):
    """
    replace `pmm *args` with `python manage.py migrate *args`
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'python manage.py migrate'
    keyboard.type(command + ' ' + arguments)
    
    return should_click_enter


def perform_search_youtube(arguments='', should_click_enter=True):
    """
    Find a video on YouTube by search query:\n
    https://www.youtube.com/results?search_query=
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'https://www.youtube.com/results?search_query='
    keyboard.type(command + arguments)

    return should_click_enter


def perform_search_merriam_webster(arguments='', should_click_enter=True):
    """
    Find a word on Merriam-Webster:\n
    https://www.merriam-webster.com/dictionary/
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'https://www.merriam-webster.com/dictionary/'
    keyboard.type(command + arguments)

    return should_click_enter


def perform_search_cambridge_dictionary(arguments='', should_click_enter=True):
    """
    Find a word on Cambridge Dictionary:\n
    https://dictionary.cambridge.org/dictionary/english/
    """
    delete_args_and_keyword(n=len(arguments))
    command = 'https://dictionary.cambridge.org/dictionary/english/'
    keyboard.type(command + arguments)
    
    return should_click_enter
