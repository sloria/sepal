from django.core.files import File
from celery import task

# TODO
@task()
def read_datasource(source):
    with open(source, 'r') as s:
        data = File(s)
        for line in data:
            print line