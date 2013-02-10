# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Species'
        db.delete_table('datasets_species')

        # Deleting field 'Instance.species'
        db.delete_column('datasets_instance', 'species_id')


        # Renaming column for 'Dataset.species' to match new field type.
        db.rename_column('datasets_dataset', 'species_id', 'species')
        # Changing field 'Dataset.species'
        db.alter_column('datasets_dataset', 'species', self.gf('django.db.models.fields.CharField')(max_length=75, null=True))
        # Removing index on 'Dataset', fields ['species']
        db.delete_index('datasets_dataset', ['species_id'])


    def backwards(self, orm):
        # Adding index on 'Dataset', fields ['species']
        db.create_index('datasets_dataset', ['species_id'])

        # Adding model 'Species'
        db.create_table('datasets_species', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('datasets', ['Species'])

        # Adding field 'Instance.species'
        db.add_column('datasets_instance', 'species',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=2, related_name='instances', to=orm['datasets.Species']),
                      keep_default=False)


        # Renaming column for 'Dataset.species' to match new field type.
        db.rename_column('datasets_dataset', 'species', 'species_id')
        # Changing field 'Dataset.species'
        db.alter_column('datasets_dataset', 'species_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['datasets.Species']))

    models = {
        'datasets.dataset': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 16, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasets.featurevalue': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'FeatureValue'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Instance']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.instance': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Instance'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 16, 0, 0)'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_values': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'instances'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['datasets.LabelValue']"})
        },
        'datasets.labelname': {
            'Meta': {'object_name': 'LabelName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'no label'", 'max_length': '100', 'blank': 'True'})
        },
        'datasets.labelvalue': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'LabelValue'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'label_values'", 'null': 'True', 'to': "orm['datasets.LabelName']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "'none'", 'max_length': '100'})
        }
    }

    complete_apps = ['datasets']