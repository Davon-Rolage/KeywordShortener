from pynput.keyboard import Controller, Key


class CustomKeywordHandler:
    def __init__(self):
        self.keyboard = Controller()
        self.CUSTOM_KEYWORD_BINDINGS = {
            'dbash': self.handle_docker_bash,
        }

    def handle_keyword(self, keyword: str):
        '''
        Executes a custom action based on the given keyword.
        '''
        if keyword in self.CUSTOM_KEYWORD_BINDINGS:
            self.CUSTOM_KEYWORD_BINDINGS[keyword]()
    
    def n_taps(self, key: Key, n: int=1):
        for _ in range(n):
            self.keyboard.tap(key)

    def handle_docker_bash(self):
        self.n_taps(Key.left, 5)
        self.keyboard.tap(Key.space)
