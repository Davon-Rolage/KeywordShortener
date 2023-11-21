import time

import pyperclip
from pynput.keyboard import Controller, Key, KeyCode, Listener

from keyword_functions import *


# left_alt + ` (backtick)
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
        # Do not remove existing time.sleep() functions as they are necessary for proper execution timing.
        time.sleep(0.4)
        
        # Copy the text to clipboard (from where the mouse caret is)
        keyboard_ctrl_a()
        keyboard_ctrl_c()
        
        time.sleep(0.2)
        clipboard_content = pyperclip.paste()
        content_chunks = clipboard_content.split(' ', 1)
        
        clipboard_keyword = content_chunks[0]
        clipboard_arguments = content_chunks[1] if len(content_chunks) > 1 else ''

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
    should_click_enter = False if '-ne' in keyword else True
    keyword = keyword.replace('-ne', '')
    
    try:
        related_function = keyword_bindings[keyword]
        related_function(arguments)
        
    except KeyError:
        should_click_enter = False
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    
    click_enter() if should_click_enter else None


# key: related_function
keyword_bindings = {
    'dif': perform_difference_between,
    'pmr': perform_python_manage_runserver,
    'pmmm': perform_python_manage_makemigrations,
    'pmm': perform_python_manage_migrate,
    'yt': perform_search_youtube,
    'mw': perform_search_merriam_webster,
    'cbd': perform_search_cambridge_dictionary,
}

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
