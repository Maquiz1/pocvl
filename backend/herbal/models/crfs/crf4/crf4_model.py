# herbal/models/crfs/crf4_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel



class CRF4(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf4"
    )

    medication_given = models.BooleanField(default=False)

    dosage = models.CharField(max_length=100, blank=True)

    adherence = models.BooleanField(default=True)

    comments = models.TextField(blank=True)
