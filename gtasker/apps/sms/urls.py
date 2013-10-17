# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import SmsReplyView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns('',
                       url(r'^reply$', SmsReplyView.as_view(), name='reply'),)