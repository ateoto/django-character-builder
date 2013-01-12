# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Character.level'
        db.add_column('character_builder_character', 'level',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.strength'
        db.add_column('character_builder_character', 'strength',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.constitution'
        db.add_column('character_builder_character', 'constitution',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.dexterity'
        db.add_column('character_builder_character', 'dexterity',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.intelligence'
        db.add_column('character_builder_character', 'intelligence',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.wisdom'
        db.add_column('character_builder_character', 'wisdom',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Character.charisma'
        db.add_column('character_builder_character', 'charisma',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Character.level'
        db.delete_column('character_builder_character', 'level')

        # Deleting field 'Character.strength'
        db.delete_column('character_builder_character', 'strength')

        # Deleting field 'Character.constitution'
        db.delete_column('character_builder_character', 'constitution')

        # Deleting field 'Character.dexterity'
        db.delete_column('character_builder_character', 'dexterity')

        # Deleting field 'Character.intelligence'
        db.delete_column('character_builder_character', 'intelligence')

        # Deleting field 'Character.wisdom'
        db.delete_column('character_builder_character', 'wisdom')

        # Deleting field 'Character.charisma'
        db.delete_column('character_builder_character', 'charisma')


    models = {
        'character_builder.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'character_builder.character': {
            'Meta': {'object_name': 'Character'},
            'charisma': ('django.db.models.fields.IntegerField', [], {}),
            'class_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.ClassType']"}),
            'constitution': ('django.db.models.fields.IntegerField', [], {}),
            'dexterity': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intelligence': ('django.db.models.fields.IntegerField', [], {}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'race': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['character_builder.Race']"}),
            'strength': ('django.db.models.fields.IntegerField', [], {}),
            'wisdom': ('django.db.models.fields.IntegerField', [], {})
        },
        'character_builder.classtype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ClassType'},
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
            'Meta': {'ordering': "['name']", 'object_name': 'Race'},
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
            'Meta': {'ordering': "['name']", 'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['character_builder']