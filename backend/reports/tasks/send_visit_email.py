import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from reports.tasks.reminder_log import mark_sent, already_sent
from reports.tasks.get_site_staff_emails import get_site_staff_emails
from utils.sites import get_active_site_url  # ✅ your util

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

        # ✅ Get base URL (DB or settings fallback)
        base_url = get_active_site_url()

        if base_url == "#":
            logger.warning("No active SiteConfiguration found, using fallback URL")

        # ✅ Build subject URL safely
        subject_url = f"{base_url}/subjects/{subject_obj.id}/"

        subject = f"[Visit Reminder] {visit_name} - {subject_id}"

        context = {
            "subject_id": subject_id,
            "visit_name": visit_name,
            "scheduled_date": visit.scheduled_date,
            "site_name": site_name,
            "reminder_type": reminder_type,
            "subject_url": subject_url,  # ✅ added
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

        # ✅ Get recipients
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

        # ✅ Mark as sent
        mark_sent(visit, reminder_type)

        logger.info(
            f"Email sent for visit {visit.id} ({reminder_type}) to {len(recipient_list)} recipients"
        )

    except Exception as e:
        logger.error(f"Email failed for visit {visit.id}: {str(e)}", exc_info=True)