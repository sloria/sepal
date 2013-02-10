# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Instance.created_at'
        db.add_column('datasets_instance', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 14, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Instance.created_at'
        db.delete_column('datasets_instance', 'created_at')


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 14, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'datasets'", 'null': 'True', 'to': "orm['datasets.Species']"})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasets.featurevalue': {
            'Meta': {'object_name': 'FeatureValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Instance']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.instance': {
            'Meta': {'ordering': "['created_at']", 'object_name': 'Instance'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 14, 0, 0)'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_values': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'instances'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['datasets.LabelValue']"}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Species']"})
        },
        'datasets.labelname': {
            'Meta': {'object_name': 'LabelName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'no label'", 'max_length': '100', 'blank': 'True'})
        },
        'datasets.labelvalue': {
            'Meta': {'object_name': 'LabelValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'label_values'", 'null': 'True', 'to': "orm['datasets.LabelName']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '100'})
        },
        'datasets.species': {
            'Meta': {'object_name': 'Species'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['datasets']