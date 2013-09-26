# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import TaskerUser

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskerUserSerializer(serializers.ModelSerializer):
    pk = serializers.RelatedField()
    full_name = serializers.SerializerMethodField('get_full_name')

    class Meta:
        model = TaskerUser
        fields = (
            'pk',
            'full_name',
            'picture',
            'email'
        )

    def get_full_name(self, obj):
        return u'{0} {1}'.format(obj.first_name, obj.last_name)