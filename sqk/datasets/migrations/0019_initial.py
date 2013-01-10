# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LabelName'
        db.create_table('datasets_labelname', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='no label', max_length=100, blank=True)),
        ))
        db.send_create_signal('datasets', ['LabelName'])

        # Adding model 'LabelValue'
        db.create_table('datasets_labelvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label_name', self.gf('django.db.models.fields.related.ForeignKey')(related_name='label_values', null=True, to=orm['datasets.LabelName'])),
            ('value', self.gf('django.db.models.fields.CharField')(default='none', max_length=100)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('datasets', ['LabelValue'])

        # Adding model 'Dataset'
        db.create_table('datasets_dataset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('species', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 9, 0, 0))),
        ))
        db.send_create_signal('datasets', ['Dataset'])

        # Adding model 'Audio'
        db.create_table('datasets_audio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audio_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('datasets', ['Audio'])

        # Adding model 'Instance'
        db.create_table('datasets_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['datasets.Dataset'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 1, 9, 0, 0))),
            ('audio', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasets.Audio'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('datasets', ['Instance'])

        # Adding M2M table for field label_values on 'Instance'
        db.create_table('datasets_instance_label_values', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('instance', models.ForeignKey(orm['datasets.instance'], null=False)),
            ('labelvalue', models.ForeignKey(orm['datasets.labelvalue'], null=False))
        ))
        db.create_unique('datasets_instance_label_values', ['instance_id', 'labelvalue_id'])

        # Adding model 'Feature'
        db.create_table('datasets_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('datasets', ['Feature'])

        # Adding M2M table for field instances on 'Feature'
        db.create_table('datasets_feature_instances', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feature', models.ForeignKey(orm['datasets.feature'], null=False)),
            ('instance', models.ForeignKey(orm['datasets.instance'], null=False))
        ))
        db.create_unique('datasets_feature_instances', ['feature_id', 'instance_id'])

        # Adding model 'FeatureValue'
        db.create_table('datasets_featurevalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feature', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Feature'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='values', to=orm['datasets.Instance'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('datasets', ['FeatureValue'])


    def backwards(self, orm):
        # Deleting model 'LabelName'
        db.delete_table('datasets_labelname')

        # Deleting model 'LabelValue'
        db.delete_table('datasets_labelvalue')

        # Deleting model 'Dataset'
        db.delete_table('datasets_dataset')

        # Deleting model 'Audio'
        db.delete_table('datasets_audio')

        # Deleting model 'Instance'
        db.delete_table('datasets_instance')

        # Removing M2M table for field label_values on 'Instance'
        db.delete_table('datasets_instance_label_values')

        # Deleting model 'Feature'
        db.delete_table('datasets_feature')

        # Removing M2M table for field instances on 'Feature'
        db.delete_table('datasets_feature_instances')

        # Deleting model 'FeatureValue'
        db.delete_table('datasets_featurevalue')


    models = {
        'datasets.audio': {
            'Meta': {'object_name': 'Audio'},
            'audio_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'datasets.dataset': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 9, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'})
        },
        'datasets.feature': {
            'Meta': {'ordering': "['name']", 'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'datasets.featurevalue': {
            'Meta': {'ordering': "['feature']", 'object_name': 'FeatureValue'},
            'feature': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Feature']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': "orm['datasets.Instance']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.instance': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Instance'},
            'audio': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasets.Audio']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 1, 9, 0, 0)'}),
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