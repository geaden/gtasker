# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy, reverse
from django.test import TestCase

from ...profiles.models import TaskerUser
from ..models import Project

from ...core.helpers import create_fixture

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectsViewTestCase(TestCase):
    fixtures = ['fixtures/test.json']

    def setUp(self):
        self.user = TaskerUser.objects.create(
            email='foo@bar.com',
            last_name='foo',
            first_name='bar',
            password='bazzar',
            is_staff=True
        )
        self.url = reverse('projects:main')
        self.login_url = reverse('profiles:login')
        login = self.client.login(email='foo@bar.com',
                                  password='bazzar')
        self.assertTrue(login)

    @create_fixture
    def before(self):
        return self.user

    def test_projects_view(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('profiles:login') + '?next=/')
        response = self.client.post(self.login_url,
                         {'email': 'foo@bar.com', 'password': 'bazzar'})
        self.assertRedirects(response, reverse('projects:main'))
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'projects/project_list.html')

    def test_project_details(self):
        project = Project.objects.create(
            name='foo',
            notes='bar',
            owner=self.user
        )
        url = reverse('projects:detail', kwargs={'pk': project.pk})
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)








