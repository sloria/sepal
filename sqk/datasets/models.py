from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

class LabelName(models.Model):
    '''The name of label (called Variables in the templates), e.g. Marital Status
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

class Species(models.Model):
    name = models.CharField(max_length=100, default='')
    def __unicode__(self):
        return self.name

class Dataset(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, null=True, blank=True)
    species = models.ForeignKey(Species, null=True, blank=True,
                                related_name='datasets')
    # TODO: Dataset should have many label names. Or just treat them like features (no relationship to dataset)
    # label_name = models.ForeignKey(LabelName, null=True, related_name='datasets')
    created_at = models.DateTimeField('created at', default=timezone.now())
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
    # def labels(self):
    #     '''Returns a list of dicts corresponding to the label_name:label_value 
    #     pairs for each instance in this dataset.

    #     Example:
    #     >> dataset.labels()
    #     [{u'marital status': u'bonded', u'genotype': u'homozygous'},
    #     {u'marital status': u'bachelor', u'genotype': u'heterozygous'}
    #     ...]
    #     '''
    #     return [inst.labels() for inst in self.instances.order_by('pk')]
    def get_data(self):
        '''Returns the data as a list of dicts with instance attributes as 
        keys and instance values as values.

        Example:
        >> dataset.get_data()

        [{'pk': 1425, 'values': [10.32, 3.4], 'labels': {'marital': 'bonded,}},
         {'pk': 1426, 'values': [10.34, 2.4], 'labels': {'marital': 'unbonded,}},
         ]
        '''
        data = []
        for inst in self.instances.order_by('pk'):
            data.append({'pk': inst.pk, 
                        'values': inst.values_as_list(), 
                        'labels': inst.labels()})
        return data
    class Meta:
        get_latest_by = "created_at"


class Instance(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='instances')
    species = models.ForeignKey(Species, related_name='instances')
    label_values = models.ManyToManyField(LabelValue, null=True, blank=True,
                    related_name='instances')
    def __unicode__(self):
        return u'pk %s from dataset %s' %(self.pk, self.dataset.pk)
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
        return self.values.values_list('value', flat=True).order_by('feature')
    def labels(self):
        '''Returns a dict with label names as keys and label values as values.
        '''
        labels = {}
        for label_value in self.label_values.order_by('pk'):
            label_name = label_value.label_name
            labels[label_name] = label_value
        return labels
    class Meta:
        get_latest_by = 'pk'

# Extract features from the audio files
# 
# Labels        : Categories
# FeatureValues : Values exrtacted from the audio files
class Feature(models.Model):
    instances = models.ManyToManyField(
        Instance, 
        null=True, 
        related_name='features')
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class FeatureValue(models.Model):
    feature = models.ForeignKey(Feature, related_name='values')
    instance = models.ForeignKey(Instance, related_name='values')
    value = models.FloatField()
    def __unicode__(self):
        return unicode(self.value)