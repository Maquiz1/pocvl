# choices/models/crfs/crf2/painmodel.py

from django.contrib import admin
from choices.models import Pain
from ...base_admin import BaseChoiceAdmin

@admin.register(Pain)
class PainAdmin(BaseChoiceAdmin):
    pass


