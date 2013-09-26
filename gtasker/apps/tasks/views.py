# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import CreateView
from rest_framework.renderers import JSONRenderer

from .models import Task
from .forms import TaskForm
from .serializers import TaskProjectSerializer

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    serializer_class = TaskProjectSerializer

    def render_to_response(self, context, **response_kwargs):
        print(context)
        if 'ajax' in self.request.GET:
            return HttpResponse(json.dumps(context),
                                content_type='application/json',
                                **response_kwargs)
        return super(TaskCreateView, self).render_to_response(
            context, **response_kwargs
        )

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        if obj.assignee is None:
            obj.assignee = self.request.user
        obj.save()
        if 'ajax' in self.request.GET:
            context = JSONRenderer().render(
                self.serializer_class(obj).data
            )
            return HttpResponse(context,
                                content_type='applicataion/json')
        return super(TaskCreateView, self).form_valid(form)

    def form_invalid(self, form):
        if 'ajax' in self.request.GET:
            return HttpResponseBadRequest(
                json.dumps(
                    dict(form.errors.items()),
                    sort_keys=True,
                    indent=2
                ),
                content_type='application/json; charset=UTF-8'
            )
        return super(TaskCreateView, self).form_invalid(form)
