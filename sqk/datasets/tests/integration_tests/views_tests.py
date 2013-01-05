"""Tests for the views of the datasets app."""
from django.test import TestCase
from django.core.urlresolvers import reverse
from nose.tools import *

from sqk.datasets.tests.factories import *


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


class DeleteInstancesViewTest(TestCase):
    def setUp(self):
        # Create a dataset with instances
        self.dataset = DatasetFactory()
        inst1, inst2 = InstanceFactory(), InstanceFactory()
        self.dataset.instances.add(inst1)
        self.dataset.instances.add(inst2)
        self.dataset.save()
        self.post_data = {'selected[]': [1, 2]}

    def get_view_name(self):
        return 'datasets:delete_instances'

    def get_view_kwargs(self):
        return {'dataset_id': self.dataset.pk}

    def test_view_deletes_instances_in_db(self):
        # There should be 2 instances in the dataset
        assert_equal(len(self.dataset.instances.all()), 2)
        # Send the request to delete both instances
        response = self.client.post(reverse(self.get_view_name(),
                                    kwargs=self.get_view_kwargs()),
                                    self.post_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                                    )
        # Now there shouldn't be any instances
        assert_equal(len(self.dataset.instances.all()), 0)
