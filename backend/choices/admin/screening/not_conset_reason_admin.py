# choices/admin/screening/not_enrolled_reason_admin.py

from django.contrib import admin
from choices.models import NotConsetReason
from ..base_admin import BaseChoiceAdmin


@admin.register(NotConsetReason)
class NotConsetReasonAdmin(BaseChoiceAdmin):
    pass