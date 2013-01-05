""" Unit tests for the datasets models """
import os
from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse
from nose.tools import *
from sqk.datasets.models import *
from sqk.datasets.tests.factories import *
from django.db import IntegrityError
from sqk.datasets.utils import filter_by_key, find_dict_by_item
from sqk.datasets.tasks import extract_features


class DatasetTest(TestCase):
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


class FeatureTest(TestCase):
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

    def test_name_uniqueness(self):
        FeatureFactory(name='spectral centroid')

        with self.assertRaises(IntegrityError):
            FeatureFactory(name='spectral centroid')
        
    def test_display_name_defaults_to_capitalized_name(self):
        feature_1 = FeatureFactory(name="spectral centroid")
        assert_equal(feature_1.display_name, "Spectral centroid")

    def test_can_set_display_name(self):
        feature = FeatureFactory(name="zcr")
        assert_equal(feature.display_name, "Zcr")
        feature.display_name = "ZCR"
        feature.save()
        assert_equal(feature.display_name, "ZCR")

    def test_can_set_unit(self):
        feature = FeatureFactory(name="zcr")
        assert_false(feature.unit)
        feature.unit = "Hz"
        feature.save()
        assert_equal(feature.unit, "Hz")


class UtilsTest(TestCase):
    def setUp(self):
        self.dicts = [{'duration': 1, 'ss': 2}, {'duration': 3, 'ss': 4}]

    def test_filter_by_key(self):
        assert_equal(filter_by_key('duration', self.dicts), [1, 3])

    def test_find_dict_by_item(self):
        assert_equal(
                        find_dict_by_item(('duration', 3), self.dicts),
                        {'duration': 3, 'ss': 4}
                    )

        assert_is_none(
                        find_dict_by_item(('duration', 5), self.dicts)
                    )


class TasksTest(TestCase):
    def setUp(self):
        self.audio_file_name = 'ex.wav'

    def tearDown(self):
        try:
            # Delete all the files uploaded in the tests
            tmp_files = glob(os.path.join(settings.MEDIA_ROOT,
                                 'audio',  
                                 '{}*.wav'.format(self.audio_file_name.split('.')[0])))
            for f in tmp_files:
                os.remove(f)
        except:
            pass

    def test_extract_features(self):
        # Create a dataset and an instance
        dataset = DatasetFactory()
        instance = InstanceFactory()
        dataset.instances.add(instance)
        dataset.save()
        # The file path of the test audio file
        file_path = os.path.join(
                            os.path.abspath(os.path.dirname(__file__)),
                            self.audio_file_name
                    ) 
        # Extract the features
        extract_features(dataset.pk, instance.pk, file_path)
        # The duration, rate, and ZCR
        duration = Feature.objects.get(name='duration')
        duration_value = instance.values.get(feature=duration)

        sample_rate = Feature.objects.get(name='sample rate')
        sample_rate_value = instance.values.get(feature=sample_rate)

        spec_centroid = Feature.objects.get(name='spectral centroid')
        spec_centroid_value = instance.values.get(feature=spec_centroid)

        zcr = Feature.objects.get(name='zcr')
        zcr_value = instance.values.get(feature=zcr)
        # Test that the values are correct
        assert_equal(round(duration_value.value, 3), 9.639)
        assert_equal(round(sample_rate_value.value, 3), 11025.000)
        assert_equal(round(spec_centroid_value.value, 3), 112.283)
        assert_equal(round(zcr_value.value, 3), 0.061)

        # The features should have correct units
        assert_equal('s', duration.unit)
        assert_equal('Hz', sample_rate.unit)
        assert_equal("Hz", zcr.unit)
