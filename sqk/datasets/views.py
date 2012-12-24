import os
from django.views.generic import View, ListView, DetailView, FormView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie
from sqk.datasets.forms import DatasetForm, DatasetEditForm, DatasourceForm
from sqk.datasets.models import *
from sqk.datasets.tasks import read_datasource, handle_uploaded_file, extract_features

############## Dataset views ##################


class DatasetList(ListView):
    model = Dataset
    queryset = Dataset.objects.order_by('-created_at')
    context_object_name = 'all_datasets'
    template_name = 'datasets/index.html'


class DatasetDisplay(DetailView):
    model = Dataset
    context_object_name = 'dataset'
    template_name = 'datasets/detail.html'

    def get_query_set(self):
        return Dataset.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        dataset = self.get_object()
        context = dataset.get_context()
        context['upload_form'] = DatasourceForm()
        context.update(**kwargs)
        return super(DatasetDisplay, self).get_context_data(**context)


class DatasetAddDatasource(FormView, SingleObjectMixin):
    '''View for adding data to a dataset.
    '''
    model = Dataset
    form_class = DatasourceForm
    template_name = 'datasets/detail.html'

    def get_context_data(self, **kwargs):
        dataset = self.get_object()
        print dataset
        context = dataset.get_context()
        context['upload_form'] = self.get_form(DatasourceForm)
        context.update(**kwargs)
        return super(DatasetAddDatasource, self).get_context_data(**context)

    def get_success_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = self.get_object()
        if form.cleaned_data['uploaded_file']:
            f = form.cleaned_data['uploaded_file']
            print 'f in form_valid is type %s' % f.content_type
            # If user uploaded an audio file
            if f.content_type == 'audio/wav':
                # Create new Audio object
                # This uploads the file to media/audio
                audio_obj = Audio(audio_file=f)
                audio_obj.save()
                # Create new instance and associate it with the audio file
                instance = Instance(dataset=self.object)
                instance.audio = audio_obj
                instance.save()
                result = extract_features(self.object.pk, instance.pk,
                    os.path.join(settings.MEDIA_ROOT, 'audio', f.name))
            # If user uploaded a csv file
            elif f.content_type == 'text/csv':
                # Save file
                handle_uploaded_file(f)
                # Parse data and save to database
                read_datasource(self.object,
                    os.path.join(settings.MEDIA_ROOT, 'data_sources', f.name))
        return super(DatasetAddDatasource, self).form_valid(form)


class DatasetDetail(View):
    '''The base dataset detail view. Handles both GET and POST requests
    '''
    def get(self, request, *args, **kwargs):
        view = ensure_csrf_cookie(DatasetDisplay.as_view())
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ensure_csrf_cookie(DatasetAddDatasource.as_view())
        return view(request, *args, **kwargs)


class DatasetCreate(FormView):
    form_class = DatasetForm
    template_name = 'datasets/create.html'
    success_url = reverse_lazy('datasets:index')

    def form_valid(self, form):
        form.save()
        return super(DatasetCreate, self).form_valid(form)


class DatasetEdit(UpdateView):
    model = Dataset
    form_class = DatasetEditForm
    context_object_name = 'dataset'
    template_name = 'datasets/edit.html'


def delete_dataset(request, pk):
    '''View for deleting a dataset.
    '''
    dataset = Dataset.objects.get(pk=pk)
    dataset.delete()
    return HttpResponseRedirect(reverse('datasets:index'))

################ Instance views ####################


