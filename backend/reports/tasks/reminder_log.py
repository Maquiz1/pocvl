from reports.models import VisitReminderLog


def already_sent(visit, reminder_type):
    return VisitReminderLog.objects.filter(
        visit=visit,
        reminder_type=reminder_type
    ).exists()


def mark_sent(visit, reminder_type):
    VisitReminderLog.objects.create(
        visit=visit,
        reminder_type=reminder_type
    )