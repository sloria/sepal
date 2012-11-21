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

class Instance(models.Model):
    dataset = models.ForeignKey(Dataset)
    name = models.CharField(max_length=100, 
        default='unnamed')
    def __unicode__(self):
        return self.name

class Feature(models.Model):
    instance = models.ForeignKey(Instance)
    name = models.CharField(max_length=100)
    value = models.FloatField()
    def __unicode__(self):
        return self.name + ': ' + unicode(self.value)