class InstanceDetail(DetailView):
    model = Instance
    context_object_name = 'instance'
    template_name = 'instances/detail.html'

    def render_to_response(self, context):
        instance = self.get_object()
        # Assume an instance is ready when it has >= 1 feature
        ready = len(instance.features.all()) >= 1
        if self.kwargs['format'] == 'json':
            return http.HttpResponse(json.dumps({'ready': ready}),  # TODO
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


def instance_ready(request, dataset_id, instance_id):
    '''View for checking if an instance is ready
    '''
    message = {"ready": ''}
    inst = get_object_or_404(Instance, pk=instance_id)
    message['ready'] = inst.as_dict()['ready']
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')


class InstanceRow(DetailView):
    model = Instance
    template_name = 'instances/instance_row.html'

    def get_query_set(self):
        dataset = get_object_or_404(Dataset,
            pk=self.kwargs['dataset_id'])
        return Instance.objects.filter(dataset=dataset)

    def get_context_data(self, **kwargs):
        instance = self.get_object()
        context = super(InstanceDetail, self).get_context_data(**kwargs)
        context['inst'] = instance.as_dict()
        return context


def delete_instances(request, dataset_id):
    '''View for deleting selected instances.

    Must be a POST request.
    '''
    # Get the ids of the selected instances
    if request.is_ajax():
        instance_ids = [int(instance_id) for instance_id in request.POST.getlist('selected[]')]
        for id in instance_ids:
            inst_obj = Instance.objects.get(pk=id)
            inst_obj.delete()
        dataset = Dataset.objects.get(pk=dataset_id)
        dataset.get_data()
        json_data = dataset.get_json_data()
        return HttpResponse(json_data, mimetype='applicationjson')
    else:
        # TODO: handle non-AJAX?
        return HttpResponseRedirect(reverse('datasets:detail', args=(dataset_id,)))


def update_instances_labels(request, dataset_id, label_name_id):
    '''View for updating the label values for selected instances.

    Must be a POST request.
    '''
    # TODO: Make URL and UI for this
    new_label_value = request.POST['new_label'].lower()
    print new_label_value
    if request.is_ajax():
        instance_ids = [int(instance_id) for instance_id in request.POST.getlist('selected[]')]
        for id in instance_ids:
            # Get the instance
            inst = Instance.objects.get(pk=id)
            # Get the label_name
            label_name_obj = get_object_or_404(LabelName, pk=label_name_id)  # the label name
            # Replace the old label value with the new one
            old_label_value_obj = inst.label_values.get(label_name=label_name_obj)
            inst.label_values.remove(old_label_value_obj)
            new_label_value_obj, created = LabelValue.objects.get_or_create(
                                            value=new_label_value,
                                            label_name=label_name_obj)
            inst.label_values.add(new_label_value_obj)
        dataset = Dataset.objects.get(pk=dataset_id)
        dataset.get_data()
        json_data = dataset.get_json_data()
        return HttpResponse(json_data, mimetype='applicationjson')
    else:
        # TODO: handle non-AJAX ?
        return HttpResponseRedirect(reverse('datasets:detail', args=(dataset_id,)))


###################### X-editable views ##################


@ensure_csrf_cookie
def update_name(request, dataset_id):
    '''View for updating the dataset name using X-editable.
    '''
    message = {"name": ''}
    if request.is_ajax():
        # Save new Dataset name
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset.name = request.POST['value']
        dataset.save()
        message['name'] = request.POST['value']

    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')


@ensure_csrf_cookie
def update_description(request, dataset_id):
    '''View for updating the dataset description using X-editable.
    '''
    message = {"description": ''}
    if request.is_ajax():
        description = request.POST['value']
        # Save new Dataset name
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset.description = description
        dataset.save()
        message['description'] = description
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')


@ensure_csrf_cookie
def update_species(request, dataset_id):
    '''View for updating the dataset description using X-editable.
    '''
    message = {"species": ''}
    if request.is_ajax():
        species = request.POST['value']
        # Save new Dataset name
        dataset = get_object_or_404(Dataset, pk=dataset_id)
        dataset.species = species
        dataset.save()
        message['species'] = species
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')


@ensure_csrf_cookie
def update_instance_label(request, instance_id, label_name_id):
    '''View for updating an instance label name using X-editable.
    '''
    message = {"label": ''}
    if request.is_ajax():
        new_label_value = request.POST['value'].lower()  # e.g. u'bonded'
        label_name_obj = get_object_or_404(LabelName, pk=label_name_id)  # the label name
        # Get the instance
        inst = get_object_or_404(Instance, pk=instance_id)
        # Replace the old label value with the new one
        old_label_value_obj = inst.label_values.get(label_name=label_name_obj)
        inst.label_values.remove(old_label_value_obj)
        new_label_value_obj, created = LabelValue.objects.get_or_create(
                                        value=new_label_value,
                                        label_name=label_name_obj)
        inst.label_values.add(new_label_value_obj)
        message['label'] = new_label_value
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')


@ensure_csrf_cookie
def update_label_name(request, dataset_id, label_name_id):
    '''View for updating a label name using X-editable.
    '''
    message = {"name": ''}
    if request.is_ajax():
        new_label_name = request.POST['value']
        label_name_obj = get_object_or_404(LabelName, pk=label_name_id)
        label_name_obj.name = new_label_name
        label_name_obj.save()
        message['name'] = new_label_name
    json = simplejson.dumps(message)
    return HttpResponse(json, mimetype='application/json')
