from django import template
from sqk.datasets.models import Dataset

register = template.Library()

@register.inclusion_tag('datasets/show_dataset.html')
def show_dataset(dataset):
    return {'dataset': dataset}

@register.inclusion_tag('instances/instance_row.html')
def instance_row(instance):
    return {'instance': instance}


          