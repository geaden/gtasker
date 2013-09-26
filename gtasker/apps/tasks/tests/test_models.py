# -*- coding: utf-8 -*-
from django.test import TestCase
from ..models import Task
from ...profiles.models import TaskerUser
from ...projects.models import Project


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='bz'
        )
        self.project = Project.objects.create(
            name='foo',
            notes='bar',
            owner=self.user
        )
        self.task = Task.objects.create(
            name='foo',
            project=self.project,
            owner=self.user,
            assignee=self.user
        )

    def test_task_create(self):
        self.assertEquals(1, Task.objects.count())