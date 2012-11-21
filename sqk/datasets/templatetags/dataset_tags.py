from django import template
from sqk.datasets.models import Dataset

register = template.Library()

@register.inclusion_tag('datasets/show_dataset.html')
def show_dataset(dataset):
    instances = dataset.instance_set.all()
    features = instances[0].feature_set.all()
    return {'instances': instances, 'features': features}


          