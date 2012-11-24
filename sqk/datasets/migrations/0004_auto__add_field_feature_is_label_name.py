# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Feature.is_label_name'
        db.add_column('datasets_feature', 'is_label_name',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Feature.is_label_name'
        db.delete_column('datasets_feature', 'is_label_name')


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 23, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'source': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'datasets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'features'", 'symmetrical': 'False', 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'is_label_name': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'datasets.instance': {
            'Meta': {'object_name': 'Instance'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'instances'", 'to': "orm['datasets.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'unnamed'", 'max_length': '100'})
        },
        'datasets.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "'unlabeled'", 'max_length': '100'})
        },
        'datasets.value': {
            'Meta': {'object_name': 'Value'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Instance']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['datasets']