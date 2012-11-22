# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Label'
        db.create_table('datasets_label', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
        ))
        db.send_create_signal('datasets', ['Label'])

        # Adding field 'Instance.label'
        db.add_column('datasets_instance', 'label',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='labels', null=True, to=orm['datasets.Label']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Label'
        db.delete_table('datasets_label')

        # Deleting field 'Instance.label'
        db.delete_column('datasets_instance', 'label_id')


    models = {
        'datasets.dataset': {
            'Meta': {'object_name': 'Dataset'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 11, 21, 0, 0)'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'datasets.feature': {
            'Meta': {'object_name': 'Feature'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instances': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'features'", 'null': 'True', 'to': "orm['datasets.Instance']"}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'datasets.instance': {
            'Meta': {'object_name': 'Instance'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['datasets.Dataset']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'labels'", 'null': 'True', 'to': "orm['datasets.Label']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'unnamed'", 'max_length': '100'})
        },
        'datasets.label': {
            'Meta': {'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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