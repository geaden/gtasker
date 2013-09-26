# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation \
    import ugettext_lazy as _

from .models import Project
from .widgets import DatepickerWidget, ColorpickerWidget, AutocompleteFollowersWidget

from ..core.helpers import battrs

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


notes = battrs(_('Notes'))
notes.update({'rows': 3})


def date_attrs(name):
    """
    Makes class for date field

    :param name: name of datenfield
    :returns: dictionary of attrubutes
    """
    attrs = battrs(name)
    attrs.update({'class': 'form-control datepicker'})
    return attrs


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'color',
            'name',
            'notes',
            'followers',
            'start_date',
            'finish_date',
        )
        widgets = {
            'color': ColorpickerWidget(attrs=battrs(_('Color'))),
            'name': forms.TextInput(attrs=battrs(_('Name'))),
            'notes': forms.Textarea(attrs=notes),
            'start_date': DatepickerWidget(attrs=date_attrs(_('Start date'))),
            'finish_date': DatepickerWidget(attrs=date_attrs(_('Finish date'))),
            'followers': AutocompleteFollowersWidget(attrs=battrs(_('Followers')))
        }

    def clean(self):
        super(ProjectForm, self).clean()
        start_date = self.cleaned_data.get("start_date")
        finish_date = self.cleaned_data.get("finish_date")

        if start_date and finish_date:
            if start_date > finish_date:
                raise forms.ValidationError(_('Incorrect date input. '
                                              'Finish date is earlier than start date.'))
        if finish_date and not start_date:
            raise forms.ValidationError(_('Provide beginning date.'))
        return super(ProjectForm, self).clean()
