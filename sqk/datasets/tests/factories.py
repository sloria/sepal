import factory
from random import random
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
    value = random()


class LabelNameFactory(factory.Factory):
    FACTORY_FOR = LabelName

    name = "Marital status"


class LabelValueFactory(factory.Factory):
    FACTORY_FOR = LabelValue

    label_name = factory.SubFactory(LabelNameFactory)
    value = "bonded" 


class FullDatasetFixture(object):
    def __init__(self):
        self.dataset = DatasetFactory()
        # Create some instances
        self.instance1 = InstanceFactory(dataset=self.dataset)
        self.instance2 = InstanceFactory(dataset=self.dataset)
        self.instance3 = InstanceFactory(dataset=self.dataset)
        # Create some features
        self.feature_1 = FeatureFactory(name='duration')
        self.feature_2 = FeatureFactory(name='zcr', display_name='ZCR')
        self.feature_3 = FeatureFactory(name='spectral centroid')
        # Create some values
        self.instance1.values.add(FeatureValueFactory(feature=self.feature_1, value=101))
        self.instance1.values.add(FeatureValueFactory(feature=self.feature_2, value=102))
        self.instance1.values.add(FeatureValueFactory(feature=self.feature_3, value=103))

        self.instance2.values.add(FeatureValueFactory(feature=self.feature_1, value=51.2))
        self.instance2.values.add(FeatureValueFactory(feature=self.feature_2, value=52.3))
        self.instance2.values.add(FeatureValueFactory(feature=self.feature_3, value=53.4))

        self.instance3.values.add(FeatureValueFactory(feature=self.feature_1, value=0.12))
        self.instance3.values.add(FeatureValueFactory(feature=self.feature_2, value=0.34))
        self.instance3.values.add(FeatureValueFactory(feature=self.feature_3, value=0.56))

        # Create some labels and label values
        ln = LabelNameFactory(name='Marital status')
        lv1 = LabelValueFactory(label_name=ln, value='bonded')
        lv2 = LabelValueFactory(label_name=ln, value='unbonded')
        # Associate label values with instances - one label value each

        # Instance 1 is 'bonded'
        self.instance1.label_values.add(lv1)
        self.instance1.save()
        lv1.instances.add(self.instance1)
        lv1.save()
        # Instance 2 is 'unbonded'
        self.instance2.label_values.add(lv2)
        self.instance2.save()
        lv2.instances.add(self.instance2)
        lv2.save()
        # Instance 3 is 'bonded'
        self.instance3.label_values.add(lv1)
        self.instance3.save()
        lv1.instances.add(self.instance1)
        lv1.save()

