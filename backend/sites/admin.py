from django.contrib import admin
from sites.models import Site
from choices.admin import BaseChoiceAdmin

@admin.register(Site)
class SiteAdmin(BaseChoiceAdmin):
    pass
