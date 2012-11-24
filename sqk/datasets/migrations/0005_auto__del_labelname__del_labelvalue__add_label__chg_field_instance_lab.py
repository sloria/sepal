# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'LabelName'
        db.delete_table('datasets_labelname')

        # Deleting model 'LabelValue'
        db.delete_table('datasets_labelvalue')

        # Adding model 'Label'
        db.create_table('datasets_label', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='unlabeled', max_length=100)),
        ))
        db.send_create_signal('datasets', ['Label'])


        # Changing field 'Instance.label'
        db.alter_column('datasets_instance', 'label_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasets.Label']))

    def backwards(self, orm):
        # Adding model 'LabelName'
        db.create_table('datasets_labelname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('datasets', ['LabelName'])

        # Adding model 'LabelValue'
        db.create_table('datasets_labelvalue', (
            ('label_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.LabelName'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='unlabeled', max_length=100)),
        ))
        db.send_create_signal('datasets', ['LabelValue'])

        # Deleting model 'Label'
        db.delete_table('datasets_label')


        # Changing field 'Instance.label'
        db.alter_column('datasets_instance', 'label_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasets.LabelValue']))

    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 24, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'feature_row': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_col': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'source': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'datasets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'features'", 'symmetrical': 'False', 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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