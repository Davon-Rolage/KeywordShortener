<div align = "center">

<img src="./media/logo.png" height="200"></img>

<h1>KeywordShortener</h1>

<p>Coding is about creativity, not keyboard acrobatics</p>

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

</div>


## Description
Define custom keywords and assign them specific commands. For example, type `pipfreqs` and press `Space` to replace it with `python -m pip install -r requirements.txt`


## Sample Video
<img src="media/preview.gif"></img>


## Installation
1. Create a virtual environment and activate it:
```
python -m venv venv && venv\Scripts\activate
```
2. Install required dependencies:
```
python -m pip install -r requirements.txt
```
3. Run the script in the background:
```
pythonw keyword_shortener.pyw
```
> To run the script in the terminal, use `python` instead of `pythonw`


## Run on startup (Windows)
4. To run the script in the background on startup, you will have to install `pynput` and `pyperclip` to the global environment (100 Kb):
```
deactivate && pip install -r requirements.txt
```
5. Press `Win + R` and enter `shell:startup`
1. Add a shortcut for `keyword_shortener.pyw` there.
1. Either reboot your computer or run:
```
pythonw keyword_shortener.pyw
```
> To stop the script, open up Task Manager with `Ctrl + Shift + Esc` -> Details.<br>Find the `pythonw.exe` process and end it.


## Keyword Shortcuts Examples
| Keyword | Corresponding value |
| ------- | ------------- |
| pmr | python manage.py runserver |
| djproj | django-admin startproject |
| pmmkmg | python manage.py makemigrations |
| pmmg | python manage.py migrate |
| pyvenvact | python -m venv venv && venv\\scripts\\activate |
| pipfreqs | python -m pip install -r requirements.txt |
| dcupb | docker-compose up --build |
| gramcor | Does it sound grammatically correct? |
| mw | https://www.merriam-webster.com/dictionary/ |


## Create Your Own Keywords
All keywords are stored in the `config` folder where you can specify your own keywords and values.
<br>
Make sure your value doesn't contain its key to avoid recursion. For example, the following json file would've ended up with an infinite loop of the strings "That's a coolThat's a coolThat's a cool", because the word "cool" is in both key and value:
```json
{
    "cool": "That's a cool idea"
// --> "That's a coolThat's a coolThat's a cool..."
}
```
In this case, a `Potential Recursion Error` will pop up and the script will not run.
* If your keys are repeated in *different* files, a `Duplicate Keyword` info message will pop up and prompt you to choose one of the values.
* If your keys are repeated in the same file, the second value will have precedence. This is a feature of JSON.
* Also, it is **not** recommended to mix other keys in the values like this:
```json
{
    "hi": "hello dear traveller",
    "hinana": "and i said hi to my grandma"
// --> hinana
// Possible output:
// --> "and i said hi to my granhello dear traveller"
}
```

> [!NOTE]
> Be wary when creating keys that require the use of modifier keys (Shift, Ctrl, etc.), such as the underscore `_`. The current implementation resets `self.current_word` when you press any modifier key.


## Pressing Enter and executing multiple commands at once
To simulate pressing `Enter` when replacing a keyword, include `\n` in your value. For example, if you'd like to generate a random number in python shell, your json file might look like this:
```json
{
    "pygenrand": "python\nimport random\nprint(random.random())\n"
}
```
So pynput treats every `\n` as a newline and presses `Enter`. It is useful when you want to press Enter right after the script typed your value.
<br>
> [!IMPORTANT]
> Keep in mind, that pynput types the keyword value without a pause. So if you have several commands and one of them takes some time to execute, it's not going to work.

If you want to run multiple commands in a sequence, it's better to write all your commands in one line with a `&&` separator or using python's `-c` (command) flag, like this:
```json
{
    "mkdjango": "python -m venv venv && venv\\Scripts\\activate && python -m pip install django && django-admin startproject myproj . && python manage.py startapp myapp && python manage.py runserver\n",
    "pygenrand": "python -c \"import random; print(random.random())\"\n"
}
```
* `mkdjango` key will successfully create and activate a virtual environment, install Django, start a new project, create a new app and run a server.
* `pygenrand` key will execute lines inside the `-c` flag (entering the shell), print a random number and automatically exit the shell.


