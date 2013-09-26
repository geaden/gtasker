# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation \
    import ugettext_lazy as _

from .models import Task

from ..core.helpers import battrs

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


taskattrs = battrs(_('Add task'))
taskattrs.update({'autocomplete': 'off'})

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'name',
            'project',
        )
        widgets = {
            'project': forms.HiddenInput(),
            'name': forms.TextInput(attrs=taskattrs)
        }