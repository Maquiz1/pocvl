# choices/admin/occupation_admin.py

from django.contrib import admin
from choices.models import Occupation
from ..base_admin import BaseChoiceAdmin


@admin.register(Occupation)
class OccupationAdmin(BaseChoiceAdmin):
    pass