## Limitations
1. When you press a `Backspace` key even once, `self.current_word` is set to an empty string. It is an intentional behavior since there is no way for the script to know (without complicating the code) whether you previously selected the whole string with `Ctrl + A` for example, hence deleting not one, but multiple characters.
1. Keywords are keyboard layout insensitive meaning that pynput only registers button pressing, not the actual value of the keys you are pressing, so `qwerty` and `йцукен` are considered the same keyword, because you need to press the same keys to type it:
```json
{
    "yt": "youtube"
}
```
Here, if you type "не" ("yt" in Russian layout), the output will be "нщгегиу".


## Custom Keyword Handler
If you want to tweak the output of a certain keyword, like press `Left` a few times or select a certain word after typing the value, set `USE_CUSTOM_KEYWORD_HANDLER` attribute to `True` (defaults to `False`).
<br>
In `custom_keyword_handler.py` you can define your own methods for any keyword.
<br><br>
For example, `dbash` keyword's value is `docker exec -it bash` and it is handled by `move_cursor_left_and_insert_space` method with `num_taps=5` argument. This method presses `Left` 5 times and presses `Space` so that your mouse caret is ready to type the <container_name>:

<img src="media/custom_handler.gif" width="379" height="200"></img>


## How does it work?
1. When JSON files are loaded, three types of checks are performed: for recursive keywords, for duplicate keywords, and for long keywords (ones that contain more than `VALUE_LENGTH_LIMIT` characters, defaults to `300`). If either of these checks is triggered, a message box will pop up. It can create a `config_fail` attribute which will be used to prevent the script from running.
1. When the script starts, set `self.current_word = ''`.
1. When you press any key, `time_since_last_press` is calculated.
1. Check if any modifier key, like `Ctrl`, is pressed (but not released).
* If it is, no further code is executed. It is there to ensure that when you press `Ctrl+A`, for example, the 'A' is not appended to the current_word.
> [!NOTE]  
> Because of this, when defining your keywords, you can't use characters that require a pressed `Shift`, like an underscore `_`, but you can use hyphens `-` instead.
5. Check if the pressed key is `self.STOP_KEY`.
* If it is, stop the script completely (end the process).
6. Check if the pressed key belongs to the `pynput.keyboard.Key` class (whether it is a modifier key, like Shift).
* If it is a modifier key, check if it is `Space`.
* If it is, execute the main `replace_keyword_with_value` method. It tries to find `self.current_word` key in the `self.KEYWORD_BINDINGS` dictionary. If there is such a key, press Backspace for every character in the `self.current_word` + 1 (for the Space) and type the corresponding keyword value.
* if `self.USE_CUSTOM_KEYWORD_HANDLER = True`, try to handle the keyword as defined in `custom_keyword_handler.py`.
7. Set `self.current_word = ''`
8. Check if the elapsed time between key presses `time_since_last_press` exceeds `self.RESET_AFTER` limit.
* If it does, set `self.current_word = ''`.
9. Check if the pressed key is a character key, like `a` or `1`.
* If it is, concatenate this character to `self.current_word`.
10. If any exception occurred during the key press, log this exception to `keyword_logger.log` file with the exception timestamp, pressed key and the exception message.


# Legacy Version
Previously, `KeywordShortener` included hotkey activation and copying current window's content to the clipboard which proved to be inefficient and prone to occasional keyboard freezes when clipboard contained a lot of text. You can find legacy code in the `legacy` folder. Here is the legacy documentation.


### Description (legacy)
Create custom keyword shortcuts and run them in the background. For example, type `pipfreqs`, press the hotkey ``Left Alt + ` (backtick)`` to replace it with `python -m pip install -r requirements.txt`
> Additionally, you can pass the `-ne | --no-enter` flag after the keyword, which will not press `Enter` after script execution.
<br>For example, `? -ne hash` or `? hash --no-enter` will type `What is hash` and will not press `Enter`


### Sample Video (legacy)
<img src="media/preview_legacy.gif"></img>


### Create Your Own Keywords (legacy)
All regular keywords are stored in the `config` folder where you can specify your own keywords and their values.
<br>
They are separated into different json files only for convenience. The only thing you should do is either create a custom json file or modify the existing ones.
<br>
> You can add your own hotkeys by modifying the `TRIGGER_COMBINATIONS` attribute of the `KeywordShortener` class.


### Limitations (legacy)
To avoid unexpected keyboard behavior, the limit for the `ARGUMENTS_LENGTH_LIMIT` was set to `100` characters, i.e. if you accidentally activate a hotkey, it will not freeze the keyboard until the whole text is typed.