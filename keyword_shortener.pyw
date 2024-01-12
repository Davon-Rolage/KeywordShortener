import glob
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from tkinter.messagebox import askokcancel, askyesnocancel, showerror

from pynput.keyboard import Controller, Key, KeyCode, Listener


logger = logging.getLogger(__name__)
logging.basicConfig(filename='keyword_logger.log', level=logging.INFO)


class KeywordShortener:
    TIMESTAMP_FORMAT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    VALUE_LENGTH_LIMIT = 300 # characters. If the value is longer, warn the user
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
                    # If space is pressed, replace current_word with its related value
                    if key == Key.space:
                        self.replace_keyword_with_value()
                        # If a custom keyword handler is used, try to handle the keyword
                        if self.USE_CUSTOM_KEYWORD_HANDLER:
                            if self.current_word in self.custom_handler.CUSTOM_KEYWORD_BINDINGS:
                                self.custom_handler.handle_keyword(self.current_word)

                    # If backspace is pressed, remove the last character
                    if key == Key.backspace:
                        self.current_word = self.current_word[:-1]
                    
                    # If any other modifier Key is pressed, reset current_word
                    else:
                        self.current_word = ''
                        
                    self.modifier_key_pressed = True

                # If `self.RESET_AFTER` seconds have passed, clear the current word
                if self.RESET_AFTER and time_since_last_press > self.RESET_AFTER:
                    self.current_word = ''

                # If a character key is pressed, add it to the current word
                if isinstance(key, KeyCode):
                    self.current_word += key.char
                    
            except Exception as e:
                logger.exception("Timestamp: {}\nKey: {}\nError: {}".format(self.TIMESTAMP_FORMAT, key, e))

        
    def replace_keyword_with_value(self) -> None:
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
            'Duplicate keyword "{}" found:\n'
            '1) {}\n'
            '2) {}'
        ).format(keyword, self.KEYWORD_BINDINGS[keyword], value)
        detail = '- Yes to choose the first value.\n- No to choose the second value.\n- Cancel to stop the script.'
        option = askyesnocancel(title=info_title, message=info_message, detail=detail)
        return option
    
    def handle_recursive_keyword(self, keyword, value, file_path) -> None:
        '''
        If a recursive keyword is found, notify the user and stop the script.
        '''
        self.config_fail = True
        error_title = 'Potential Recursion Error'
        error_message = (
            'Please change the following keyword to avoid recursion:\n\n'
            f'{keyword}: {value}'
        )
        showerror(title=error_title, message=error_message, detail=file_path)
    
    def handle_long_keyword_value(self, keyword, value, full_path) -> None:
        '''
        If a keyword value contains more than `VALUE_LENGTH_LIMIT` characters, prompt the user to take action.
        '''
        info_title = 'Keyword Value Is Longer Than %s Characters' % self.VALUE_LENGTH_LIMIT
        info_message = (
            'Found a keyword "{}" whose value is longer than {} characters (it has {} characters).\n'
            'Such long values may freeze the keyboard until the whole text is typed.\n\n'
            '- Press Ok to ignore this warning.\n- Press Cancel to prevent the script from running.\n\n'
            '{}\n\n'
            '{}'
        ).format(keyword, self.VALUE_LENGTH_LIMIT, len(value), value, full_path)
        detail = "You may change the character upper limit by changing the value of `self.VALUE_LENGTH_LIMIT` attribute of KeywordShortener class."
        proceed = askokcancel(
            title=info_title, message=info_message,
            icon='warning', default='cancel', detail=detail
        )
        return proceed
    
    def check_for_collisions(self, keyword, value, full_path):
        # Check for recursive keywords
        if keyword in value.split():
            self.handle_recursive_keyword(keyword, value, full_path)
            return True
        
        # Check for duplicate keywords
        if keyword in self.KEYWORD_BINDINGS:
            option = self.handle_duplicate_keyword(keyword, value)
            if option is not None:
                if not option:
                    # If user chose No, overwrite the value
                    self.KEYWORD_BINDINGS[keyword] = value
            else:
                self.config_fail = True
            return True

        # Check for long keyword values
        if self.VALUE_LENGTH_LIMIT and len(value) > self.VALUE_LENGTH_LIMIT:
            proceed = self.handle_long_keyword_value(keyword, value, full_path)
            if proceed:
                self.KEYWORD_BINDINGS[keyword] = value
            else:
                self.config_fail = True
                return True

        return False

    def load_keywords(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            keywords = json.load(f)
            full_path = Path(f.name).resolve()
            
        for keyword, value in keywords.items():
            has_collisions = self.check_for_collisions(keyword, value, full_path)
            if not has_collisions:
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
            self.custom_handler = CustomKeywordHandler()

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
    