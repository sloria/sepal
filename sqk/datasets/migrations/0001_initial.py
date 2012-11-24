# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dataset'
        db.create_table('datasets_dataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('source', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('label_col', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('feature_row', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 11, 24, 0, 0))),
        ))
        db.send_create_signal('datasets', ['Dataset'])

        # Adding model 'LabelName'
        db.create_table('datasets_labelname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('datasets', ['LabelName'])

        # Adding model 'LabelValue'
        db.create_table('datasets_labelvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.LabelName'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='unlabeled', max_length=100)),
        ))
        db.send_create_signal('datasets', ['LabelValue'])

        # Adding model 'Instance'
        db.create_table('datasets_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['datasets.Dataset'])),
            ('label', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='instances', to=orm['datasets.LabelValue'])),
            ('name', self.gf('django.db.models.fields.CharField')(default='unnamed', max_length=100)),
        ))
        db.send_create_signal('datasets', ['Instance'])

        # Adding model 'Feature'
        db.create_table('datasets_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('datasets', ['Feature'])

        # Adding M2M table for field datasets on 'Feature'
        db.create_table('datasets_feature_datasets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['datasets.feature'], null=False)),
            ('dataset', models.ForeignKey(orm['datasets.dataset'], null=False))
        ))
        db.create_unique('datasets_feature_datasets', ['feature_id', 'dataset_id'])

        # Adding M2M table for field instances on 'Feature'
        db.create_table('datasets_feature_instances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['datasets.feature'], null=False)),
            ('instance', models.ForeignKey(orm['datasets.instance'], null=False))
        ))
        db.create_unique('datasets_feature_instances', ['feature_id', 'instance_id'])

        # Adding model 'Value'
        db.create_table('datasets_value', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Feature'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Instance'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('datasets', ['Value'])


    def backwards(self, orm):
        # Deleting model 'Dataset'
        db.delete_table('datasets_dataset')

        # Deleting model 'LabelName'
        db.delete_table('datasets_labelname')

        # Deleting model 'LabelValue'
        db.delete_table('datasets_labelvalue')

        # Deleting model 'Instance'
        db.delete_table('datasets_instance')

        # Deleting model 'Feature'
        db.delete_table('datasets_feature')

        # Removing M2M table for field datasets on 'Feature'
        db.delete_table('datasets_feature_datasets')

        # Removing M2M table for field instances on 'Feature'
        db.delete_table('datasets_feature_instances')

        # Deleting model 'Value'
        db.delete_table('datasets_value')


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
            'label': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'instances'", 'to': "orm['datasets.LabelValue']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'unnamed'", 'max_length': '100'})
        },
        'datasets.labelname': {
            'Meta': {'object_name': 'LabelName'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        'datasets.labelvalue': {
            'Meta': {'object_name': 'LabelValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label_name': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.LabelName']"}),
            'value': ('django.db.models.fields.CharField', [], {'default': "'unlabeled'", 'max_length': '100'})
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