from django.views.generic import CreateView
from sqk.datasets.forms import DatasetForm
from sqk.datasets.models import Dataset

class DatasetCreate(CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name='datasets/create.html'
    success_url='/datasets/' #TODO: remove this and dfine get_absolute_url()

