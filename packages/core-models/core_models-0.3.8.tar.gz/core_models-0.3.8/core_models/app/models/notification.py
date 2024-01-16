from django.db import models

from . import Company
from .base import BaseModelAbstract


class Notification(BaseModelAbstract, models.Model):
    company = models.ForeignKey(Company, models.CASCADE, null=True, blank=True)
    notice_type = models.CharField(max_length=50, null=False, blank=False)
    object_id = models.UUIDField(null=True, blank=True)
    seen = models.BooleanField(default=False)

    def __unicode__(self):
        return f"Notification type: {self.notice_type} for: {self.created_by.email}"

    @property
    def text(self):
        return ''
