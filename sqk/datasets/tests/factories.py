import factory
import random
from sqk.datasets.models import *


class DatasetFactory(factory.Factory):
    FACTORY_FOR = Dataset

    name = factory.Sequence(lambda n: "Test dataset {0}".format(n))
    description = "This is a dataset"
    species = "P. californicus"


class InstanceFactory(factory.Factory):
    FACTORY_FOR = Instance

    dataset = factory.SubFactory(DatasetFactory)

    
class FeatureFactory(factory.Factory):
    FACTORY_FOR = Feature

    name = factory.Sequence(lambda n: "feature{0}".format(n))
    unit = "Hz"


class FeatureValueFactory(factory.Factory):
    FACTORY_FOR = FeatureValue

    feature = factory.SubFactory(FeatureFactory)
    instance = factory.SubFactory(InstanceFactory)
    value = random.random()


class LabelNameFactory(factory.Factory):
    FACTORY_FOR = LabelName

    name = "Marital status"


class LabelValueFactory(factory.Factory):
    FACTORY_FOR = LabelValue

    label_name = factory.SubFactory(LabelNameFactory)
    value = "bonded" 


class FullDatasetGenerator(object):
    """Class for quickly creating datasets filled with
    instances, features, values, label names, and label values
    for use in testing.

    Example
    #######
    To create a dataset with 20 instances, each with 5 values and associated 
    features
    >> G = FullDatasetGenerator(n_instances=20)
    >> G.generate_values(n_values=5)
    >> dataset = G.dataset 
    >> assert_true(dataset.pk)
    True

    Each of the values will be a random float.

    To add labels such that half the instances will be labeled 'mutant' and half 
    will be labeled 'wild-type':
    >> G.generate_labels(label_name="Genotype", label_set=['mutant', 'wild-type'])
    """

    def __init__(self, n_instances=3):
        self.dataset = DatasetFactory()
        for i in range(n_instances):
            InstanceFactory(dataset=self.dataset)

    def generate_values(self, n_values=5):
        features = []
        for j in range(n_values):
            f = FeatureFactory()
            features.append(f)

        for i, inst in enumerate(self.dataset.instances.all()):
            for j in range(n_values):
                val = random.random()
                FeatureValue.objects.create(value=val, 
                                            feature=features[j], 
                                            instance=inst)

    def generate_labels(self, label_name='Marital status', label_set=['bonded', 'unbonded']):
        # Create the label names
        label_name_obj = LabelNameFactory(name=label_name)
        for label in label_set:
            LabelValueFactory(label_name=label_name_obj, value=label)

        # Label each instance, cycling through each label in the label set
        for i, inst in enumerate(self.dataset.instances.all()):
            label_value = LabelValue.objects.get(value=label_set[i % len(label_set)])
            inst.label_values.add(label_value)
            label_value.instances.add(inst)
