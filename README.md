
# Sqk web #

## About ##


## Prerequisites ##

- Python >= 2.5
- pip
- [yaafe][YAAFE]
- virtualenv (virtualenvwrapper is recommended for use during development)

## Installation ##

- Install prerequisites
- cd to sqk directory
- $ pip install -r requirements/dev.txt
- $ cp sqk/settings/local-dist.py sqk/settings/local.py (local.py shouldn't be added
  to your source control)
- $ ./manage.py syncdb
- $ ./manage.py runserver


License
-------
This software is licensed under the [New BSD License][BSD]. For more
information, read the file ``LICENSE``.

[BSD]: http://opensource.org/licenses/BSD-3-Clause
[YAAFE]: http://yaafe.sourceforge.net/