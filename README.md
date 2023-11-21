# Keyword Shortener

Create custom keyword shortcuts to run in the background, like `dif a b c`, press the hotkey ``Left Alt + ` (backtick)`` to replace it with `What is the difference between "a", "b", and "c"?`


## Sample Video
<img src="./media/sample.gif" width="650" height="200"></img>


## Installation
1. Create a virtual environment and activate it:
```
python -m venv venv
venv\scripts\activate
```
2. Install required dependencies:
```
python -m pip install -r requirements.txt
```


## Run in the background (on Windows)
3. Press `Left Alt + R` and enter `shell:startup`
1. Add a shortcut for `keyword_shortener.pyw` there.
1. Either reboot your computer or do this:
* Open up Task Manager with `Ctrl + Shift + Esc` -> File -> Run new task -> `C:\full\path\to\your\keyword_shortener.pyw`


## Available Keyword Shortcuts
* `dif a, b, c` becomes `What is the difference between "a", "b", and "c"?`
* Most of django's `python manage.py <command>` commands, like:
    - `pmr *args` becomes `python manage.py runserver *args`
    - `pmmkmg *args` becomes `python manage.py makemigrations *args`
    - `pmmg *args` becomes `python manage.py migrate *args`
    - etc...
* `wiki *args` becomes `https://en.wikipedia.org/wiki/*args`
* `yt *args` becomes `https://www.youtube.com/results?search_query=*args`
* `mw *args` becomes `https://www.merriam-webster.com/dictionary/*args`
* `cbd *args` becomes `https://dictionary.cambridge.org/dictionary/english/*args`

> Additionally, one might pass a `-ne | --no-enter` flag after the keyword, which will not press enter after script execution.
<br>For example, `dif -ne a b c` or `dif a b c --no-enter` will type the output message and will not press `Enter` after it.


## Custom Keywords
All regular keywords are stored in `config/keywords_default.json` file where you can specify your own custom keywords and their values.