from django.contrib import admin
from choices.models import TerminationReason
from ...base_admin import BaseChoiceAdmin

@admin.register(TerminationReason)
class TerminationReasonAdmin(BaseChoiceAdmin):
    pass