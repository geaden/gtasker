# -*- coding: utf-8 -*-
from itertools import chain

from django import forms
from django.utils.translation import \
    ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


from ..core.helpers import COLOR_CHOICES


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class DatepickerWidget(forms.TextInput):
    """
    Custom bootstrap datepicker
    """
    class Media:
        css = {
            'all': ('css/jquery-ui-1.10.3.custom.min.css',)
        }
        js = ('js/jquery-ui-1.10.3.custom.min.js', 'js/datepicker.js',)


class ColorpickerWidget(forms.Select):
    """
    Custom colorpicker
    """
    input_type = 'color'

    class Media:
        css = {
            'all': ('css/colorpicker.css',)
        }
        js = ('js/colorpicker.js',)

    def render_color(self, color, current=False):
        if not current:
            current = ''
        else:
            current = ' current'
        return format_html('<div class="color{0}" '
                           'style="background-color: {1};"></div>',
                           current, color)

    def render(self, name, value, attrs=None, choices=()):
        wrapper = [u'<div class="dropdown">', '</div>']
        trigger = [u'<a data-toggle="dropdown" href="#">','</a>']
        current_color = self.render_color(COLOR_CHOICES[value - 1][1], current=True)
        trigger.insert(1, current_color)
        wrapper.insert(1, '\n'.join(trigger))
        options = self.render_options(choices, [value])
        if options:
            wrapper.insert(2, options)
        wrapper.insert(0, format_html('<input type="hidden" value="{0}" name="color" id="id_color" />',
                                      value))
        return mark_safe('\n'.join(wrapper))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value in selected_choices:
            selected_html = mark_safe(' active')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        color = self.render_color(option_label)
        link = format_html('<a href="#" id="color_{0}" '
                           'data-value="{0}" onclick="selectColor(this)">{1}</a>',
                           option_value, color)
        return format_html('<li class="colors{0}">{1}</li>',
                           selected_html,
                           link)

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        output.append(format_html('<ul class="dropdown-menu colors" role="menu" aria-labelledby="colorMenu">'))
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        output.append('</ul>')
        return mark_safe('\n'.join(output))


class AutocompleteFollowersWidget(forms.MultipleHiddenInput):
    class Media:
        css = {
            'all': ('css/autocomplete.css',)
        }
        js = ('js/autocomplete.js',)

    def render(self, name, value, attrs=None, choices=()):
        wrapper = [format_html('<input type="text" '
                   'name="followers_autocomplete" id="id_followers_autocomplete" '
                   'class="form-control" placeholder="{0}" />', unicode(_(u'Followers')))]
        wrapper.insert(0, super(AutocompleteFollowersWidget, self).render(name, value, attrs, choices))
        return mark_safe('\n'.join(wrapper))

