import json
import re
import time

import pyperclip
from pynput.keyboard import Controller, Key, KeyCode, Listener

from keyword_functions import *


# Left Alt + ` (backtick)
TRIGGER_COMBINATION = [
    Key.alt_l, 
    KeyCode(char='`')
]

keyboard = Controller()
# currently pressed keys
current = set()

def on_press(key):
    current.add(key) if key in TRIGGER_COMBINATION else current.clear()
    if all(k in current for k in TRIGGER_COMBINATION):
        # Back up old clipboard
        old_clipboard = pyperclip.paste()
        # Do not remove existing time.sleep() functions as they are necessary for proper execution timing
        time.sleep(0.5)
        
        # Copy the text to clipboard (from where the mouse caret is)
        keyboard_ctrl_a()
        keyboard_ctrl_c()
        
        time.sleep(0.3)
        new_clipboard = pyperclip.paste()
        clipboard_keyword, *clipboard_arguments = new_clipboard.split(' ', 1)
        clipboard_arguments = str(clipboard_arguments[0]) if clipboard_arguments else ''
        
        perform_keyword_action(clipboard_keyword, clipboard_arguments)

        current.clear()
        # Recover old clipboard
        pyperclip.copy(old_clipboard)


def on_release(key):
    current.discard(key)


def perform_keyword_action(keyword, arguments=''):
    if not keyword:
        return
    
    # Strip the trailing backticks `
    keyword, arguments = [x.strip('`') for x in (keyword, arguments)]

    # Checks for the -ne (--no-enter) flag    
    if any(re.findall('-ne|--no-enter', arguments)):
        should_click_enter = False
        arguments = re.sub('-ne|--no-enter', '', arguments).strip()
    else:
        should_click_enter = True
        
    try:
        # Process custom keyword
        if keyword in keywords_custom:
            related_function = KEYWORD_BINDINGS[keyword]
            should_click_enter = related_function(arguments, should_click_enter)
        # Process regular keyword
        else:
            keyword_value = KEYWORD_BINDINGS[keyword]
            replace_keyword_with_value(keyword_value, arguments)
        
    except KeyError as e:
        should_click_enter = False
        click_right()
        keyboard.press(Key.space)
        
        # Type "unknown_keyword_<keyword>" and select it
        err_unknown_keyword = 'unknown_keyword_' + keyword
        keyboard.type(err_unknown_keyword)
        with keyboard.pressed(Key.shift_l, Key.ctrl_l):
            keyboard.press(Key.left)
    
    click_enter() if should_click_enter else None


with open('config/keywords_default.json', 'r') as f:
    keywords_default = json.load(f)

with open('config/keywords_python.json', 'r') as f:
    keywords_python = json.load(f)

# Custom keywords are the ones that are handled differently (with custom functions)
keywords_custom = {
    'dif': replace_dif_keyword_with_question,
}

KEYWORD_BINDINGS: dict = keywords_default | keywords_custom | keywords_python

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
