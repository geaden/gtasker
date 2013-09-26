# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms import TextInput, PasswordInput
from django.utils.translation import \
    ugettext_lazy as _

from .models import TaskerUser

from ..core.helpers import battrs

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TrackerAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control',
                                                       'placeholder': _('Email')}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control',
                                                       'placeholder': _('Password')}))


class TaskerPasswordResetForm(forms.Form):
    password1 = forms.CharField(required=True, widget=PasswordInput(
        attrs=battrs(_('New password'))))
    password2 = forms.CharField(required=True, widget=PasswordInput(
        attrs=battrs(_('Password again'))))

    def clean(self):
        cleaned_data = super(TaskerPasswordResetForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2:
            if not password1 == password2:
                raise forms.ValidationError(_('Passwords do not match. Please check.'))
        return super(TaskerPasswordResetForm, self).clean()
