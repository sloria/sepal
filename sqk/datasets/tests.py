from django.test import TestCase
from tasks import read_datasource
from models import *

class ReadDataSourceTest(TestCase):
    def setUp(self):
        self.d = Dataset.objects.create(name='iris-data')
        self.d.save()
        read_datasource(self.d, 
            'media/data_sources/iris.csv',
            label_col=4,
            feature_row=0)

    def test_dataset_created(self):
        self.assertEqual(Dataset.objects.count(), 1)
        data = Dataset.objects.get(name='iris-data')

