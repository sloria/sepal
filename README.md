
# Sqk web #

## Prerequisites ##

- Python >= 2.5
- [pip][PIP]
- [yaafe][YAAFE]
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

- Install prerequisites
- cd to sqk directory
- Edit compiled.txt to choose your database adapter.
- if windows: install all the exe's in requirements/win64/*
- $ pip install -r requirements/dev.txt
- $ cp sqk/settings/local-dist.py sqk/settings/local.py (local.py shouldn't be added
  to your source control)
- Edit local.py with your local database settings.
- $ ./manage.py syncdb
- $ ./manage.py schemamigration --initial datasets
- $ ./manage.py migrate datasets
- $ ./manage.py runserver


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[PIP]: http://www.pip-installer.org/en/latest/installing.html
[BSD]: http://opensource.org/licenses/BSD-3-Clause
[YAAFE]: http://yaafe.sourceforge.net/