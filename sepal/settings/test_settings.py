# flake8: noqa
"""Settings to be used for running tests."""
import os

from sepal.settings import *


INSTALLED_APPS.append('django_nose')

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
SOUTH_TESTS_MIGRATE = False

TEST_RUNNER = 'sepal.testrunner.NoseCoverageTestRunner'
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
    'sepal.base.management',
    'sepal.coffeescript',
    'sepal.celerytest',
    'sepal.datasets.templatetags',
    'sepal.base.templatetags',
    'sepal.datasets.wsgi'
]
NOSE_ARGS = ['--verbosity=2']

COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(__file__, '../../../coverage')
