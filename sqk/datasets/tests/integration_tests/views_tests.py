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
    
    def test_datasets_page_has_names_and_species(self):
        response = self.client.get(reverse(self.get_view_name()))
        self.assertTemplateUsed(response, 'datasets/index.html')

        # check the datasets appear on the page
        assert_in(self.dataset_1.name, response.content)
        assert_in(self.dataset_1.species, response.content)
        assert_in(self.dataset_1.description, response.content)
        assert_in(self.dataset_2.name, response.content)
        assert_in(self.dataset_2.species, response.content)
        assert_in(self.dataset_2.description, response.content)



# TODO: test all views

