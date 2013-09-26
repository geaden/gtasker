# -*- coding: utf-8 -*-
from django.test import TestCase

from ..models import TaskerUser
from ..serializers import TaskerUserSerializer

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskerUserSerializersTestCase(TestCase):
    def setUp(self):
        self.user = TaskerUser.objects.create_user(
            email='foo@bar.bz',
            last_name='foo',
            first_name='bar',
            password='buz'
        )

    def test_tasker_user_serializer(self):
        serializer = TaskerUserSerializer(self.user)
        self.assertEquals(
            serializer.data['full_name'], 'bar foo')

