# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required

from .views import TaskerAuthView, ProfilesAutocompleteView, \
    GoogleLoginView, GoogleAuthReturnView, TaskerUserPasswordReset, GoogleActivityView

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


urlpatterns = patterns('',
                       url(r'^logout/?$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^login/?$', TaskerAuthView.as_view(),
                           name='login'),
                       url(r'^autocomplete/?$',
                           login_required(ProfilesAutocompleteView.as_view()),
                           name='autocomplete'),
                       url(r'^login/google/?$', GoogleLoginView.as_view(), name='google'),
                       url(r'^activity/?$', GoogleActivityView.as_view(), name='activity'),
                       url(r'^oauth2callback', GoogleAuthReturnView.as_view(), name='oauth'),
                       url(r'^reset', login_required(
                           TaskerUserPasswordReset.as_view()), name='reset'),
                       )