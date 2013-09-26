# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import \
    ugettext_lazy as _
from django.db import models

from ..core.models import TimeStampedModel, OwnedModel
from ..profiles.models import TaskerUser

from ..core.helpers import COLOR_CHOICES, nullable

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


class Project(TimeStampedModel, OwnedModel):
    name = models.CharField(max_length=128)
    notes = models.CharField(max_length=256, **nullable)
    followers = models.ManyToManyField(TaskerUser,
                                       related_name='projects',
                                       **nullable)
    start_date = models.DateTimeField(**nullable)
    finish_date = models.DateTimeField(**nullable)
    archived = models.BooleanField(default=False)
    color = models.PositiveSmallIntegerField(
        choices=COLOR_CHOICES, default=1, help_text=_('Select color for project'))
    finished_at = models.DateTimeField(**nullable)

    def get_absolute_url(self):
        return reverse_lazy('projects:details', self.pk)

    @property
    def is_finished(self):
        if self.finish_date or self.finish_date:
            return True
        return False

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.finish_date:
            self.finish_date = self.finish_date
        return super(Project, self).save(force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    class Meta:
        ordering = ['-created_at']

