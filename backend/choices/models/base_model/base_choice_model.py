# choices/models/enrollments/base_choice_model.py

from django.db import models
from core.models import AuditModel

class BaseChoiceModel(AuditModel):
    value = models.IntegerField()
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    label = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["id"]

    def __str__(self):
        return self.name or ""