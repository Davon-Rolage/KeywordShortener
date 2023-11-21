# Keyword Shortener

Create custom keyword shortcuts to run in the background like `dif a b c`, press ``Left Alt + ` (backtick)`` to replace it with `What is the difference between "a", "b", and "c"?`


## Sample Video
<img src="./media/sample.gif" width="700" height="300"></img>


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
* `dif a, b, c` becomes `What is the difference between "a", "b", and "c"?`,
* `pmr *args` becomes `python manage.py runserver *args`,
* `pmmm *args` becomes `python manage.py makemigrations *args`,
* `pmm *args` becomes `python manage.py migrate *args`,
* `yt <query>` becomes `https://www.youtube.com/results?search_query=<query>`,
* `mw <word>` becomes `https://www.merriam-webster.com/dictionary/<word>`,
* `cbd <word>` becomes `https://dictionary.cambridge.org/dictionary/english/<word>`

> Additionally, one might pass a `-ne | --no-enter` flag after the keyword which will not press enter after script execution.
<br>For example, `dif -ne a b c` or `dif a b c --no-enter` will type the output message and will not press `Enter` after it.
