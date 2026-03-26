# choices/models/visits/visit_day_model.py

from django.db import models
from choices.models import BaseChoiceModel

class VisitDay(BaseChoiceModel):
    order = models.PositiveIntegerField()               # for sorting

    class Meta:
        ordering = ["order"]
        verbose_name = "Visit Day"
        verbose_name_plural = "Visit Days"

    
    