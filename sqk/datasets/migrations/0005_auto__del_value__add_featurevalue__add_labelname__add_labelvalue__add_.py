# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Value'
        db.delete_table('datasets_value')

        # Adding model 'FeatureValue'
        db.create_table('datasets_featurevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Feature'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Instance'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('datasets', ['FeatureValue'])

        # Adding model 'LabelName'
        db.create_table('datasets_labelname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('datasets', ['LabelName'])

        # Adding model 'LabelValue'
        db.create_table('datasets_labelvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='label_values', null=True, to=orm['datasets.LabelName'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('datasets', ['LabelValue'])

        # Adding field 'Dataset.label_name'
        db.add_column('datasets_dataset', 'label_name',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='datasets', null=True, to=orm['datasets.LabelName']),
                      keep_default=False)

        # Deleting field 'Feature.is_label_name'
        db.delete_column('datasets_feature', 'is_label_name')


    def backwards(self, orm):
        # Adding model 'Value'
        db.create_table('datasets_value', (
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Instance'])),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Feature'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('datasets', ['Value'])

        # Deleting model 'FeatureValue'
        db.delete_table('datasets_featurevalue')

        # Deleting model 'LabelName'
        db.delete_table('datasets_labelname')

        # Deleting model 'LabelValue'
        db.delete_table('datasets_labelvalue')

        # Deleting field 'Dataset.label_name'
        db.delete_column('datasets_dataset', 'label_name_id')

        # Adding field 'Feature.is_label_name'
        db.add_column('datasets_feature', 'is_label_name',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 1, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasets'", 'null': 'True', 'to': "orm['datasets.LabelName']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'datasets'", 'to': "orm['datasets.Species']"})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'datasets': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'features'", 'symmetrical': 'False', 'to': "orm['datasets.Dataset']"}),
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