from django.contrib import admin
from choices.models import PatientType
from ..base_admin import BaseChoiceAdmin

@admin.register(PatientType)
class PatientTypeAdmin(BaseChoiceAdmin):
    pass