# choices/admin/education_level_admin.py

from django.contrib import admin
from choices.models import EducationLevel
from ..base_admin import BaseChoiceAdmin


@admin.register(EducationLevel)
class EducationLevelAdmin(BaseChoiceAdmin):
    pass