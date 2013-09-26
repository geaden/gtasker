# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import Project

from ..tasks.serializers import TaskProjectSerializer


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectSerializer(serializers.ModelSerializer):
    pk = serializers.RelatedField()
    tasks = TaskProjectSerializer(many=True)
    color = serializers.SerializerMethodField('get_color')

    class Meta:
        model = Project
        fields = (
            'pk',
            'name',
            'notes',
            'color',
            'start_date',
            'finish_date',
            'tasks',
        )

    def get_color(self, obj):
        return obj.get_color_display()