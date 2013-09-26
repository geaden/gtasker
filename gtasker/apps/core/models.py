from django.db import models

# Create your models here.

from ..profiles.models import TaskerUser


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides
    self-updating 'created' and 'modified' fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    """
    An abstract class for owned models
    """
    owner = models.ForeignKey(TaskerUser)

    class Meta:
        abstract = True
