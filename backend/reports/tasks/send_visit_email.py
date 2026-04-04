import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from reports.tasks.reminder_log import mark_sent, already_sent
from reports.tasks.get_site_staff_emails import get_site_staff_emails
from utils.sites import get_active_site_url

from utils.models import EmailLog  # ✅ ADD THIS

logger = logging.getLogger(__name__)


def send_visit_email(visit, reminder_type):
    try:
        # ✅ Prevent duplicate emails
        if already_sent(visit, reminder_type):
            logger.info(f"Skipped duplicate email for visit {visit.id} ({reminder_type})")
            return

        subject_obj = visit.subject

        subject_id = getattr(subject_obj, "subject_id", "N/A")
        visit_name = getattr(visit.visit_day, "name", "N/A")
        site_name = getattr(getattr(subject_obj, "site", None), "name", "N/A")

        base_url = get_active_site_url()

        if base_url == "#":
            logger.warning("No active SiteConfiguration found")

        subject_url = f"{base_url}/subjects/{subject_obj.id}/"

        subject = f"[Visit Reminder] {visit_name} - {subject_id}"

        context = {
            "subject_id": subject_id,
            "visit_name": visit_name,
            "scheduled_date": visit.scheduled_date,
            "site_name": site_name,
            "reminder_type": reminder_type,
            "subject_url": subject_url,
        }

        text_content = render_to_string(
            "emails/visit_reminder/visit_reminder.txt",
            context
        )

        html_content = render_to_string(
            "emails/visit_reminder/visit_reminder.html",
            context
        )

        recipient_list = get_site_staff_emails(visit)

        if not recipient_list:
            logger.warning(f"No recipients for visit {visit.id}")
            return

        # ✅ Send email
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        # ✅ Mark as sent (your existing logic)
        mark_sent(visit, reminder_type)

        # ✅ LOG SUCCESS (loop recipients)
        for recipient in recipient_list:
            EmailLog.objects.create(
                recipient=recipient,
                subject=subject,
                status="sent",
                task_type=f"visit_reminder_{reminder_type}",
            )

        logger.info(
            f"Email sent for visit {visit.id} ({reminder_type}) to {len(recipient_list)} recipients"
        )

    except Exception as e:
        error_msg = str(e)

        logger.error(
            f"Email failed for visit {visit.id}: {error_msg}",
            exc_info=True
        )

        # ✅ LOG FAILURE (loop recipients if available)
        try:
            recipient_list = get_site_staff_emails(visit)
        except Exception:
            recipient_list = []

        for recipient in recipient_list or ["unknown"]:
            EmailLog.objects.create(
                recipient=recipient,
                subject=f"[Visit Reminder Failed] Visit {visit.id}",
                status="failed",
                error_message=error_msg,
                task_type=f"visit_reminder_{reminder_type}",
            )