# -*- coding: utf-8 -*-
from django.test import TestCase

from ..widgets import DatepickerWidget

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectWidgetsTestCase(TestCase):
    def test_datepicker_widget(self):
        w = DatepickerWidget()
        self.assertEquals('<script type="text/javascript"'
                          ' src="/static/js/bootstrap-datepicker.js"></script>',
                          str(w.media.js))