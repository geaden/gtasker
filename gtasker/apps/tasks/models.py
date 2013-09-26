# -*- coding: utf-8 -*-
from django.db import models

from ..core.models import TimeStampedModel, OwnedModel
from ..core.helpers import nullable
from ..projects.models import Project
from ..profiles.models import TaskerUser


class Task(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=256, **nullable)
    assignee = models.ForeignKey(TaskerUser,
                                 related_name='assigned_tasks',
                                 **nullable)
    due_date = models.DateTimeField(**nullable)
    project = models.ForeignKey(Project, related_name='tasks')
    attachment = models.URLField(**nullable)
    is_done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def done(self, *args, **kwargs):
        self.is_done = True
        self.save(*args, **kwargs)
