from django.db import models
from core.models import AuditModel, ActiveModel


class VisitScheduleConfig(AuditModel, ActiveModel):

    visit_day = models.OneToOneField(
        "choices.VisitDay",
        on_delete=models.CASCADE,
        related_name="schedule_config"
    )

    offset_days = models.IntegerField(
        help_text="Days from enrollment date"
    )

    window_before = models.IntegerField(default=3)
    window_after = models.IntegerField(default=3)

    class Meta:
        ordering = ["visit_day__order"]

    def __str__(self):
        return f"{self.visit_day.code} → {self.offset_days} days"