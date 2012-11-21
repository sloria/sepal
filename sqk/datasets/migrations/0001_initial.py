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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('source', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('datasets', ['Dataset'])

        # Adding model 'Instance'
        db.create_table('datasets_instance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasets.Dataset'])),
        ))
        db.send_create_signal('datasets', ['Instance'])

        # Adding model 'Feature'
        db.create_table('datasets_feature', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datasets.Instance'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('datasets', ['Feature'])


    def backwards(self, orm):
        # Deleting model 'Dataset'
        db.delete_table('datasets_dataset')

        # Deleting model 'Instance'
        db.delete_table('datasets_instance')

        # Deleting model 'Feature'
        db.delete_table('datasets_feature')


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        'datasets.instance': {
            'Meta': {'object_name': 'Instance'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['datasets']