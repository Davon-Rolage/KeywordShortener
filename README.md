# Keyword Shortener

Create custom keyword shortcuts to run in background like `dif a b c`, press ``<left_alt> + ` (backtick)`` to replace it with `What is the difference between "a", "b", and "c"?`

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
3. (on Windows) to be able to use keywords in the background, press `<left_alt> + R` and enter `shell:startup`
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

> Additionally, one might pass a `-ne` (--no-enter) flag which will not press enter after script execution.
<br>For example, `dif-ne a b c` will type the output message and will not press `Enter` after it.