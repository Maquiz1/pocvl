# choices/admin/screening/not_enrolled_reason_admin.py

from django.contrib import admin
from choices.models import NotEnrolledReason
from ..base_admin import BaseChoiceAdmin


@admin.register(NotEnrolledReason)
class NotEnrolledReasonAdmin(BaseChoiceAdmin):
    pass