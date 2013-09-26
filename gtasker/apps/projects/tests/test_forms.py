# -*- coding: utf-8 -*-
from django.test import TestCase

from ..forms import ProjectForm

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectFormTestCase(TestCase):
    def test_project_form(self):
        data = {'name': u'foo',
                'start_date': u'04.09.2013',
                'finish_date': u'04.10.2013',
                'color': 1}
        form = ProjectForm(data=data)
        self.assertTrue(form.is_valid())



