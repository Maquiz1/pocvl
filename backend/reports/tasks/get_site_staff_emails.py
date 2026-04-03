import logging
from django.conf import settings

logger = logging.getLogger(__name__)


def get_site_staff_emails(visit):
    """
    Safely returns a list of emails for site staff.
    Falls back to DEFAULT_FROM_EMAIL if none found.
    """

    try:
        subject = getattr(visit, "subject", None)
        site = getattr(subject, "site", None)

        if not site:
            logger.warning(f"No site found for visit {visit.id}")
            return [settings.DEFAULT_FROM_EMAIL]

        # ✅ OPTION 1: notification_emails field (comma-separated)
        notification_emails = getattr(site, "notification_emails", None)
        if notification_emails:
            emails = [
                e.strip() for e in notification_emails.split(",") if e.strip()
            ]
            if emails:
                return emails

        # ✅ OPTION 2: related users
        if hasattr(site, "users"):
            emails = list(
                site.users.filter(is_active=True)
                .exclude(email__isnull=True)
                .exclude(email__exact="")
                .values_list("email", flat=True)
            )
            if emails:
                return emails

        logger.warning(f"No staff emails found for site {site.id}")

    except Exception as e:
        logger.error(f"Error getting emails for visit {getattr(visit, 'id', 'unknown')}: {e}")

    # ✅ fallback (critical for production)
    return [settings.DEFAULT_FROM_EMAIL]