from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

class Dataset(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    source = models.FileField(upload_to='data_sources')
    label_col = models.IntegerField(default=-1)
    feature_row = models.IntegerField(default=0)
    created_at = models.DateTimeField('created at', default=timezone.now())
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('datasets:detail', kwargs={'pk': self.pk})
    def sorted_features(self):
        return self.features.order_by('pk')
    def sorted_instances(self):
        return self.instances.order_by('pk')
    def values_as_list(self):
        return [self.sorted_instances()[i].values_as_list() for i in range(
            len(self.sorted_instances()))]

class Label(models.Model):
    label = models.CharField(max_length=100, default='unlabeled')
    def __unicode__(self):
        return self.label

class Instance(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='instances')
    label = models.ForeignKey(Label, default=0, related_name='instances')
    def __unicode__(self):
        return u'pk %s from dataset %s' %(self.pk, self.dataset.pk)
    def sorted_values(self):
        return self.values.order_by('feature')
    def values_as_list(self):
        return [value.value for value in self.sorted_values()]
    def sorted_features(self):
        return self.features.order_by('pk')

class Feature(models.Model):
    #TODO: support for meta values
    datasets = models.ManyToManyField(Dataset,
        related_name='features')
    instances = models.ManyToManyField(
        Instance, 
        null=True, 
        related_name='features')
    name = models.CharField(max_length=100)
    is_label_name = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Value(models.Model):
    feature = models.ForeignKey(Feature, related_name='values')
    instance = models.ForeignKey(Instance, related_name='values')
    value = models.FloatField()
    def __unicode__(self):
        return unicode(self.value)
