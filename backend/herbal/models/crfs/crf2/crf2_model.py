# herbal/models/crfs/crf2_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel


class CRF2(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf2"
    )

    lab_result = models.TextField()

    test_date = models.DateField()

    comments = models.TextField(blank=True)
