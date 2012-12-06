import os
from django.views.generic import View, ListView, DetailView, CreateView, FormView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson as json
from django import http

from sqk.datasets.forms import DatasetForm, DatasetEditForm, DatasourceForm, LabelNameForm
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
    
    def get_query_set(self):
        return Dataset.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        dataset = self.get_object()
        context = {
            'upload_form': DatasourceForm(),
            'data': dataset.get_data()
        }
        if self.get_object().instances.exists():
            context['feature_objects'] = list(dataset.last_instance().feature_objects())
            context['feature_names'] = list(dataset.last_instance().feature_names())
        context.update(**kwargs)
        return super(DatasetDisplay, self).get_context_data(**context)

class DatasetAddDatasource(FormView, SingleObjectMixin):
    '''View for adding data to a dataset.
    '''
    model = Dataset
    form_class = DatasourceForm
    template_name = 'datasets/detail.html#visualization'

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
        instance = Instance.objects.create(
                dataset=self.object,
                species=self.object.species)
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
            extract_features.delay(instance,
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

    def render_to_response(self, context):
        if self.kwargs['format'] == 'json':
            return http.HttpResponse(json.dumps({'ready': False}), # TODO
                                     content_type='application/json',
                                     **httpresponse_kwargs)
        else:
            return super(InstanceDetail, self).render_to_response(context)

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

class InstanceRow(DetailView):
    model = Instance
    template_name = 'instances/instance_row.html'

    def get_query_set(self):
        dataset = get_object_or_404(Dataset,
            pk=self.kwargs['dataset_id'])
        return Instance.objects.filter(dataset=dataset)

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
class LabelNameCreate(FormView):
    form_class = LabelNameForm
    context_object_name = 'label_name'
    template_name = 'features/new_label.html'

    def get_context_data(self, **kwargs):
        # Get context objects that get passed to template
        context = super(LabelNameCreate, self).get_context_data(**kwargs)
        context['dataset'] = Dataset.objects.get(pk=self.kwargs['dataset_id'])
        context['upload_form'] = self.get_form(LabelNameForm)
        return context

    def form_valid(self, form): # TODO: getorcreate everything
        dataset, created = Dataset.objects.get_or_create(pk=self.kwargs['dataset_id'])
        # Save the new label object and associate with dataset
        label, created = LabelName.objects.get_or_create(name=form.cleaned_data['name'])
        label.datasets.add(dataset)
        # Add the associated values
        value_1_obj, created = LabelValue.objects.get_or_create(value=form.cleaned_data['value1'])
        value_2_obj, created = LabelValue.objects.get_or_create(value=form.cleaned_data['value2'])
        label.label_values.add(value_1_obj)
        label.label_values.add(value_2_obj)
        label.save()
        return super(LabelNameCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('datasets:detail', 
            kwargs={'pk': self.kwargs['dataset_id']})







