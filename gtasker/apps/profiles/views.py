# -*- coding: utf-8 -*-
import json
import logging
import os
from apiclient.discovery import build
from django.core import serializers
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.views.generic import FormView, ListView, View, TemplateView
from django.conf import settings
from django.contrib.auth import authenticate, login
import httplib2
from oauth2client import xsrfutil
from oauth2client.django_orm import Storage
from oauth2client.client import     flow_from_clientsecrets, OAuth2WebServerFlow

from .forms import TrackerAuthForm, TaskerPasswordResetForm

from .models import TaskerUser, CredentialsModel


__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskerAuthView(FormView):
    form_class = TrackerAuthForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        if 'next' in self.request.GET:
            success_url = self.request.GET['next']
        else:
            success_url = settings.LOGIN_REDIRECT_URL
        return success_url

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
        return super(TaskerAuthView, self).form_valid(form)


class ProfilesAutocompleteView(ListView):
    model = TaskerUser
    paginate_by = 5

    def render_to_response(self, context, **response_kwargs):
        context = serializers.serialize('json', self.get_queryset(),
                                        fields=('last_name', 'first_name', 'email', 'picture'))
        return HttpResponse(context,
                            content_type='application/json',
                            **response_kwargs)

    def get_queryset(self):
        queryset = super(ProfilesAutocompleteView, self).\
            get_queryset()
        if 'q' in self.request.GET:
            q = self.request.GET.get('q')
            if q:
                queryset = self.model.objects.filter(
                    Q(last_name__istartswith=q) |
                    Q(first_name__istartswith=q) |
                    Q(email__istartswith=q)
                )[:self.paginate_by]
            else:
                queryset = []
        return queryset


CLIENT_SECRETS = os.path.join(
    os.path.dirname(__file__), '..', '..', '..', 'client_secrets.json')

FLOW = OAuth2WebServerFlow(
    client_id=settings.GOOGLEAPI_CLIENT_ID,
    client_secret=settings.GOOGLEAPI_CLIENT_SECRET,
    scope='openid email profile',
    redirect_uri=settings.GOOGLEAPI_REDIRECT_URL)


class GoogleActivityView(TemplateView):
    """Test google view"""
    template_name = 'profiles/index.html'
    context = {}

    def get_context_data(self, **kwargs):
        ctx = super(GoogleActivityView, self).\
            get_context_data(**kwargs)
        ctx.update(self.context)
        return ctx

    def get(self, request, *args, **kwargs):
        storage = Storage(CredentialsModel,
                          'id', self.request.user.pk, 'credential')
        credential = storage.get()
        if credential is None or \
                credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY,
                request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            http = httplib2.Http()
            http = credential.authorize(http)
            service = build("plus", "v1", http=http)
            activities = service.activities()
            activitylist = activities.list(collection='public',
                                           userId='me').execute()
            self.context['activitylist'] = activitylist
            logging.info(activitylist)
        return super(GoogleActivityView, self).\
            get(request, **kwargs)


class GoogleLoginView(View):
    """Google Login View"""
    def get(self, request, *args, **kwargs):
        storage = Storage(CredentialsModel,
                          'id', self.request.user.pk, 'credential')
        credential = storage.get()
        if credential is None or \
                credential.invalid:
            FLOW.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY,
                request.user)
            authorize_url = FLOW.step1_get_authorize_url()
            return HttpResponseRedirect(authorize_url)
        else:
            HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        return super(GoogleLoginView, self).\
            get(request, **kwargs)


class TaskerUserPasswordReset(FormView):
    form_class = TaskerPasswordResetForm
    template_name = 'profiles/reset.html'
    success_url = reverse_lazy('projects:main')

    def form_valid(self, form):
        user = self.request.user
        password = form.cleaned_data.get('password1')
        if password:
            user.set_password(password)
            user.save()
        return super(TaskerUserPasswordReset, self).\
            form_valid(form)


class GoogleAuthReturnView(View):
    """Google Auth return view"""
    def get(self, request, **kwargs):
        if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.REQUEST['state'],
                request.user):
            return HttpResponseBadRequest()
        credential = FLOW.step2_exchange(request.REQUEST)
        user_document = self.get_user_info(credential)
        email = user_document['email']
        try:
            user = TaskerUser.objects.get_by_natural_key(email)
        except TaskerUser.DoesNotExist:
            user = None
        if user is not None:
            storage = Storage(CredentialsModel, 'id', user, 'credential')
            storage.put(credential)
            user = authenticate(google_user=user_document)
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        password = TaskerUser.objects.make_random_password()
        user = TaskerUser.objects.create_user(
            email=email,
            last_name=user_document['family_name'],
            first_name=user_document['given_name'],
            password=password)
        user_backend = authenticate(username=email,
                                    password=password)
        if user_backend:
            login(request, user_backend)
        if email == settings.ADMIN_USER:
            user.is_staff = True
            user.is_superuser = True
        user.gender = user_document['gender']
        user.birthday = user_document['birthday']
        user.picture = user_document['picture']
        user.google_id = user_document['id']
        user.save()
        storage = Storage(CredentialsModel, 'id', user, 'credential')
        storage.put(credential)
        return HttpResponseRedirect(reverse_lazy('profiles:reset'))

    def get_user_info(self, credential):
        http = httplib2.Http()
        http = credential.authorize(http)
        service = build("oauth2", "v2", http=http)
        user_document = service.userinfo().get().execute()
        return user_document
