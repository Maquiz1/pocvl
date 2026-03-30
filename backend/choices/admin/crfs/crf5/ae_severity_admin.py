from django.contrib import admin
from choices.models import AeSeverity
from ...base_admin import BaseChoiceAdmin

@admin.register(AeSeverity)
class AeSeverityAdmin(BaseChoiceAdmin):
    pass