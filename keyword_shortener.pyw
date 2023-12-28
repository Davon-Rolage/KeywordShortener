import glob
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from tkinter.messagebox import askokcancel, showerror

from pynput.keyboard import Controller, Key, KeyCode, Listener


logger = logging.getLogger(__name__)
logging.basicConfig(filename='keyword_logger.log', level=logging.INFO)


class KeywordShortener:
    TIMESTAMP_FORMAT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    RESET_AFTER = 3 # seconds after which self.current_word will be set to ''
    STOP_KEY = None # Example: Key.esc or KeyCode(char='q')
    USE_CUSTOM_KEYWORD_HANDLER = False

    def __init__(self):
        self.keyboard = Controller()
        self.current_word = ''
        self.last_pressed = time.time()
        self.modifier_key_pressed = False

        # Clear the log file when starting the script
        with open('keyword_logger.log', 'w') as f:
            f.write('')
        
    def on_press(self, key):
        current_time = time.time()
        time_since_last_press = current_time - self.last_pressed
        self.last_pressed = current_time
        
        if not self.modifier_key_pressed:
            # If the stop key is pressed, stop the script
            if self.STOP_KEY and key == self.STOP_KEY:
                self.listener.stop()
                logger.info(
                    f"Timestamp: {self.TIMESTAMP_FORMAT}\n"
                    f"Key: {key}\n"
                    "Stop key pressed. Script stopped."
                )
                return

            try:
                if isinstance(key, Key):
                    # If space is pressed, replace the keyword with its value
                    if key == Key.space:
                        self.replace_keyword_with_value()
                        # If a custom keyword handler is used, try to handle the keyword
                        if self.USE_CUSTOM_KEYWORD_HANDLER:
                            if self.current_word in self.handler.CUSTOM_KEYWORD_BINDINGS:
                                self.handler.handle_keyword(self.current_word)

                    self.modifier_key_pressed = True

                # If `self.RESET_AFTER` seconds have passed, clear the current word
                if self.RESET_AFTER and time_since_last_press > self.RESET_AFTER:
                    self.current_word = ''

                # If a character key is pressed, add it to the current word
                if isinstance(key, KeyCode):
                    self.current_word += key.char
                    return
                    
            except Exception as e:
                logger.exception("Timestamp: {}\nKey: {}\nError: {}".format(self.TIMESTAMP_FORMAT, key, e))

            self.current_word = ''
        
    def replace_keyword_with_value(self):
        keyword_value = self.KEYWORD_BINDINGS.get(self.current_word)
        if keyword_value:
            for _ in range(len(self.current_word)+1):
                self.keyboard.tap(Key.backspace)
            time.sleep(0.1)
            self.keyboard.type(keyword_value)
    
    def handle_duplicate_keyword(self, keyword, value) -> bool:
        '''
        If a duplicate keyword is found, prompt the user to take action.
        '''
        info_title = 'Duplicate Keyword'
        info_message = (
            f'Duplicate keyword "{keyword}" found:\n'
            f'1) {self.KEYWORD_BINDINGS[keyword]}\n'
            f'2) {value}\n\n'
            f'The second value will be used.'
        )
        return askokcancel(title=info_title, message=info_message)
    
    def handle_recursive_keyword(self, keyword, value, file_path):
        error_title = 'Potential Recursion Error'
        error_message = (
            f'Please change the following keyword to avoid recursion:\n\n'
            f'{keyword}: {value}\n\n'
            f'{file_path}'
        )
        showerror(title=error_title, message=error_message)

    def load_keywords(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
            
        for keyword, value in keywords.items():
            # Check for duplicate keywords
            if keyword in self.KEYWORD_BINDINGS:
                proceed = self.handle_duplicate_keyword(keyword, value)
                if proceed:
                    self.KEYWORD_BINDINGS[keyword] = value
                else:
                    self.config_fail = True
                    return
            # Check for recursive keywords
            if keyword in value.split():
                full_path = Path(f.name).resolve()
                self.handle_recursive_keyword(keyword, value, full_path)
                self.config_fail = True
                return

            self.KEYWORD_BINDINGS[keyword] = value
        
    def load_json_files(self, json_files):
        for file_path in json_files:
            self.load_keywords(file_path)
        
    def load_config(self):
        self.KEYWORD_BINDINGS = {}
        json_files = glob.glob('config/*.json')
        self.load_json_files(json_files)
        
        if self.USE_CUSTOM_KEYWORD_HANDLER:
            from custom_keyword_handler import CustomKeywordHandler
            self.handler = CustomKeywordHandler()

    def on_release(self, key):
        if isinstance(key, Key):
            self.modifier_key_pressed = False
    
    def run_listener(self):
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        with self.listener:
            self.listener.join()

    def main(self):
        self.load_config()
        self.run_listener() if not hasattr(self, 'config_fail') else None


if __name__ == "__main__":
    keyword_shortener = KeywordShortener()
    keyword_shortener.main()
    