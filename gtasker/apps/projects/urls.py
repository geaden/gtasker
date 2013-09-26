# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required

from .views import ProjectMainView, ProjectCreateView, ProjectDetailView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns(
    '',
    url(r'^$', login_required(
        ProjectMainView.as_view()), name='main'),
    url(r'^create$', login_required(
        ProjectCreateView.as_view()), name='create'),
    url(r'^(?P<pk>\d+)$', login_required(
        ProjectDetailView.as_view()), name='detail'),
)
