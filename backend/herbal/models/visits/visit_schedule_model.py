# herbal/models/visits/visit_schedule_model.py

from django.db import models
from django.utils import timezone

from core.models import BaseModel
from ..enrollments.enrollment_model import Enrollment


VISIT_DAY_CHOICES = [
    ("D0", "Day 0"),
    ("D7", "Day 7"),
    ("D14", "Day 14"),
    ("D30", "Day 30"),
    ("D60", "Day 60"),
    ("D90", "Day 90"),
    ("D120", "Day 120"),
]


MISSED_REASON_CHOICES = [
    ("patient_unavailable", "Patient Unavailable"),
    ("patient_refused", "Patient Refused"),
    ("transport_issue", "Transport Issue"),
    ("site_error", "Site Error"),
    ("medical_reason", "Medical Reason"),
    ("changed_location", "Changed Location"),
    ("other", "Other"),
]

class VisitSchedule(BaseModel):


    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="visits"
    )

    visit_day = models.CharField(
        max_length=10,
        choices=VISIT_DAY_CHOICES
    )

    scheduled_date = models.DateField()

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("missed", "Missed"),
        ("incomplete", "Incomplete"),
        ("na", "Not Applicable"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    missed_reason = models.CharField(
        max_length=50,
        choices=MISSED_REASON_CHOICES,
        blank=True,
        null=True
    )

    missed_comment = models.TextField(
        blank=True,
        null=True
    )
    
    actual_visit_date = models.DateField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["scheduled_date"]

        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "visit_day"],
                name="unique_enrollment_visit"
            )
        ]


    def is_overdue(self):

        return (
            self.status == "pending"
            and self.scheduled_date < timezone.now().date()
        )

    @property
    def subject(self):
        return self.enrollment.screening.subject

    @property
    def is_na(self):
        return self.status in ["missed", "na"]

    def __str__(self):
        return f"{self.enrollment.screening.subject.subject_id} - {self.visit_day}"


