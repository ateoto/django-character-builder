# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('character_builder_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('character_builder', ['Source'])

        # Adding model 'Campaign'
        db.create_table('character_builder_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('character_builder', ['Campaign'])

        # Adding model 'Race'
        db.create_table('character_builder_race', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character_builder.Source'])),
        ))
        db.send_create_signal('character_builder', ['Race'])

        # Adding model 'ClassType'
        db.create_table('character_builder_classtype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character_builder.Source'])),
        ))
        db.send_create_signal('character_builder', ['ClassType'])

        # Adding model 'Character'
        db.create_table('character_builder_character', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('class_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character_builder.ClassType'])),
            ('race', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character_builder.Race'])),
        ))
        db.send_create_signal('character_builder', ['Character'])

        # Adding model 'Item'
        db.create_table('character_builder_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['character_builder.Source'])),
        ))
        db.send_create_signal('character_builder', ['Item'])


    def backwards(self, orm):
        # Deleting model 'Source'
        db.delete_table('character_builder_source')

        # Deleting model 'Campaign'
        db.delete_table('character_builder_campaign')

        # Deleting model 'Race'
        db.delete_table('character_builder_race')

        # Deleting model 'ClassType'
        db.delete_table('character_builder_classtype')

        # Deleting model 'Character'
        db.delete_table('character_builder_character')

        # Deleting model 'Item'
        db.delete_table('character_builder_item')


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
        'character_builder.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['character_builder']