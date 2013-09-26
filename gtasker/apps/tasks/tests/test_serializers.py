# -*- coding: utf-8 -*-

from django.test import TestCase

from ..serializers import TaskProjectSerializer

from ...projects.models import Project
from ...profiles.models import TaskerUser
from ..models import Task

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TasksSerializersTestCase(TestCase):
    def setUp(self):
        self.user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='buz'
        )
        self.project = Project.objects.create(
            name='foo',
            notes='bar',
            owner=self.user
        )
        self.task = Task.objects.create(
            name='boo',
            description='bur',
            project=self.project,
            owner=self.user,
            assignee=self.user
        )

    def test_task_project_serializer(self):
        serializer = TaskProjectSerializer(self.task)
        self.assertEquals(
            serializer.data['name'], 'boo')
        self.assertEquals(
            serializer.data['description'], 'bur')
        self.assertEquals(
            serializer.data['assignee']['full_name'], 'bar foo')







