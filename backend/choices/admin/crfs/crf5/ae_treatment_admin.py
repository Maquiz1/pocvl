from django.contrib import admin
from choices.models import AeTreatment
from ...base_admin import BaseChoiceAdmin

@admin.register(AeTreatment)
class AeTreatmentAdmin(BaseChoiceAdmin):
    pass