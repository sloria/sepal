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

    name = factory.Sequence(lambda n: "feature name {0}".format(n))

class FeatureValueFactory(factory.Factory):
    FACTORY_FOR = FeatureValue

    feature = factory.SubFactory(FeatureFactory)
    instance = factory.SubFactory(InstanceFactory)
    value = random()

# TODO: create factory for all models


