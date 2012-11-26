import os
from django.views.generic import View, ListView, DetailView, FormView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from sqk.datasets.forms import DatasetForm, DatasetEditForm, DatasourceForm
from sqk.datasets.models import Dataset, Instance
from sqk.datasets.tasks import read_datasource, handle_uploaded_file

class DatasetList(ListView):
    model = Dataset
    queryset = Dataset.objects.order_by('-created_at')
    context_object_name = 'all_datasets'
    template_name='datasets/index.html'

class DatasetDisplay(DetailView):
    model = Dataset
    context_object_name = 'dataset'
    template_name = 'datasets/detail.html'
    def get_context_data(self, **kwargs):
        context = {
            'form': DatasourceForm(),
        }
        context.update(**kwargs)
        return super(DatasetDisplay, self).get_context_data(**context)

class DatasetAddDatasource(FormView, SingleObjectMixin):
    model = Dataset
    form_class = DatasourceForm
    template_name = 'datasets/detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'object': self.get_object(),
        }
        return super(DatasetAddDatasource, self).get_context_data(**context)

    def get_success_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        if form.cleaned_data['source'] != None:
            f = form.cleaned_data['source']
            handle_uploaded_file(f)
            read_datasource(self.object, 
                os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name ))
        return super(DatasetAddDatasource, self).form_valid(form)


class DatasetDetail(View):
    def get(self, request, *args, **kwargs):
        view = DatasetDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = DatasetAddDatasource.as_view()
        return view(request, *args, **kwargs)


class DatasetCreate(FormView):
    form_class = DatasetForm
    template_name='datasets/create.html'
    success_url= reverse_lazy('datasets:index')

    def form_valid(self, form):
        d = form.save()
        if form.cleaned_data['source'] != None:
            f = form.cleaned_data['source']
            # TODO: Might not need to save uploaded file
            # Save file
            handle_uploaded_file(f)
            # Parse data and save to database
            read_datasource.delay(d, 
                os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name ))
        return super(DatasetCreate, self).form_valid(form)

class DatasetEdit(UpdateView):
    model = Dataset
    form_class = DatasetEditForm
    context_object_name = 'dataset'
    template_name='datasets/edit.html'

class DatasetDelete(DeleteView):
    model = Dataset
    template_name='datasets/delete.html'
    context_object_name = 'dataset'
    success_url = reverse_lazy('datasets:index')

class InstanceDetail(DetailView):
    model = Instance
    context_object_name = 'instance'
    template_name = 'instances/detail.html'


