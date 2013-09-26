# -*- coding: utf-8 -*-
from django.test import TestCase

from ..serializers import ProjectSerializer
from ..models import Project
from ...profiles.models import TaskerUser
from ...tasks.models import Task

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectSerizlizerTestCase(TestCase):
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
            name='foo',
            description='bar',
            owner=self.user,
            assignee=self.user,
            project=self.project
        )

    def test_project_serializer(self):
        serializer = ProjectSerializer(self.project)
        self.assertEquals(
            len(serializer.data['tasks']), 1)
        self.assertEquals(
            serializer.data['tasks'][0]['name'], 'foo')

