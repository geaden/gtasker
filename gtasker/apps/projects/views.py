# -*- coding: utf-8 -*-
import json
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest, Http404
from django.views.generic import ListView, \
    DetailView, CreateView
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Project
from .forms import ProjectForm
from ..tasks.forms import TaskForm
from .serializers import ProjectSerializer

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    serializer_class = ProjectSerializer

    def render_to_response(self, context, **response_kwargs):
        if 'ajax' in self.request.GET:
            return HttpResponse(json.dumps(context),
                                content_type='application/json',
                                **response_kwargs)
        return super(ProjectCreateView, self).render_to_response(
            context, **response_kwargs
        )

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        if 'ajax' in self.request.GET:
            form.save_m2m()
            content = JSONRenderer().render(
                self.serializer_class(obj).data
            )
            return HttpResponse(content,
                                content_type='application/json')
        return super(ProjectCreateView, self).form_valid(form)

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
        return super(ProjectCreateView, self).form_invalid(form)


class ProjectUpdateView(APIView):
    """
    Update project ajaxy
    """
    model = Project

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def post(self, request, pk, **kwargs):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.DATA,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDetailView(DetailView):
    model = Project
    serializer_class = ProjectSerializer

    def render_to_response(self, context, **response_kwargs):
        if 'ajax' in self.request.GET:
            context = JSONRenderer().render(
                self.serializer_class(self.get_object()).data)
            return HttpResponse(context,
                                content_type='application/json',
                                **response_kwargs)
        return super(ProjectDetailView, self).render_to_response(context, **response_kwargs)


class ProjectMainView(ListView):
    model = Project
    paginate_by = 10
    context_object_name = 'project_list'

    def get_context_data(self, **kwargs):
        ctx = super(ProjectMainView, self).get_context_data(**kwargs)
        ctx['form'] = ProjectForm()
        ctx['task_form'] = TaskForm()
        return ctx

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner__exact=self.request.user) |
            Q(followers__exact=self.request.user)
        )