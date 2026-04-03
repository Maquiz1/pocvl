from celery import shared_task
from django.utils import timezone

from herbal.models.visits.visit_schedule_model import VisitSchedule
from reports.tasks.send_visit_email import send_visit_email


@shared_task
def send_overdue_visit_reminders():
    today = timezone.now().date()

    # ✅ Run only on Sunday
    if today.weekday() != 6:
        return

    overdue_visits = VisitSchedule.objects.filter(
        status="pending",
        scheduled_date__lt=today
    )

    for visit in overdue_visits:
        send_visit_email(visit, "overdue")