# choices/models/crfs/crf2/mobility_model.py

from django.contrib import admin
from choices.models import Mobility
from ...base_admin import BaseChoiceAdmin

@admin.register(Mobility)
class MobilityAdmin(BaseChoiceAdmin):
    pass


