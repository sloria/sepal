# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Dataset.species'
        db.alter_column('datasets_dataset', 'species_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['datasets.Species']))

    def backwards(self, orm):

        # Changing field 'Dataset.species'
        db.alter_column('datasets_dataset', 'species_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasets.Species']))

    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 29, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'species'", 'null': 'True', 'to': "orm['datasets.Species']"})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'datasets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'features'", 'symmetrical': 'False', 'to': "orm['datasets.Dataset']"}),
            'feature_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasets.FeatureSet']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasets.featureset': {
            'Meta': {'object_name': 'FeatureSet'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasets.instance': {
            'Meta': {'object_name': 'Instance'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Species']"})
        },
        'datasets.species': {
            'Meta': {'object_name': 'Species'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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