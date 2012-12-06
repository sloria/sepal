from django import template
from sqk.datasets.models import Dataset

register = template.Library()

@register.inclusion_tag('datasets/show_dataset.html')
def show_dataset(dataset):
    context = {'dataset': dataset}
    if dataset.instances.exists():
        context['features'] = list(dataset.last_instance().sorted_features())
    return context


          