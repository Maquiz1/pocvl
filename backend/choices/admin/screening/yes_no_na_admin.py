# choices/admin/screening/yes_no_admin.py

from django.contrib import admin
from choices.models import YesNoNa
from ..base_admin import BaseChoiceAdmin


@admin.register(YesNoNa)
class YesNoNaAdmin(BaseChoiceAdmin):
    pass