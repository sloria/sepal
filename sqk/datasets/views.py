from django.views.generic import ListView, DetailView, FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.core.files import File
from sqk.datasets.forms import DatasetForm, DatasetEditForm
from sqk.datasets.models import Dataset
from sqk.datasets.tasks import read_datasource

class DatasetList(ListView):
    model = Dataset
    queryset = Dataset.objects.order_by('-created_at')
    context_object_name = 'all_datasets'
    template_name='datasets/index.html'

class DatasetDetail(DetailView):
    model = Dataset
    context_object_name = 'dataset'
    template_name='datasets/detail.html'

class DatasetCreate(FormView):
    form_class = DatasetForm
    template_name='datasets/create.html'
    success_url= reverse_lazy('datasets:index')

    def form_valid(self, form):
        d = form.save()
        read_datasource.delay(d, d.source.path)
        return super(DatasetCreate, self).form_valid(form)

class DatasetEdit(UpdateView):
    model = Dataset
    form_class = DatasetEditForm
    template_name='datasets/edit.html'

class DatasetDelete(DeleteView):
    model = Dataset
    template_name='datasets/delete.html'
    context_object_name = 'dataset'
    success_url = reverse_lazy('datasets:index')
