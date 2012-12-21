# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Story'
        db.create_table('artillery_story', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tagline', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('summary', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('canon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artillery.Canon'])),
            ('classification', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('artillery', ['Story'])

        # Adding M2M table for field editors on 'Story'
        db.create_table('artillery_story_editors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('story', models.ForeignKey(orm['artillery.story'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('artillery_story_editors', ['story_id', 'user_id'])

        # Adding model 'Chapter'
        db.create_table('artillery_chapter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artillery.Story'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('artillery', ['Chapter'])

        # Adding unique constraint on 'Chapter', fields ['story', 'order']
        db.create_unique('artillery_chapter', ['story_id', 'order'])

        # Deleting field 'Canon.author'
        db.delete_column('artillery_canon', 'author_id')

        # Adding field 'Canon.owner'
        db.add_column('artillery_canon', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']),
                      keep_default=False)

        # Adding M2M table for field mods on 'Canon'
        db.create_table('artillery_canon_mods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('canon', models.ForeignKey(orm['artillery.canon'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('artillery_canon_mods', ['canon_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Chapter', fields ['story', 'order']
        db.delete_unique('artillery_chapter', ['story_id', 'order'])

        # Deleting model 'Story'
        db.delete_table('artillery_story')

        # Removing M2M table for field editors on 'Story'
        db.delete_table('artillery_story_editors')

        # Deleting model 'Chapter'
        db.delete_table('artillery_chapter')

        # Adding field 'Canon.author'
        db.add_column('artillery_canon', 'author',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Canon.owner'
        db.delete_column('artillery_canon', 'owner_id')

        # Removing M2M table for field mods on 'Canon'
        db.delete_table('artillery_canon_mods')


    models = {
        'artillery.canon': {
            'Meta': {'object_name': 'Canon'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'genre+'", 'symmetrical': 'False', 'to': "orm['artillery.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_nsfw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mods': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'u+'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'primary_genre': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artillery.Genre']"})
        },
        'artillery.chapter': {
            'Meta': {'unique_together': "(('story', 'order'),)", 'object_name': 'Chapter'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artillery.Story']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'artillery.genre': {
            'Meta': {'object_name': 'Genre'},
            'created_on': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'artillery.profile': {
            'Meta': {'object_name': 'Profile'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'artillery.story': {
            'Meta': {'object_name': 'Story'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'canon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artillery.Canon']"}),
            'classification': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'editor+'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['artillery']