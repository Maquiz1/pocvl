from django.conf import settings

def get_active_site_url():
    from utils.models import SiteConfiguration  # lazy import

    config = SiteConfiguration.objects.filter(
        is_active=True,
        is_deleted=False
    ).first()

    if config and config.site_url:
        return config.site_url.rstrip("/")  # ✅ avoid double slashes

    return getattr(settings, "SITE_URL", "#").rstrip("/")