import json
import os
import re
import time

import pyperclip
from pynput.keyboard import Controller, Key, KeyCode, Listener

from legacy_custom_keyword_functions import *


class KeywordShortener:
    ARGUMENTS_LENGTH_LIMIT = 100
    TRIGGER_COMBINATIONS = [
        {Key.alt_l, KeyCode(char='`')}, # Left Alt + ` (backtick)
        # Add your hotkeys here
    ]

    def __init__(self):
        self.keyboard = Controller()
        self.current = set()
        self.keyword = ''
        self.arguments = ''

    def on_press(self, key):
        self.current.add(key)
        # Checks if any of the trigger combinations is pressed
        if any(all(k in self.current for k in combo) for combo in self.TRIGGER_COMBINATIONS):
            # If it is, release all keys that were pressed during the trigger combination
            for combo in self.TRIGGER_COMBINATIONS:
                for key in combo:
                    self.keyboard.release(key)
            
            self.current.clear()
            self.execute()

    def on_release(self, key):
        self.current.discard(key)

    def execute(self):
        self.initial_clipboard = pyperclip.paste()
        # Do not remove existing time.sleep() functions. They are necessary for proper execution timing
        time.sleep(0.2)
        self.with_pressed_click(Key.ctrl_l, 'a')
        self.with_pressed_click(Key.ctrl_l, 'c')
        time.sleep(0.2)
        line = pyperclip.paste().strip() 
        within_limit = self.handle_line_elements_extraction(line)
        if within_limit:
            self.perform_keyword_action()
        
        self.arguments = ''
        # Recover old clipboard
        pyperclip.copy(self.initial_clipboard)
    
    def handle_line_elements_extraction(self, line: str) -> bool:
        line_components = line.split(' ', 1)
        self.keyword = line_components[0]
        if len(line_components) > 1:
            self.arguments = line_components[1]
            if len(self.arguments) > self.ARGUMENTS_LENGTH_LIMIT:
                self.keyboard.tap(Key.right)
                return False
            
        self.with_pressed_click(Key.ctrl_l, 'a')
        self.keyboard.tap(Key.delete)
        return True

    def perform_keyword_action(self):
        if not self.keyword:
            return
        
        regex = '-ne|--no-enter'
        self.ne_flags = re.findall(regex, self.arguments)
        self.arguments = re.sub(regex, '', self.arguments)
        should_click_enter = not any(self.ne_flags)
        
        self.keyword = self.keyword.strip('`').strip()
        self.arguments = self.arguments.strip('`').strip()

        try:
            # Process a custom keyword
            if self.keyword in self.keywords_custom:
                related_function = self.KEYWORD_BINDINGS[self.keyword]
                should_click_enter = related_function(self.arguments, should_click_enter)

            # Process a regular keyword
            else:
                keyword_value = self.KEYWORD_BINDINGS[self.keyword]
                self.replace_keyword_with_value(keyword_value)

        except KeyError:
            self.type_error_unknown_keyword()
            self.with_pressed_click([Key.ctrl_l, Key.shift_l], Key.left)
            should_click_enter = False
        
        if should_click_enter:
            self.keyboard.tap(Key.enter)
    
    def replace_keyword_with_value(self, keyword_value: str):
        """
        replace `keyword *args` with `keyword_value *args` 
        """
        self.keyboard.type(keyword_value + self.arguments)
    
    def type_error_unknown_keyword(self):
        err_message = 'unknown_keyword_' + self.keyword
        self.keyboard.type(f'{self.keyword} {self.arguments}')
        if self.arguments:
            self.keyboard.tap(Key.space)
        self.keyboard.type(err_message)
                
    def with_pressed_click(self, keys: list|str, char: str):
        """
        Holds down the specified key(s) followed by a character key tap.
        """
        keys = keys if isinstance(keys, list) else [keys]
        with self.keyboard.pressed(*keys):
            self.keyboard.tap(char)
            
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
            'dif': transform_dif_to_question,
            # Add your custom functions to "custom_keyword_functions.py"
            # and map them here
        }
        self.KEYWORD_BINDINGS.update(self.keywords_custom)

    def run_listener(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        with self.listener:
            self.listener.join()

    def main(self):
        self.load_config()
        self.run_listener()


if __name__ == "__main__":
    keyword_shortener = KeywordShortener()
    keyword_shortener.main()
    