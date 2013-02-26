""" Unit tests for the datasets app"""
import os
from collections import OrderedDict
from django.test import TestCase
from django.utils import timezone, simplejson
from django.core.urlresolvers import reverse
from nose.tools import *
from django.db import IntegrityError
from sepal.datasets.utils import filter_by_key, find_dict_by_item
from sepal.datasets.tasks import extract_features

from sepal.base.tests.factories import UserFactory
from sepal.datasets.models import *
from sepal.datasets.tests.factories import *


class DatasetTest(TestCase):
    def test_model(self):
        dataset = DatasetFactory()
        assert_true(dataset.pk)
        assert_true(dataset.description)
        assert_true(dataset.species)

    def test_creating_and_saving_a_dataset(self):
        dataset = Dataset()
        dataset.user = UserFactory()
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

    def test_get_json_data(self):
        # Dataset is created
        dataset = Dataset.objects.create(name='P. californicus USVs',
                                            user=UserFactory())
        # It has instances 
        inst1 = Instance.objects.create(dataset=dataset)
        inst2 = Instance.objects.create(dataset=dataset)
        # The instance has a duration
        duration = Feature.objects.create(name='duration')
        duration_val1 = FeatureValue.objects.create(feature=duration,
                                            instance=inst1, 
                                            value=12.34)
        duration_val2 = FeatureValue.objects.create(feature=duration,
                                    instance=inst2, 
                                    value=56.78)
        # And ZCR
        zcr = Feature.objects.create(name='zcr', display_name='ZCR')
        zcr_val1 = FeatureValue.objects.create(feature=zcr, 
                                            instance=inst1,
                                            value=567.890)
        zcr_val2 = FeatureValue.objects.create(feature=zcr, 
                                            instance=inst2,
                                            value=123.456)

        # instance has a label and value
        marital = LabelName.objects.create(name='Marital status')
        bonded = LabelValue.objects.create(label_name=marital, value='bonded')
        bonded.instances.add(inst1)
        inst1.label_values.add(bonded)
        unbonded = LabelValue.objects.create(label_name=marital, value='unbonded')
        unbonded.instances.add(inst2)
        inst2.label_values.add(unbonded)


        dataset_dict = {
                            "instances": [
                                OrderedDict([
                                  ("Duration", duration_val1.value),
                                  ("ZCR", zcr_val1.value),
                                  ("label", bonded.value.upper()),
                                  ("pk", inst1.pk)
                                ]),
                                OrderedDict([
                                  ("Duration", duration_val2.value),
                                  ("ZCR", zcr_val2.value),
                                  ("label", unbonded.value.upper()),
                                  ("pk", inst2.pk)
                                ])
                            ],
                            "labels": [
                                bonded.value.upper(),
                                unbonded.value.upper()
                            ]
                        }
        json = simplejson.dumps(dataset_dict)
        assert_equal(dataset.get_json_data(), json)


class InstanceTest(TestCase):
    def setUp(self):
        self.instance = InstanceFactory()

    def test_feature_names(self):
        # Create 2 features with values
        feature1 = Feature.objects.create(name='zcr', display_name='ZCR')
        feature2 = Feature.objects.create(name='duration')
        value1 = FeatureValueFactory(feature=feature1, instance=self.instance)
        value2 = FeatureValueFactory(feature=feature2, instance=self.instance)
        # feature_names() should return a list of display names
        assert_equal(self.instance.feature_names(), ['Duration', 'ZCR'])


class FeatureTest(TestCase):
    def test_model(self):
        feature = FeatureFactory()
        assert_true(feature.pk)

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
        feature = FeatureFactory(name="zcr", unit=None)
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


class FullDatasetGeneratorTest(TestCase):
    def setUp(self):
        self.G = FullDatasetGenerator(n_instances=5)

    def test_generate_instances(self):
        assert_equal(len(self.G.dataset.instances.all()), 5)

    def test_generate_values(self):
        self.G.generate_values(3)
        # An instance in the dataset has 3 values
        assert_equal(len(self.G.dataset.instances.latest().values_as_list()), 3)
        # The dataset has 3 features
        assert_equal(len(self.G.dataset.feature_names()), 3)

        # The values of each instance should be different from each other
        instances = self.G.dataset.instances.all()
        assert_not_equal(instances[0].values.all()[0], instances[1].values.all()[0])
        # The values within an instance should be different from each other
        assert_not_equal(instances[0].values.all()[0], instances[0].values.all()[1])

    def test_generate_labels(self):
        self.G.generate_labels('Marital', ['bonded', 'unbonded', 'none'])
        assert_equal(len(self.G.dataset.labels()), 1)
        instances = self.G.dataset.instances.all()
        # The first instance is bonded
        assert_equal(instances[0].label_values.all()[0].value, u'bonded')
        # The seconded isntance is unbonded
        assert_equal(instances[1].label_values.all()[0].value, u'unbonded')
        # The third instance has label 'none'
        assert_equal(instances[2].label_values.all()[0].value, u'none')
        # The fourth instance is bonded (the cycle starts again)
        assert_equal(instances[3].label_values.all()[0].value, u'bonded')
