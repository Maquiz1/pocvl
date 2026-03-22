from django.db import models
from core.models import BaseModel
from herbal.models.visits.visit_schedule_model import VisitSchedule
from django.conf import settings

User = settings.AUTH_USER_MODEL


class DataQuery(BaseModel):

    visit = models.ForeignKey(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="queries"
    )

    field_name = models.CharField(
        max_length=100
    )

    query_text = models.TextField()

    raised_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="queries_raised"
    )

    STATUS_CHOICES = [
        ("open", "Open"),
        ("answered", "Answered"),
        ("closed", "Closed"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open"
    )

    response = models.TextField(
        blank=True,
        null=True
    )

    responded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="queries_responded"
    )

    def __str__(self):
        return f"Query on {self.visit} - {self.field_name}"