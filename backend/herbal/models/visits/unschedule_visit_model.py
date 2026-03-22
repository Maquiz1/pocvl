# herbal/models/visits/unschedule_visit_model.py

from django.db import models
from ..enrollments.enrollment_model import Enrollment
from .visit_schedule_model import VisitSchedule   # 👈 IMPORT THIS
from core.models import BaseModel


REASON_CHOICES = [
    ("ae", "Adverse Event"),
    ("unscheduled_followup", "Unscheduled Follow-up"),
    ("protocol_deviation", "Protocol Deviation"),
    ("missed_visit_followup", "Missed Visit Follow-up"),
    ("other", "Other"),
]


class UnscheduledVisit(BaseModel):

    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="unscheduled_visits"
    )

    visit_date = models.DateField()

    # 🔥 THIS IS WHERE IT GOES
    after_visit = models.ForeignKey(
        VisitSchedule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="unscheduled_after"
    )

    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        if self.after_visit:
            return f"Unscheduled after {self.after_visit.get_visit_day_display()} - {self.enrollment.screening.subject}"
        return f"Unscheduled - {self.enrollment.screening.subject}"