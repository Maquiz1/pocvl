# herbal/models/crfs/crf5_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from ...enrollments.enrollment_model import Enrollment
from core.models import BaseModel


class CRF5(BaseModel):

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="adverse_events"
    )

    event_date = models.DateField()

    # 🔥 THIS IS WHERE IT GOES
    after_visit = models.ForeignKey(
        VisitSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="adverse_after"
    )
    
    event_description = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=[
            ("mild","Mild"),
            ("moderate","Moderate"),
            ("severe","Severe")
        ]
    )

    action_taken = models.TextField(blank=True)

    outcome = models.TextField(blank=True)
