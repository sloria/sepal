""" Unit tests for the datasets models """
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from nose.tools import assert_equal, assert_in, assert_true
from sqk.datasets.models import *
from sqk.datasets.tests.factories import *


class DatasetTestCase(TestCase):
    def test_model(self):
        dataset = DatasetFactory()
        assert_true(dataset.pk)
        assert_true(dataset.description)
        assert_true(dataset.species)

    def test_creating_and_saving_a_dataset(self):
        dataset = Dataset()
        dataset.name = "New dataset"
        dataset.species = "P. californicus"
        dataset.description = "This is a test dataset."
        dataset.created_at = timezone.now()

        dataset.save()

        all_datasets = Dataset.objects.all()

        # Check that dataset was saved
        assert_equal(len(all_datasets), 1)
        only_dataset = all_datasets[0]
        assert_equal(only_dataset, dataset)

        # Check that attributes got saved
        assert_equal(only_dataset.name, "New dataset")
        assert_equal(only_dataset.species, "P. californicus")
        assert_equal(only_dataset.created_at, dataset.created_at)


class FeatureTestCase(TestCase):
    def test_model(self):
        feature = FeatureFactory()
        assert_true(feature.pk)

    def test_adding_instances(self):
        feature = FeatureFactory()
        instance_1 = InstanceFactory()
        feature.instances.add(instance_1)

        assert_equal(len(feature.instances.all()), 1)    

        instance_2 = InstanceFactory()
        feature.instances.add(instance_2)

        assert_equal(len(feature.instances.all()), 2)

    # TODO: test display_name attribute
