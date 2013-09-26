# -*- coding: utf-8 -*-
import datetime
from django.test import TestCase

from ..models import TaskerUser


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProfilesModelsTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_super_user(self):
        super_user = TaskerUser.objects.create_superuser(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='buz'
        )
        self.assertEquals(TaskerUser.objects.all().count(),
                          1, msg='Number of users should be 1')
        self.assertTrue(super_user.is_superuser,
                        msg='User should be super user')

    def test_create_regular_user(self):
        user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='baz'
        )
        self.assertEquals(TaskerUser.objects.all().count(),
                          1, msg='Number of users should be 1')
        self.assertFalse(user.is_superuser,
                         msg='User shouldn\'t be super user')

    def test_extend_user_model(self):
        user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            first_name='foo',
            last_name='bar',
            password='baz'
        )
        user.birthday = datetime.datetime.strptime(
            '1987-05-11', '%Y-%m-%d')
        user.gender = u'male'
        user.picture = 'http://www.google.com/robot'
        user.save()
        user = TaskerUser.objects.get(pk=1)
        self.assertEquals(user.picture, 'http://www.google.com/robot')


