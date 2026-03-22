# choices/admin/marital_status_admin.py

from django.contrib import admin
from choices.models import MaritalStatus
from ..base_admin import BaseChoiceAdmin


@admin.register(MaritalStatus)
class MaritalStatusAdmin(BaseChoiceAdmin):
    pass