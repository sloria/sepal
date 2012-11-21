from django.db import models
from django.utils import timezone
import datetime

class Dataset(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    source = models.FileField(upload_to='data_sources')
    created_at = models.DateTimeField('created at', default=timezone.now())
    def __unicode__(self):
        return self.name
    def instances(self):
        return self.instance_set.all()

class Instance(models.Model):
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=100, 
        default='unnamed')
    def __unicode__(self):
        return self.name
    def features(self):
        return self.feature_set.all()
    def values(self):
        return [feature.value for feature in self.feature_set.all()]

class Feature(models.Model):
    instance = models.ForeignKey(Instance)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    def __unicode__(self):
        return self.name + ': ' + unicode(self.value)
