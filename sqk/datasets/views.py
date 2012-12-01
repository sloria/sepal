from django.views.generic import View, ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404, render

from sqk.datasets.forms import DatasetForm, DatasetEditForm, DatasourceForm
from sqk.datasets.models import *
from sqk.datasets.tasks import read_datasource, handle_uploaded_file, extract_features

## Dataset views

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
            'upload_form': DatasourceForm(),
        }
        context.update(**kwargs)
        return super(DatasetDisplay, self).get_context_data(**context)

class DatasetAddDatasource(FormView, SingleObjectMixin):
    model = Dataset
    form_class = DatasourceForm
    template_name = 'datasets/detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'dataset': self.get_object(),
            'upload_form': self.get_form(DatasourceForm),
        }
        return super(DatasetAddDatasource, self).get_context_data(**context)

    def get_success_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        if form.cleaned_data['csv'] != None:
            f = form.cleaned_data['csv']
            # Save file
            # TODO: might not need to do this
            handle_uploaded_file(f)
            # Parse data and save to database
            read_datasource(self.object, 
                os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name ))
        if form.cleaned_data['audio'] != None:
            f = form.cleaned_data['audio']
            handle_uploaded_file(f)
            extract_features(self.object,
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
        return super(DatasetCreate, self).form_valid(form)

class DatasetEdit(UpdateView):
    model = Dataset
    form_class = DatasetEditForm
    context_object_name = 'dataset'
    template_name='datasets/edit.html'

class DatasetDelete(DeleteView):
    model = Dataset
    template_name='datasets/delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('datasets:index')


## Instance views

class InstanceDetail(DetailView):
    model = Instance
    context_object_name = 'instance'
    template_name = 'instances/detail.html'

    def get_query_set(self):
        dataset = get_object_or_404(Dataset,
            pk=self.kwargs['dataset_id'])
        return Instance.objects.filter(dataset=dataset)

    def get_context_data(self, **kwargs):
        context = super(InstanceDetail, self).get_context_data(**kwargs)
        # context['instance'] =  get_object_or_404(Instance,
        #     pk=self.kwargs['pk'])
        context['dataset'] = self.get_object().dataset
        return context

class InstanceDelete(DeleteView):
    model = Instance
    template_name='instances/delete.html'
    context_object_name = 'object'

    def get_success_url(self):
        return reverse_lazy('datasets:detail', 
            kwargs={'pk': self.kwargs['dataset_id']})


## Feature views
# Class to manage feature lists for datasets
# Model     : Feature (datasets/models.py) 
class LabelNameCreate(FormView, SingleObjectMixin):

    model = LabelName
    form_class = LabelNameForm
    context_object_name = 'label_name'
    template_name = 'features/new_label.html'


    def get_context_data(self, **kwargs):
        # Get context objects that get passed to template
        context = super(InstanceDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.kwargs['dataset_id']
        return context


    def get_context_data(self, **kwargs):
        context = {
            'data_'
            'label_name': self.get_object(),
            'upload_form': self.get_form(LabelNameForm),
        }
        return super(LabelNameCreate, self).get_context_data(**context)

    def form_valid(self, form):
        dataset = self.kwargs['dataset_id']







