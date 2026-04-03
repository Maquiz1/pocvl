from reports.models import VisitReminderLog

from django.db import IntegrityError

def mark_sent(visit, reminder_type):
    try:
        VisitReminderLog.objects.create(
            visit=visit,
            reminder_type=reminder_type
        )
    except IntegrityError:
        pass  # already created by another worker