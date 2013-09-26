# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import Task

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskViewTestCase(TestCase):
    def setUp(self):
        self.create_url = reverse(
            'tasks:create')

    def test_create_view(self):
        response = self.client.post(self.create_url)
        self.assertRedirects(response, reverse('profiles:login') +
            '?next=/tasks/create/'
        )
