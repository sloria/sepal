import os
from collections import OrderedDict
from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils import simplejson as json



class LabelName(models.Model):
    '''The name of label (called Variables in the templates), e.g. Marital Status

    NOTE: The name column does not validate uniqueness. This is because different
    datasets should have different LabelName objects associated with them, even if
    the they have the same variable. This ensures that the names will be editable.
    '''
    name = models.CharField(max_length=100, default='no label', blank=True)

    def __unicode__(self):
        return unicode(self.name)


class LabelValue(models.Model):
    '''A value for a label type, e.g. Bachelor
    '''
    label_name = models.ForeignKey(LabelName, related_name='label_values', null=True)
    value = models.CharField(max_length=100, default='none')

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        order_with_respect_to = 'label_name'


class Dataset(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, null=True, blank=True)
    species = models.CharField(max_length=75, null=True, blank=True)
    created_at = models.DateTimeField('created at', default=timezone.now())

    def __init__(self, *args, **kwargs):
        super(Dataset, self).__init__(*args, **kwargs)
        self.data = []

    def __unicode__(self):
        return self.name

    def get_cname(self):
        return 'dataset'

    def get_absolute_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.pk})

    def last_instance(self):
        return self.instances.reverse()[0]

    def sorted_instances(self):
        return self.instances.order_by('pk')

    def values(self):
        '''Returns a 2D array of instance values.

        Example:
        >> dataset.values()
        {1432: ([0.0458984375, 71.7224358880516], {'Marital status',
        1433: [0.23984375, 73.7244358880516]}
        '''
        instance_ids = self.instances.values_list('pk', flat=True).order_by('pk')
        data = {}
        for inst_id in instance_ids:
            data[inst_id] = FeatureValue.objects.filter(
                    instance__id=inst_id).values_list(
                        'value', flat=True).order_by('feature')
        return data

    def get_data(self):
        '''Returns the data as a list of dicts with instance attributes as
        keys and instance values as values.

        Example:
        >> dataset.get_data()

        [{'pk': 1425, 'values': [10.32, 3.4], 'labels': {'marital': 'bonded,}},
         {'pk': 1426, 'values': [10.34, 2.4], 'labels': {'marital': 'unbonded,}},
         ]
        '''
        instances = self.instances.prefetch_related('values',
                                                    'label_values__label_name',
                                                    'audio')
        for inst in instances:
            self.data.append(inst.as_dict())
        return self.data

    # TODO: wasteful to have both get_data and get_json_data. Find out how to make dataset serializable
    def get_json_data(self):
        '''Returns a json representation of the instance data. Used for the D3 visualization.
        NOTE: Dataset.get_data() MUST be called before this method can be called.

        Object has the form:
        {
            "instances" : [
                {
                  "feature_0" : val_0,
                  ...
                  "feature_N" : val_N,
                  "label" : "label_val"
                },
                ...
            ],
            "labels" : [
                "label_0",
                ...
                "label_N"
            ]
        }
        '''
        data = {'instances': [], 'labels': []}
        features = list(self.feature_names())  # list of unicode strings
        for inst in self.data:
            # Feature-value pairs are ordered
            data_instance = OrderedDict()
            for i, value in enumerate(inst['values']):
                feature = features[i].capitalize()
                # "feature": "value"
                data_instance[feature] = value
            # NOTE: Assumes only 1 label_value per dataset (takes the first one)
            label_value = inst['labels'].values()[0].value.upper()
            # Add label to instance data
            data_instance['label'] = label_value
            data['instances'].append(data_instance)
            # Add label to set of known labels if it hasn't yet been added
            if label_value not in data['labels']:
                data['labels'].append(label_value)
        return json.dumps(data)

    def labels(self):
        '''Return a list of the LabelName objects associated with this dataset through its
        instances.
        '''
        if self.instances.exists():
            return self.instances.all()[0].labels().keys()
        else:
            return False

    def feature_names(self):
        '''Returns a list of the feature names (unicode strings) associated with this
        dataset throught its instances.
        '''
        if self.instances.exists():
            return self.instances.latest().feature_names()
        else:
            return False

    def get_context(self, **kwargs):
        '''Get the request context for a dataset detail page.
        Returns a dict of the form:

        {
            'data': ... List of instances in dict representation ...
            'is_empty': False,
            'feature_objects': [<Feature: u'ZCR'>, ...],
            'feature_names': ['ZCR'...],
            'label_names': [<LabelName: u' ],
            'label_name_id': 34,
            'label_name': 'Marital status'
        }
        '''
        context = {
            'data': self.get_data(),
            'dataset': self,
            'is_empty': True
        }
        if self.instances.exists():
            context['data_as_json'] = self.get_json_data()
            context['is_empty'] = False
            # feature_objects is a list of <Feature> objects
            context['feature_objects'] = list(self.instances.latest().feature_objects())
            # feature_names is a list of strings
            context['feature_names'] = list(self.feature_names())
            # label_names is a list of <LabelName> objects
            context['label_names'] = list(self.labels())
            # NOTE: this is assuming only 1 variable per dataset. more in the future
            # the LabelName id
            context['label_name_id'] = self.labels()[0].id
            context['label_name'] = self.labels()[0].name
        return context

    class Meta:
        get_latest_by = "created_at"
        ordering = ["-created_at"]


