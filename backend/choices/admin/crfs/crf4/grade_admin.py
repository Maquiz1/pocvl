# choices/models/crfs/crf2/anxiety_model.py

from django.contrib import admin
from choices.models import Grade
from ...base_admin import BaseChoiceAdmin

@admin.register(Grade)
class GradeAdmin(BaseChoiceAdmin):
    pass

