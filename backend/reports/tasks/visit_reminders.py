from celery import shared_task
from django.utils import timezone

from herbal.models.visits.visit_schedule_model import VisitSchedule
from reports.tasks.send_visit_email import send_visit_email


@shared_task
def send_visit_reminders():
    today = timezone.now().date()

    visits = VisitSchedule.objects.filter(status="pending")

    for visit in visits:
        days_diff = (visit.scheduled_date - today).days

        if days_diff == 3:
            send_visit_email(visit, "3_day")

        elif days_diff == 1:
            send_visit_email(visit, "1_day")

        elif days_diff == 0:
            send_visit_email(visit, "same_day")