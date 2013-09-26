# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskerUser'
        db.create_table(u'profiles_taskeruser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255, db_index=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'profiles', ['TaskerUser'])

        # Adding M2M table for field groups on 'TaskerUser'
        db.create_table(u'profiles_taskeruser_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('taskeruser', models.ForeignKey(orm[u'profiles.taskeruser'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(u'profiles_taskeruser_groups', ['taskeruser_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'TaskerUser'
        db.create_table(u'profiles_taskeruser_user_permissions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('taskeruser', models.ForeignKey(orm[u'profiles.taskeruser'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(u'profiles_taskeruser_user_permissions', ['taskeruser_id', 'permission_id'])

        # Adding model 'FlowModel'
        db.create_table(u'profiles_flowmodel', (
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.TaskerUser'], primary_key=True)),
            ('flow', self.gf('oauth2client.django_orm.FlowField')(null=True)),
        ))
        db.send_create_signal(u'profiles', ['FlowModel'])

        # Adding model 'CredentialsModel'
        db.create_table(u'profiles_credentialsmodel', (
            ('id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['profiles.TaskerUser'], primary_key=True)),
            ('credential', self.gf('oauth2client.django_orm.CredentialsField')(null=True)),
        ))
        db.send_create_signal(u'profiles', ['CredentialsModel'])


    def backwards(self, orm):
        # Deleting model 'TaskerUser'
        db.delete_table(u'profiles_taskeruser')

        # Removing M2M table for field groups on 'TaskerUser'
        db.delete_table('profiles_taskeruser_groups')

        # Removing M2M table for field user_permissions on 'TaskerUser'
        db.delete_table('profiles_taskeruser_user_permissions')

        # Deleting model 'FlowModel'
        db.delete_table(u'profiles_flowmodel')

        # Deleting model 'CredentialsModel'
        db.delete_table(u'profiles_credentialsmodel')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'profiles.credentialsmodel': {
            'Meta': {'object_name': 'CredentialsModel'},
            'credential': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.TaskerUser']", 'primary_key': 'True'})
        },
        u'profiles.flowmodel': {
            'Meta': {'object_name': 'FlowModel'},
            'flow': ('oauth2client.django_orm.FlowField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['profiles.TaskerUser']", 'primary_key': 'True'})
        },
        u'profiles.taskeruser': {
            'Meta': {'object_name': 'TaskerUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['profiles']