from django.test import TestCase
from tasks import read_datasource
from models import Dataset

class SimpleTest(TestCase):
    def test_simple(self):
        self.assertEqual(1+1,2)

class ReadDataSourceTest(TestCase):
    def setUp(self):
        read_datasource('media/data_sources/iris.csv', label_col=4)

    def test_dataset_created(self):
        self.d = Dataset.objects.get(pk=1)
