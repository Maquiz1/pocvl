from celery import shared_task
from reports.tasks.send_visit_email import send_visit_email


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_visit_email_task(self, visit_id, reminder_type):
    from herbal.models.visits.visit_schedule_model import VisitSchedule

    visit = VisitSchedule.objects.get(id=visit_id)
    send_visit_email(visit, reminder_type)