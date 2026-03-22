from django.contrib import admin
from choices.models import TreatmentType
from ..base_admin import BaseChoiceAdmin

@admin.register(TreatmentType)
class TreatmentTypeAdmin(BaseChoiceAdmin):
    pass