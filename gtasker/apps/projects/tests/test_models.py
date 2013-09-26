# -*- coding: utf-8 -*-
from django.test import TestCase

from ...profiles.models import TaskerUser
from ..models import Project


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectsModelsTestCase(TestCase):
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

    def test_project_create(self):
        self.assertEquals(Project.objects.count(), 1)
        self.assertEquals(self.project.color, 1)
        self.assertEquals(self.project.notes, 'bar')
        self.assertEquals(self.project.owner, self.user)

    def test_project_followers(self):
        self.assertFalse(self.project.followers.exists())
        follower = TaskerUser.objects.create_user(
            email='boo@bar.bz',
            last_name='boo',
            first_name='far',
            password='br'
        )
        self.project.followers.add(follower)
        self.project.save()
        self.assertEquals(self.project.followers.count(), 1)



