# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field datasets on 'Feature'
        db.delete_table('datasets_feature_datasets')


    def backwards(self, orm):
        # Adding M2M table for field datasets on 'Feature'
        db.create_table('datasets_feature_datasets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['datasets.feature'], null=False)),
            ('dataset', models.ForeignKey(orm['datasets.dataset'], null=False))
        ))
        db.create_unique('datasets_feature_datasets', ['feature_id', 'dataset_id'])


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 6, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasets'", 'null': 'True', 'to': "orm['datasets.LabelName']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'datasets'", 'to': "orm['datasets.Species']"})
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
            'Meta': {'object_name': 'Instance'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_value': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'null': 'True', 'to': "orm['datasets.LabelValue']"}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Species']"})
        },
        'datasets.labelname': {
            'Meta': {'object_name': 'LabelName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'datasets.labelvalue': {
            'Meta': {'object_name': 'LabelValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'label_values'", 'null': 'True', 'to': "orm['datasets.LabelName']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'datasets.species': {
            'Meta': {'object_name': 'Species'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['datasets']