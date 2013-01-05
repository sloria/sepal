"""Tests for the views of the datasets app."""
from django.test import TestCase
from django.core.urlresolvers import reverse
from nose.tools import assert_equal, assert_in, assert_true

from sqk.datasets.tests.factories import DatasetFactory


class DatasetListViewTest(TestCase):
    def setUp(self):
        self.dataset_1 = DatasetFactory()
        self.dataset_2 = DatasetFactory()

    def get_view_name(self):
        """
        Convenience method so that if the name of this url is changed in
         'urls.py' you would only have to change this string at this central position.
        """
        return 'datasets:index'

    def test_view(self):
        response = self.client.get(reverse(self.get_view_name()))
        self.assertEqual(response.status_code, 200)

class UpdateVisualizationViewTest(TestCase):
    def setUp(self):
        self.dataset = DatasetFactory()

    def get_view_name(self):
        return 'datasets:update_visualization'

    def get_view_kwargs(self):
        """
        Similar to get_view_name. If the url args change, only need
        to change this return value
        """
        return {'pk': self.dataset.pk}

    def test_view(self):
        response = self.client.get(reverse(self.get_view_name(),
                                kwargs=self.get_view_kwargs()))
        assert_equal(response.status_code, 200)
