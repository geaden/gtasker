# -*- coding: utf-8 -*-
from django.test import TestCase

from ..forms import TaskerPasswordResetForm

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProfilesFormsTestCase(TestCase):
    def test_reset_form(self):
        form = TaskerPasswordResetForm()
        self.assertFalse(form.is_valid())
        form = TaskerPasswordResetForm({'password1': 'boo',
                                        'password2': 'zoo'})
        self.assertFalse(form.is_valid())
        self.assertEquals(u'Passwords do not match. Please check.',
                      form.errors['__all__'][0])
