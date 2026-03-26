       
# choices/admin/screening/not_enrolled_reason_admin.py

from django.contrib import admin
from choices.models import MissedVisitReason
from ..base_admin import BaseChoiceAdmin


@admin.register(MissedVisitReason)
class MissedVisitReasonAdmin(BaseChoiceAdmin):
    pass
