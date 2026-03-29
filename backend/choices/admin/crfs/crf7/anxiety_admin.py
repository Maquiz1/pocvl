# choices/models/crfs/crf2/anxiety_model.py

from django.contrib import admin
from choices.models import Anxiety
from ...base_admin import BaseChoiceAdmin

@admin.register(Anxiety)
class AnxietyAdmin(BaseChoiceAdmin):
    pass

