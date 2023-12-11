import json
import logging
import os
import time
from datetime import datetime

from pynput.keyboard import Controller, Key, KeyCode, Listener


logger = logging.getLogger(__name__)
logging.basicConfig(filename='keyword_logger.log', level=logging.INFO)


class KeywordShortener:
    TIMESTAMP_FORMAT = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    RESET_AFTER = 3 # seconds after which the current word will reset
    STOP_KEY = None # Example: Key.esc or KeyCode(char='q')

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
            if key == self.STOP_KEY:
                self.listener.stop()
                logger.info("Timestamp: {}\nKey: {}\nStop key pressed. Script stopped.".format(self.TIMESTAMP_FORMAT, key))
                return

            try:
                if isinstance(key, Key):
                    # If space is pressed, replace the current keyword with its value
                    if key == Key.space:
                        self.replace_keyword_with_value()
    
                    self.modifier_key_pressed = True

                # If `self.RESET_AFTER` seconds have passed, clear the current word
                if time_since_last_press > self.RESET_AFTER:
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

    def load_json_file(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
        
    def load_config(self):
        self.KEYWORD_BINDINGS = {}
        # Load all json files
        json_files = [f for f in os.listdir('config') if f.endswith('.json')]
        for json_file in json_files:
            self.KEYWORD_BINDINGS.update(self.load_json_file(os.path.join('config', json_file)))

    def on_release(self, key):
        if isinstance(key, Key):
            self.modifier_key_pressed = False

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
    