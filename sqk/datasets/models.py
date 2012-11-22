from django.db import models
from django.utils import timezone

class Dataset(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    source = models.FileField(upload_to='data_sources')
    created_at = models.DateTimeField('created at', default=timezone.now())
    def __unicode__(self):
        return self.name

class Label(models.Model):
    label = models.CharField(max_length=100, default='unlabeled')
    def __unicode__(self):
        return self.label

class Instance(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='instances')
    label = models.ForeignKey(Label, default=0, related_name='instances')
    name = models.CharField(max_length=100, 
        default='unnamed')
    def __unicode__(self):
        return self.name

class Feature(models.Model):
    instances = models.ManyToManyField(
        Instance, 
        null=True, 
        related_name='features')
    name = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.name

class Value(models.Model):
    feature = models.ForeignKey(Feature, related_name='values')
    instance = models.ForeignKey(Instance, related_name='values')
    value = models.FloatField()
    def __unicode__(self):
        return unicode(self.value)
