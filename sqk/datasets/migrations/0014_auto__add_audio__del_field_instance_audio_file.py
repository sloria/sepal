# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Audio'
        db.create_table('datasets_audio', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audio_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
            ('instance', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['datasets.Instance'], unique=True)),
        ))
        db.send_create_signal('datasets', ['Audio'])

        # Deleting field 'Instance.audio_file'
        db.delete_column('datasets_instance', 'audio_file')


    def backwards(self, orm):
        # Deleting model 'Audio'
        db.delete_table('datasets_audio')

        # Adding field 'Instance.audio_file'
        db.add_column('datasets_instance', 'audio_file',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)


    models = {
        'datasets.audio': {
            'Meta': {'object_name': 'Audio'},
            'audio_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['datasets.Instance']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'datasets.dataset': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 23, 0, 0)'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 23, 0, 0)'}),
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