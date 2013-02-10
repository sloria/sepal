
# Sepal #

## Prerequisites ##

- Python >= 2.5
- [pip][PIP]
- [yaafe][YAAFE]
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

- Install prerequisites
- cd to sepal directory
- Optional: Edit compiled.txt to choose your database adapter. Skip this to use sqlite
- If windows: install all the exe's in requirements/win64/*
- `$ pip install -r requirements/dev.txt`
- `$ cp sepal/settings/local-dist.py sepal/settings/local.py` (so that local.py won't be added
  to your source control)
- Edit local.py with your local database settings.
- `$ python manage.py syncdb`
- `$ python manage.py schemamigration --initial datasets`
- `$ python manage.py migrate datasets`
- `$ python manage.py runserver`

## Running tests ##
- Run tests using `$ fab test`


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[PIP]: http://www.pip-installer.org/en/latest/installing.html
[BSD]: http://opensource.org/licenses/BSD-3-Clause
[YAAFE]: http://yaafe.sourceforge.net/