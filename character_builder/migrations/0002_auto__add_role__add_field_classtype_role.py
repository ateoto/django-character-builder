# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table('character_builder_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('character_builder', ['Role'])

        # Adding field 'ClassType.role'
        db.add_column('character_builder_classtype', 'role',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['character_builder.Role']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table('character_builder_role')

        # Deleting field 'ClassType.role'
        db.delete_column('character_builder_classtype', 'role_id')


    models = {
        'character_builder.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'character_builder.character': {
            'Meta': {'object_name': 'Character'},
            'class_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.ClassType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Race']"})
        },
        'character_builder.classtype': {
            'Meta': {'object_name': 'ClassType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Role']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Source']"})
        },
        'character_builder.item': {
            'Meta': {'object_name': 'Item'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Source']"})
        },
        'character_builder.race': {
            'Meta': {'object_name': 'Race'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Source']"})
        },
        'character_builder.role': {
            'Meta': {'object_name': 'Role'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'character_builder.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['character_builder']