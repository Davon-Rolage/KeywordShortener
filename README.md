<div align = "center">

<img src="./media/logo.png" height="200"></img>

<h1>KeywordShortener</h1>

<p>Coding is about creativity, not keyboard acrobatics</p>

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

</div>


## Description
Create custom keyword shortcuts and run them in the background. For example, type `pipfromreqs`, press the hotkey ``Left Alt + ` (backtick)`` to replace it with `python -m pip install -r requirements.txt`


## Sample Video
<img src="./media/sample.gif" width="650" height="200"></img>


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
* Most of django's `python manage.py <command>` commands, like:
    - `pmr *args` -> `python manage.py runserver *args`
    - `pmmkmg *args` -> `python manage.py makemigrations *args`
    - `pmmg *args` -> `python manage.py migrate *args`
* `? love` -> `What is love`
* `gramcor between you and I` -> `Does it sound grammatically correct? between you and I`
* `dif a, b, c` -> `What is the difference between "a", "b", and "c"?`
* `mw indict` -> `https://www.merriam-webster.com/dictionary/indict`
* and many more...

> Additionally, you can pass the `-ne | --no-enter` flag after the keyword, which will not press `Enter` after script execution.
<br>For example, `? -ne hash` or `? hash --no-enter` will type `What is hash` and will not press `Enter`


## Create Your Own Keywords
All regular keywords are stored in the `config` folder where you can specify your own keywords and their values.
<br>
They are separated into different json files only for convenience. The only thing you should do is either create a custom json file or modify the existing ones.
<br>
> You can add your own hotkeys by modifying the `TRIGGER_COMBINATIONS` attribute of the `KeywordShortener` class.


## Limitations
To avoid unexpected keyboard behavior, the limit for the `ARGUMENTS_LENGTH_LIMIT` was set to `100` characters, i.e. if you accidentally activate a hotkey, it will not freeze the keyboard until the whole text is typed.