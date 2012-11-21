from django import template
from sqk.datasets.models import Dataset

register = template.Library()

@register.inclusion_tag('datasets/show_dataset.html')
def show_dataset(dataset):
    instances = dataset.instances.all()
    features = instances[0].features.all()
    return {'instances': instances, 'features': features, }


          