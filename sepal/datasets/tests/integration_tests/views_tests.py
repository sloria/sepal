"""Tests for the views of the datasets app."""
from django.test import TestCase
from django.core.urlresolvers import reverse
from nose.tools import *

from sepal.base.tests.factories import UserFactory
from sepal.datasets.tests.factories import *


class DatasetListViewTest(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.dataset_1 = DatasetFactory(user=self.user)
        self.dataset_2 = DatasetFactory(user=self.user)
        self.client.login(username=self.user.username,
                            password='abc')

    def get_view_name(self):
        """
        Convenience method so that if the name of this url is changed in
         'urls.py' you would only have to change this string at this central position.
        """
        return 'datasets:index'

    def test_view(self):
        print self.user.username
        print self.user.email
        print self.user.password
        print self.user.is_authenticated()
        response = self.client.get(reverse(self.get_view_name()))
        print response
        self.assertEqual(response.status_code, 200)


class UpdateVisualizationViewTest(TestCase):
    def setUp(self):
        self.dataset = DatasetFactory()

    def get_view_name(self):
        return 'datasets:load_data'

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
        inst1 = InstanceFactory(dataset=self.dataset)
        inst2 = InstanceFactory(dataset=self.dataset)
        self.post_data = {'selected[]': [3, 4]}

    def get_view_name(self):
        return 'datasets:delete_instances'

    def get_view_kwargs(self):
        return {'pk': self.dataset.pk}

    def test_view_deletes_instances(self):
        # There should be 2 instances in the dataset
        assert_equal(len(self.dataset.instances.all()), 2)
        # Send the request to delete both instances
        self.client.post(reverse(self.get_view_name(),
                                    kwargs=self.get_view_kwargs()),
                                    self.post_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                                    )
        # Now there shouldn't be any instances in the database
        assert_equal(len(self.dataset.instances.all()), 0)


class DeleteDatasetViewTest(TestCase):
    def setUp(self):
        # Create a dataset with instances
        self.dataset = DatasetFactory()
        inst1, inst2 = InstanceFactory(dataset=self.dataset), InstanceFactory(dataset=self.dataset)

    def get_view_name(self):
        return 'datasets:delete_dataset'

    def get_view_kwargs(self):
        return {'pk': self.dataset.pk}

    def test_view_deletes_the_dataset(self):
        # There should be 1 dataset with 2 instances
        assert_equal(len(Dataset.objects.all()), 1)
        assert_equal(len(self.dataset.instances.all()), 2)
        # Send the request to delete the dataset
        self.client.get(reverse(self.get_view_name(),
                                    kwargs=self.get_view_kwargs())
                                    )
        # There should be no more datasets in the db
        assert_equal(len(Dataset.objects.all()), 0)
        # There also shouldn't be any instances
        assert_equal(len(self.dataset.instances.all()), 0)


class UpdateInstanceLabelTest(TestCase):
    def setUp(self):
        # Create a dataset with instances
        self.dataset = DatasetFactory()
        self.inst1 = InstanceFactory(dataset=self.dataset)
        # instance has a label and value
        self.label_name = LabelName.objects.create(name='Marital status')
        self.label_value = LabelValue.objects.create(label_name=self.label_name, 
                                                    value='unbonded')
        self.label_value.instances.add(self.inst1)
        self.inst1.label_values.add(self.label_value)
        self.post_data = {'value': 'sIngle aNd Ready 2 mINGLE'}

    def get_view_name(self):
        return 'datasets:update_instance_label'

    def get_view_kwargs(self):
        return {'dataset_id': self.dataset.pk, 
                'instance_id': self.inst1.pk,
                'label_name_id': self.label_name.pk}

    def test_view_updates_label_value(self):
        # Get the old label (the first label value)
        old_label = self.inst1.label_values.all()[0].value
        # The innstances label value is 'unbonded'
        assert_equal(old_label, 'unbonded')
        # Send the request to delete both instances
        self.client.post(reverse(self.get_view_name(),
                                    kwargs=self.get_view_kwargs()),
                                    self.post_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                                    )
        # Now ther
        new_label = self.inst1.label_values.all()[0].value
        assert_equal(new_label, 'single and ready 2 mingle')


class UpdateLabelNameTest(TestCase):
    def setUp(self):
        # Create a dataset with instances
        self.dataset = DatasetFactory()
        self.inst1 = InstanceFactory(dataset=self.dataset)
        # instance has a label and value
        self.label_name = LabelName.objects.create(name='Marital status')
        self.label_value = LabelValue.objects.create(label_name=self.label_name, 
                                                    value='unbonded')
        self.label_value.instances.add(self.inst1)
        self.inst1.label_values.add(self.label_value)
        self.post_data = {'value': 'Bonding status'}

    def get_view_name(self):
        return 'datasets:update_label_name'

    def get_view_kwargs(self):
        return {'dataset_id': self.dataset.pk,
                'label_name_id': self.label_name.pk}

    def test_view_updates_label_name(self):
        # Get the old label (the first label value)
        old_label_name = self.dataset.labels()[0].name
        # The instances label value is 'unbonded'
        assert_equal(old_label_name, 'Marital status')
        # Send the request to delete both instances
        self.client.post(reverse(self.get_view_name(),
                                    kwargs=self.get_view_kwargs()),
                                    self.post_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest'
                                    )
        # The label name should be updated in the db
        new_label_name = self.dataset.labels()[0].name
        assert_equal(new_label_name, self.post_data['value'])
