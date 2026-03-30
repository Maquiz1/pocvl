from django.contrib import admin
from choices.models import AeOutcome
from ...base_admin import BaseChoiceAdmin

@admin.register(AeOutcome)
class AeOutcomeAdmin(BaseChoiceAdmin):
    pass