class Audio(models.Model):
    '''An audio file.

    Relationships:
    instance : one-to-one
    '''
    audio_file = models.FileField(upload_to="audio", null=True, blank=True)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.audio_file.name

    def save(self, *args, **kwargs):
        '''Update slug to audio_file name upon saving the object.
        '''
        self.slug = self.audio_file.name
        super(Audio, self).save(*args, **kwargs)


class Instance(models.Model):
    '''A data instance (table row).

    Relationships:
    dataset : many-to-one
    label_values : many-to-many
    audio : one-to-one
    '''
    dataset = models.ForeignKey(Dataset, related_name='instances')
    label_values = models.ManyToManyField(LabelValue, null=True, blank=True,
                    related_name='instances')
    created_at = models.DateTimeField('created at', default=timezone.now())
    audio = models.OneToOneField(Audio, null=True, blank=True)

    def __unicode__(self):
        return u'pk %s from dataset %s' % (self.pk, self.dataset.pk)

    def get_cname(self):
        return 'instance'

    def feature_names(self):
        '''Returns a list of the feature names (unicode strings) associated
        with this instance, ordered by feature pk.

        Example:
        >> inst.sorted_features()
        [u'zcr', u'spectral spread',]
        '''
        return self.features.values_list('name', flat=True).order_by('pk')

    def feature_objects(self):
        '''Returns a list of feature objects associated with this instance.
        '''
        return self.features.order_by('pk')

    def values_as_list(self):
        '''Returns a list of the values (floats) associated with this
        instance, ordered by feature pk.

        Examples:
        >> inst.values_as_list()
        [0.0458984375, 71.7224358880516]
        '''
        return [v.value for v in self.values.all()]

    def labels(self):
        '''Returns a dict with label names as keys and label values as values.

        Example:
        >> inst.labels()
        {<LabelName: Marital status>: <LabelValue: unbonded>}
        '''
        labels = {}
        for label_value in self.label_values.all():
            label_name = label_value.label_name
            labels[label_name] = label_value
        return labels

    def as_dict(self):
        '''Returns a dict representation of the instance. The dict is of the form:

        {
            'pk': 1425, 
            'values': [10.32, 3.4],
            'labels': {<LabelName: Marital status>: <LabelValue: unbonded>},
            'audio_url': 'media/audio/call.wav',
            'audio_filename': 'call.wav'
        }
        '''
        # Assume instance is ready if it has >= 1 feature
        # ready = len(self.features.all()) >= 1
        ret = {'pk': self.pk,
                'values': self.values_as_list(),
                'labels': self.labels(),
                'created_at': self.created_at,
                # 'ready': ready
                }
        if self.audio:
            ret['audio_url'] = self.audio.audio_file.url
            ret['audio_filename'] = os.path.basename(self.audio.audio_file.name)
        return ret

    class Meta:
        get_latest_by = 'created_at'
        ordering = ['pk']


class Feature(models.Model):
    '''A feature name, e.g. 'Loudness'.

    Relationships:
    instances : many-to-many
    '''
    instances = models.ManyToManyField(
        Instance,
        null=True,
        related_name='features')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
        

class FeatureValue(models.Model):
    '''The value for a feature. Value must be a float.

    Relationships:
    feature : many-to-one (belongs to)
    instance: many-to-one (belongs to)
    '''
    feature = models.ForeignKey(Feature, related_name='values')
    instance = models.ForeignKey(Instance, related_name='values')
    value = models.FloatField()

    def __unicode__(self):
        return unicode(self.value)

    class Meta:
        ordering = ['feature']
