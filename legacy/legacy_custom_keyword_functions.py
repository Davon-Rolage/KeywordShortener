import re

from pynput.keyboard import Controller, Key


keyboard = Controller()


def clickn(char: str='', n=1):
    """
    Executes a keyboard tap action for a given character `n` times.
    """
    for _ in range(n):
        keyboard.tap(char)


def with_pressed_click(keys: list|str, char: str):
    """
    Holds down the specified key(s) followed by a character key tap.
    """
    keys = keys if isinstance(keys, list) else [keys]
    with keyboard.pressed(*keys):
        keyboard.tap(char)


def test_transform_dif_to_question():
    test_arguments = [
        '',
        'python',
        'python java',
        'python, java, django',
        'python; java; django',
        'python java "django templates"',
        'python, java  django, javascript, css and html',
        "python and java and django, javascript, 'css and html'",
        '"python", java, "django templates" ruby, \'javascript\'; css and html',
    ]
    print("\n**********\nTesting transform_dif_to_question():\n**********")
    for arg in test_arguments:
        print(f'"{arg}" -> {transform_dif_to_question(arg, test=True)}')
    print("**********\nDone testing transform_dif_to_question()\n**********\n")


def transform_dif_to_question(arguments: str = '', should_click_enter=True, test=False) -> bool:
    """
    replace `dif "two words" b c` with `What is the difference between "two words", "b", and "c"?`
    """
    # split on single/double quotes, comma, semicolon, and whitespace
    regex = r'(?:"[^"]+"|\'[^\']+\')|\w+'
    words_list = re.findall(regex, arguments)
    words_list = [arg.strip('"').strip("'") for arg in words_list if arg != 'and' and arg != '']
    
    if len(words_list) <= 1:
        should_click_enter = False
        if len(words_list) == 0:
            question = 'What is the difference between "word"?'
        if len(words_list) == 1:
            question = f'What is the difference between "{words_list[0]}" and "word"?'
    
    else:
        words_str = ', '.join([f'"{word}"' for word in words_list[:-1]])
        # Add Oxford comma
        if len(words_list) > 2:
            words_str += ','
            
        words_str += f' and "{words_list[-1]}"'
        question = f"What is the difference between {words_str}?"

    if test:
        return question
    
    keyboard.type(question)
    
    # If there is less than 2 words, select the "word" placeholder
    if len(words_list) <= 1:
        clickn(Key.left, 2)
        with_pressed_click([Key.ctrl_l, Key.shift_l], Key.left)
        
    return should_click_enter


if __name__ == '__main__':
    test_transform_dif_to_question()
