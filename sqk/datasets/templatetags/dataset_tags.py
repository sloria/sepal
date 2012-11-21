from django import template
from sqk.datasets.models import Dataset

def show_dataset(parser, token):
    try:
        tag_name, pk = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument", % token.contents.split_contents()[0])
    return DatasetNode(pk)

class DatasetNode(template.Node):
    def __init__(self, pk):
        self.dataset = Dataset.objects.get(primary_key=pk)
    def render(self, context):
        features = 
          