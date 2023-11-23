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
    
    
def delete_keyword_and_args(n=1):
    for _ in range(n):
        click_backspace()
        
    with keyboard.pressed(Key.ctrl):
        click_backspace(5)
    

def replace_dif_keyword_with_question(arguments: str = '', should_click_enter=True) -> bool:
    """
    replace `dif a, b, c` with `What is the difference between "a", "b", and "c"?`
    """
    words_list = re.split(r'[,;\s]+', arguments) # split on comma, semicolon, or whitespace
    words_list = [x for x in words_list if x != 'and'] if words_list != [''] else [] # remove 'and'
    
    if len(words_list) <= 1:
        should_click_enter = False
        if len(words_list) == 0:
            question = 'What is the difference between "word"?'
        if len(words_list) == 1:
            question = f'What is the difference between "{words_list[0]}" and "word"?'
    
    else:
        words_str = ', '.join([f'"{word}"' for word in words_list[:-1]])
        if len(words_list) > 2:
            words_str += ','
            
        words_str += f' and "{words_list[-1]}"'
        question = f"What is the difference between {words_str}?"

    delete_keyword_and_args(n=len(arguments))
    keyboard.type(question)     
    
    # If there is less than 2 words, select the "word" placeholder
    if len(words_list) <= 1:
        click_left(2)
        with keyboard.pressed(Key.ctrl_l, Key.shift_l):
            click_left()
        
    return should_click_enter
