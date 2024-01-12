from pynput.keyboard import Controller, Key


class CustomKeywordHandler:
    def __init__(self):
        self.keyboard = Controller()
        self.CUSTOM_KEYWORD_BINDINGS = {
            'dbash': (self.move_cursor_left_and_insert_space, 5),
            'x-to-say': self.tis_very_x_to_say,
        }

    def handle_keyword(self, keyword: str) -> None:
        '''
        Calls a related function with args (if any) based on the given keyword.
        '''
        binding = self.CUSTOM_KEYWORD_BINDINGS.get(keyword)
        if binding:
            # If the binding is a tuple, the first element is the function to call
            # and the rest of the elements are the arguments to pass to the function
            if isinstance(binding, tuple):
                related_method, *method_args = binding
                related_method(*method_args)
            # Otherwise, the binding should be a function
            else:
                binding()
    
    def n_taps(self, key: Key, num_taps: int=1) -> None:
        """
        Taps the given `key` `num_taps` times.

        Parameters:
            key (Key): The key to tap.
            num_taps (int, optional): The number of times to tap the key. Defaults to 1.
        """
        for _ in range(num_taps):
            self.keyboard.tap(key)
    
    def with_pressed_click(self, keys: list, target) -> None:
        """
        Performs a click action while holding down the specified keys.

        Parameters:
            keys (list): The key(s) to be pressed while performing the click action.
            target: The target key to be clicked.
        """
        with self.keyboard.pressed(*keys):
            self.keyboard.tap(target)
    
    def move_cursor_one_word(self, *, to_left: bool=True) -> None:
        """
        Moves the cursor one word to the left or right.

        Parameters:
            to_left (bool): If True, moves the cursor one word to the left, otherwise to the right. Defaults to True.
        """
        select_direction = Key.left if to_left else Key.right
        self.with_pressed_click([Key.ctrl_l], select_direction)
    
    def select_word(self, *, to_left=True) -> None:
        """
        Selects a word in the editor.

        Parameters:
            to_left (bool): If True, selects the word to the left, otherwise to the right. Defaults to True.
        """
        select_direction = Key.left if to_left else Key.right
        self.with_pressed_click([Key.ctrl_l, Key.shift_l], select_direction)

    def move_cursor_left_and_insert_space(self, num_taps: int):
        '''
        This is an example class method that accepts one parameter.\n
        Moves cursor left `num_taps` times and then inserts a space.
        '''
        self.n_taps(Key.left, num_taps)
        self.keyboard.tap(Key.space)
    
    def tis_very_x_to_say(self):
        '''
        This is an example class method that doesn't accept any parameters.\n
        The related value is `That's very generous of you to say`\n
        Moves cursor to the end of the `generous` word and then selects it.
        '''
        for _ in range(4):
            self.move_cursor_one_word()
        
        self.keyboard.tap(Key.left)
        self.select_word()


if __name__ == '__main__':
    from time import sleep
    sleep(3)

    # Test how `tis_very_x_to_say` method works
    test_keyword = 'x-to-say'
    handler = CustomKeywordHandler()
    handler.keyboard.type("That's very generous of you to say")
    handler.handle_keyword(keyword=test_keyword)
    