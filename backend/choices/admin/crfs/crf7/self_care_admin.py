# choices/models/crfs/crf2/appearance_model.py

from django.contrib import admin
from choices.models import SelfCare
from ...base_admin import BaseChoiceAdmin

@admin.register(SelfCare)
class SelfCareAdmin(BaseChoiceAdmin):
    pass


