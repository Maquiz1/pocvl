from django.db import models

from herbal.models.visits.visit_schedule_model import VisitSchedule

# class VisitReminderLog(models.Model):
#     visit = models.ForeignKey(VisitSchedule, on_delete=models.CASCADE)
#     reminder_type = models.CharField(max_length=50)
#     sent_at = models.DateTimeField(auto_now_add=True)
    
    
REMINDER_TYPES = [
    ("3_day", "3 Days Before"),
    ("1_day", "1 Day Before"),
    ("same_day", "Same Day"),
    ("overdue", "Overdue Weekly"),
]


class VisitReminderLog(models.Model):
    visit = models.ForeignKey(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="reminder_logs"
    )
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("visit", "reminder_type")  # 🚀 KEY PART
