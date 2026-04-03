import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from reports.tasks.reminder_log import mark_sent, already_sent
from reports.tasks.get_site_staff_emails import get_site_staff_emails

logger = logging.getLogger(__name__)


def send_visit_email(visit, reminder_type):
    try:
        # ✅ Prevent duplicate emails
        if already_sent(visit, reminder_type):
            return

        subject_id = getattr(visit.subject, "subject_id", "N/A")
        visit_name = getattr(visit.visit_day, "name", "N/A")
        site_name = getattr(getattr(visit.subject, "site", None), "name", "N/A")

        subject = f"[Visit Reminder] {visit_name} - {subject_id}"

        context = {
            "subject_id": subject_id,
            "visit_name": visit_name,
            "scheduled_date": visit.scheduled_date,
            "site_name": site_name,
            "reminder_type": reminder_type,
        }

        # ✅ Render templates
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

        # ✅ Email with BOTH text + HTML
        email = EmailMultiAlternatives(
            subject,
            text_content,  # plain text fallback
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        # ✅ Mark as sent
        mark_sent(visit, reminder_type)

        logger.info(f"Email sent for visit {visit.id} ({reminder_type})")

    except Exception as e:
        logger.error(f"Email failed for visit {visit.id}: {e}")