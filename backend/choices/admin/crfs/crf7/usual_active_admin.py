# choices/models/crfs/crf2/appearance_model.py

from django.contrib import admin
from choices.models import UsualActive
from ...base_admin import BaseChoiceAdmin

@admin.register(UsualActive)
class UsualActiveAdmin(BaseChoiceAdmin):
    pass

