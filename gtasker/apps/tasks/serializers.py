# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Task

from ..profiles.serializers import TaskerUserSerializer

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskProjectSerializer(serializers.ModelSerializer):
    pk = serializers.RelatedField()
    owner = TaskerUserSerializer()
    assignee = TaskerUserSerializer()

    class Meta:
        model = Task
        fields = (
            'pk',
            'name',
            'description',
            'assignee',
            'owner',
            'created_at',
        )