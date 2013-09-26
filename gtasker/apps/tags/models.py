# -*- coding: utf-8 -*-

__author__ = 'Gennady Denisov <denisovgena@gmail.com>'


from django.db import models
from django.utils.translation import \
    ugettext_lazy as _

from ..core.models import TimeStampedModel


class Tag(TimeStampedModel):
    name = models.CharField(_('Name'),
                            max_length=128)

    def __unicode__(self):
        return self.name