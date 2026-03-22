from django.contrib import admin
from choices.models import PatientCategory
from ..base_admin import BaseChoiceAdmin

@admin.register(PatientCategory)
class PatientCategoryAdmin(BaseChoiceAdmin):
    pass