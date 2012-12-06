from django import template
from sqk.datasets.models import Dataset

register = template.Library()

@register.inclusion_tag('datasets/show_dataset.html')
def show_dataset(dataset):
    context = {'dataset': dataset, 'data': dataset.get_data()}
    if dataset.instances.exists():
        context['feature_names'] = list(dataset.last_instance().feature_names())
    return context

@register.inclusion_tag('instances/instance_row.html')
def instance_row(instance):
    return {'instance': instance}


          