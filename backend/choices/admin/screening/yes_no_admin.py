# choices/admin/screening/yes_no_admin.py

from django.contrib import admin
from choices.models import YesNo
from ..base_admin import BaseChoiceAdmin


@admin.register(YesNo)
class YesNoAdmin(BaseChoiceAdmin):
    pass