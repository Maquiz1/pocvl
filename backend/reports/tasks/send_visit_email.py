import logging
from django.core.mail import send_mail
from django.conf import settings

from reports.tasks.reminder_log import mark_sent, already_sent
from reports.tasks.get_site_staff_emails import get_site_staff_emails

logger = logging.getLogger(__name__)


def send_visit_email(visit, reminder_type):
    """
    Sends visit reminder email to site staff.
    Prevents duplicate sending per reminder type.
    """

    try:
        # ✅ Prevent duplicate emails
        if already_sent(visit, reminder_type):
            logger.info(f"Skipping duplicate {reminder_type} for visit {visit.id}")
            return

        subject_id = getattr(visit.subject, "subject_id", "N/A")
        visit_name = getattr(visit.visit_day, "name", "N/A")
        site_name = getattr(getattr(visit.subject, "site", None), "name", "N/A")

        subject = f"[Visit Reminder] {visit_name} - {subject_id}"

        message = f"""
Patient ID: {subject_id}
Visit: {visit_name}
Scheduled Date: {visit.scheduled_date}
Site: {site_name}

Reminder Type: {reminder_type}

Please follow up accordingly.
        """

        recipient_list = get_site_staff_emails(visit)

        if not recipient_list:
            logger.warning(f"No recipients for visit {visit.id}")
            return

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )

        # ✅ Mark as sent AFTER success
        mark_sent(visit, reminder_type)

        logger.info(f"Email sent for visit {visit.id} ({reminder_type})")

    except Exception as e:
        logger.error(f"Email sending failed for visit {visit.id}: {e}")