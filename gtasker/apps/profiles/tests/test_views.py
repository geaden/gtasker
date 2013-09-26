# -*- coding: utf-8 -*-
import json
from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from ..models import TaskerUser
from ..forms import TrackerAuthForm

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProfilesViewsTestCase(TestCase):
    def setUp(self):
        self.user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='buz'
        )
        self.login_url = reverse('profiles:login')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEquals(200, response.status_code,
                          msg='Status code should be 200')
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertTrue(isinstance(response.context['form'],
                                   TrackerAuthForm))
        response = self.client.post(self.login_url,
            {'username': 'foo@bar.bz', 'password': 'buz'})
        self.assertRedirects(response, reverse('projects:main'))

    def test_profiles_autocomplete(self):
        self.client.login(username='foo@bar.bz',
                          password='buz')
        url = reverse('profiles:autocomplete') + '?q=foo'
        response = self.client.get(url)
        self.assertEquals(200, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
