<div align = "center">

<img src="./media/logo.png" height="200"></img>

<h1>KeywordShortener</h1>

<p>Coding is about creativity, not keyboard acrobatics</p>

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

</div>


## Description
Create custom keywords to replace them with custom values and run this script in the background. For example, type `pipfreqs` and press `Space` to replace it with `python -m pip install -r requirements.txt`


## Sample Video
<img src="media/demo.gif"></img>


## Installation
1. Create a virtual environment and activate it:
```
python -m venv venv && venv\scripts\activate
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


## Run on startup (on Windows)
4. To run the script in the background on startup, you will have to install `pynput` and `pyperclip` to the global environment (100 Kb):
```
deactivate
pip install -r requirements.txt
```
5. Press `Win + R` and enter `shell:startup`
1. Add a shortcut for `keyword_shortener.pyw` there.
1. Either reboot your computer or run:
```
pythonw keyword_shortener.pyw
```
> To stop the script, open up Task Manager with `Ctrl + Shift + Esc` -> Details.<br>Find the `pythonw.exe` process and end it.


## Keyword Shortcuts Examples
| Keyword | Keyword value |
| ------- | ------------- |
| pmr | python manage.py runserver |
| djproj | django-admin startproject |
| pmmkmg | python manage.py makemigrations |
| pmmg | python manage.py migrate |
| covtest | coverage run manage.py test |
| pyvenvact | python -m venv venv && venv\\scripts\\activate |
| pipfreqs | python -m pip install -r requirements.txt |
| dcupb | docker-compose up -d --build |
| gramcor | Does it sound grammatically correct? |
| mw | https://www.merriam-webster.com/dictionary/ |
> and many more...


## Create Your Own Keywords
All keywords are stored in the `config` folder where you can specify your own keywords and their values.
<br>
They are separated into different json files only for convenience. The only thing you should do is either create a custom json file or modify the existing ones.


## Limitations
When you press a `Backspace` key even once, `self.current_word` is set to an empty string. It is an intentional behavior since there is no way for the script to know (without complicating the code) whether you previously selected the whole string with `Ctrl + A` for example, hence deleting not one, but multiple characters.


## How does it work?
1. When the script starts, `self.current_word` is set to an empty string.
1. When you press any key, `time_since_last_press` variable is calculated (in seconds).
1. Check if any modifier key (like `Ctrl`) is pressed.
* If it is, no further script is executed.
4. Check if `self.STOP_KEY` is pressed.
* If it is, stop the script completely.
5. Check if the pressed key belongs to the `pynput.keyboard.Key` class (whether it is a modifier key, like `Ctrl`).
* If it is a modifier key, check if it is `Space`
* If it is, execute the main `replace_keyword_with_value` method that tries to find `self.current_word` key in the `self.KEYWORD_BINDINGS` dictionary. If there is such a key, press `Backspace` for every character in the `self.current_word` + 1 (for the Space) and type the found keyword value.
6. Check if the elapsed time between key presses (`time_since_last_press`) exceeds `self.RESET_AFTER` limit.
* If it does, set `self.current_word` to an empty string.
7. Check if the pressed key is a character key, like `a` or `1`
* If it is, concatenate this key to `self.current_word` and return None.
8. If any exception occurred during the key press, log this exception to `keyword_logger.log` file with the exception timestamp, pressed key and the exception message.
9. Set `self.current_word` to an empty string.


# Legacy Version
Previously, `KeywordShortener` included hotkey activation and copying current window's content to the clipboard which proved to be inefficient and prone to occasional keyboard freezes when clipboard contained a lot of text. You can find legacy code in the `legacy` folder. Here is the documentation for this legacy version code.


### Description (legacy)
Create custom keyword shortcuts and run them in the background. For example, type `pipfreqs`, press the hotkey ``Left Alt + ` (backtick)`` to replace it with `python -m pip install -r requirements.txt`
> Additionally, you can pass the `-ne | --no-enter` flag after the keyword, which will not press `Enter` after script execution.
<br>For example, `? -ne hash` or `? hash --no-enter` will type `What is hash` and will not press `Enter`


### Sample Video (legacy)
<img src="media/sample.gif"></img>


### Create Your Own Keywords (legacy)
All regular keywords are stored in the `config` folder where you can specify your own keywords and their values.
<br>
They are separated into different json files only for convenience. The only thing you should do is either create a custom json file or modify the existing ones.
<br>
> You can add your own hotkeys by modifying the `TRIGGER_COMBINATIONS` attribute of the `KeywordShortener` class.


### Limitations (legacy)
To avoid unexpected keyboard behavior, the limit for the `ARGUMENTS_LENGTH_LIMIT` was set to `100` characters, i.e. if you accidentally activate a hotkey, it will not freeze the keyboard until the whole text is typed.