from django.views.generic import ListView, DetailView, CreateView
from sqk.datasets.forms import DatasetForm
from sqk.datasets.models import Dataset

class DatasetList(ListView):
    model = Dataset
    queryset = Dataset.objects.order_by('-created_at')
    context_object_name = 'all_datasets'
    template_name='datasets/index.html'

class DatasetDetail(DetailView):
    model = Dataset
    context_object_name = 'dataset'
    template_name='datasets/detail.html'

class DatasetCreate(CreateView):
    model = Dataset
    form_class = DatasetForm
    template_name='datasets/create.html'
    success_url='/datasets/' #TODO: remove this and dfine get_absolute_url()

    # TODO: 
    # def form_valid(self, form):
        # add read_dataset to task queue


