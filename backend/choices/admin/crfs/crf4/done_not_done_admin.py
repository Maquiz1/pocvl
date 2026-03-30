# choices/models/crfs/crf2/anxiety_model.py

from django.contrib import admin
from choices.models import DoneNotDone
from ...base_admin import BaseChoiceAdmin

@admin.register(DoneNotDone)
class DoneNotDoneAdmin(BaseChoiceAdmin):
    pass

