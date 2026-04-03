from django.conf import settings

def get_active_site_url():
    from core.models import SiteConfiguration  # import only when needed
    config = SiteConfiguration.objects.filter(is_active=True, is_deleted=False).first()
    if config:
        return config.site_url
    return getattr(settings, "SITE_URL", "#")
