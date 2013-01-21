# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Genre'
        db.delete_table('artillery_genre')

        # Deleting model 'Canon'
        db.delete_table('artillery_canon')

        # Removing M2M table for field genres on 'Canon'
        db.delete_table('artillery_canon_genres')

        # Removing M2M table for field mods on 'Canon'
        db.delete_table('artillery_canon_mods')

        # Adding model 'StoryArt'
        db.create_table('artillery_storyart', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artillery.Story'], blank=True)),
            ('art', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('created_on', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('modified_on', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('artillery', ['StoryArt'])

        # Deleting field 'Story.canon'
        db.delete_column('artillery_story', 'canon_id')

        # Adding field 'Story.created_on'
        db.add_column('artillery_story', 'created_on',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.datetime(2013, 1, 20, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Story.modified_on'
        db.add_column('artillery_story', 'modified_on',
                      self.gf('django.db.models.fields.DateField')(auto_now=True, default=datetime.datetime(2013, 1, 20, 0, 0), blank=True),
                      keep_default=False)

        # Adding M2M table for field related_stories on 'Story'
        db.create_table('artillery_story_related_stories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_story', models.ForeignKey(orm['artillery.story'], null=False)),
            ('to_story', models.ForeignKey(orm['artillery.story'], null=False))
        ))
        db.create_unique('artillery_story_related_stories', ['from_story_id', 'to_story_id'])

        # Adding field 'Chapter.created_on'
        db.add_column('artillery_chapter', 'created_on',
                      self.gf('django.db.models.fields.DateField')(auto_now_add=True, default=datetime.datetime(2013, 1, 20, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Chapter.modified_on'
        db.add_column('artillery_chapter', 'modified_on',
                      self.gf('django.db.models.fields.DateField')(auto_now=True, default=datetime.datetime(2013, 1, 20, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Genre'
        db.create_table('artillery_genre', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('created_on', self.gf('django.db.models.fields.DateField')()),
            ('modified_on', self.gf('django.db.models.fields.DateField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('artillery', ['Genre'])

        # Adding model 'Canon'
        db.create_table('artillery_canon', (
            ('is_nsfw', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('primary_genre', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['artillery.Genre'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('artillery', ['Canon'])

        # Adding M2M table for field genres on 'Canon'
        db.create_table('artillery_canon_genres', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('canon', models.ForeignKey(orm['artillery.canon'], null=False)),
            ('genre', models.ForeignKey(orm['artillery.genre'], null=False))
        ))
        db.create_unique('artillery_canon_genres', ['canon_id', 'genre_id'])

        # Adding M2M table for field mods on 'Canon'
        db.create_table('artillery_canon_mods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('canon', models.ForeignKey(orm['artillery.canon'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('artillery_canon_mods', ['canon_id', 'user_id'])

        # Deleting model 'StoryArt'
        db.delete_table('artillery_storyart')

        # Adding field 'Story.canon'
        db.add_column('artillery_story', 'canon',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['artillery.Canon']),
                      keep_default=False)

        # Deleting field 'Story.created_on'
        db.delete_column('artillery_story', 'created_on')

        # Deleting field 'Story.modified_on'
        db.delete_column('artillery_story', 'modified_on')

        # Removing M2M table for field related_stories on 'Story'
        db.delete_table('artillery_story_related_stories')

        # Deleting field 'Chapter.created_on'
        db.delete_column('artillery_chapter', 'created_on')

        # Deleting field 'Chapter.modified_on'
        db.delete_column('artillery_chapter', 'modified_on')


    models = {
        'artillery.chapter': {
            'Meta': {'unique_together': "(('story', 'order'),)", 'object_name': 'Chapter'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artillery.Story']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'artillery.profile': {
            'Meta': {'object_name': 'Profile'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'artillery.story': {
            'Meta': {'object_name': 'Story'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'classification': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'created_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'editor+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'related_stories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'story+'", 'null': 'True', 'to': "orm['artillery.Story']"}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tagline': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'artillery.storyart': {
            'Meta': {'object_name': 'StoryArt'},
            'art': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'created_on': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_on': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['artillery.Story']", 'blank': 'True'})
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