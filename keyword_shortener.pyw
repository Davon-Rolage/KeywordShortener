import json
import os
import re
import time

import pyperclip
from pynput.keyboard import Controller, Key, KeyCode, Listener

from custom_keyword_functions import *


class KeywordShortener:
    TRIGGER_COMBINATIONS = [
        {Key.alt_l, KeyCode(char='`')}, # Left Alt + ` (backtick)
        # Add your own hotkeys here
    ]

    def __init__(self):
        self.keyboard = Controller()
        self.current = set()

    def on_press(self, key):
        # Checks if any of the trigger combinations are pressed
        if any([key in COMBO for COMBO in self.TRIGGER_COMBINATIONS]):
            self.current.add(key)
            if any(all(k in self.current for k in COMBO) for COMBO in self.TRIGGER_COMBINATIONS):
                self.execute()

    def on_release(self, key):
        self.current.discard(key)

    def execute(self):
        old_clipboard = pyperclip.paste()
        # Do not remove existing time.sleep() functions. They are necessary for proper execution timing
        time.sleep(0.5)
        # Copy the text to clipboard (from where the mouse caret is)
        self.keyboard_ctrl_a()
        self.keyboard_ctrl_c()
        time.sleep(0.3)
        
        new_clipboard = pyperclip.paste()
        clipboard_keyword, *clipboard_arguments = re.split(r'\s', new_clipboard, 1)
        clipboard_arguments = str(clipboard_arguments[0]) if clipboard_arguments else ''
        
        self.perform_keyword_action(clipboard_keyword, clipboard_arguments)
        
        self.current.clear()
        # Recover old clipboard
        pyperclip.copy(old_clipboard)

    def perform_keyword_action(self, keyword, arguments=''):
        if not keyword:
            return
        
        # Strip trailing backticks `
        keyword, arguments = [x.strip('`') for x in (keyword, arguments)]
        
        # Checks for the -ne (--no-enter) flag and removes it
        regex = '-ne|--no-enter'
        self.ne_flags = re.findall(regex, arguments)
        if any(self.ne_flags):
            should_click_enter = False
            arguments = re.sub(regex, '', arguments)
            
        else:
            should_click_enter = True
            
        try:
            arguments = arguments.strip()
            # Process a custom keyword
            if keyword in self.keywords_custom:
                related_function = self.KEYWORD_BINDINGS[keyword]
                should_click_enter = related_function(arguments, should_click_enter)

            # Process a regular keyword
            else:
                keyword_value = self.KEYWORD_BINDINGS[keyword]
                self.replace_keyword_with_value(keyword_value, arguments)

        except KeyError:
            should_click_enter = False
            self.keyboard_ctrl_end()
            self.click_backspace() # Delete the trailing ` (backtick)
            self.keyboard.press(Key.space)
            # Type "unknown_keyword_<keyword>" and select it
            err_unknown_keyword = 'unknown_keyword_' + keyword
            self.keyboard.type(err_unknown_keyword)
            self.keyboard_ctrl_shift_left()
        
        self.click_enter() if should_click_enter else None
    
    def replace_keyword_with_value(self, value: str, arguments: str = '') -> None:
        """
        replace `keyword *args` with `value *args` 
        """
        self.delete_keyword_and_args(n=len(arguments))
        self.keyboard.type(value + arguments)

    def keyboard_ctrl_a(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press('a')
            self.keyboard.release('a')

    def keyboard_ctrl_c(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press('c')
            self.keyboard.release('c')
    
    def keyboard_ctrl_end(self):
        with self.keyboard.pressed(Key.ctrl_l):
            self.keyboard.press(Key.end)
            self.keyboard.release(Key.end)
    
    def keyboard_ctrl_shift_left(self, n=1):
        with self.keyboard.pressed(Key.ctrl_l, Key.shift_l):
            for _ in range(n):
                self.keyboard.press(Key.left)
                self.keyboard.release(Key.left)

    def click_enter(self, n=1):
        for _ in range(n):
            self.keyboard.press(Key.enter)
            self.keyboard.release(Key.enter)
    
    def click_backspace(self, n=1):
        for _ in range(n):
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
    
    def delete_keyword_and_args(self, n=1):
        """
        Delete the whole string with the keyword, arguments, and the -ne flag if it exists
        """
        # Delete all arguments
        for _ in range(n):
            self.click_backspace()
        
        # Delete all -ne flags if they exist
        for ne_flag in self.ne_flags:
            self.click_backspace(len(ne_flag)+1)
        
        # Delete the keyword
        with keyboard.pressed(Key.ctrl):
            self.click_backspace()
            
    def load_json_file(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
        
    def load_config(self):
        self.KEYWORD_BINDINGS = {}
        # Load all json files
        json_files = [f for f in os.listdir('config') if f.endswith('.json')]
        for json_file in json_files:
            self.KEYWORD_BINDINGS.update(self.load_json_file(os.path.join('config', json_file)))

        # Custom keywords are the ones that are handled differently (with custom functions)
        self.keywords_custom = {
            'dif': replace_dif_keyword_with_question,
            # Add your custom functions to "custom_keyword_functions.py"
            # and map them here
        }
        self.KEYWORD_BINDINGS.update(self.keywords_custom)

    def run_listener(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def main(self):
        self.load_config()
        self.run_listener()


if __name__ == "__main__":
    keyword_shortener = KeywordShortener()
    keyword_shortener.main()
    