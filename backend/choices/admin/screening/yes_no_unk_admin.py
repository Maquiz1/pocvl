# choices/admin/screening/yes_no_admin.py

from django.contrib import admin
from choices.models import YesNoUnk
from ..base_admin import BaseChoiceAdmin


@admin.register(YesNoUnk)
class YesNoUnkAdmin(BaseChoiceAdmin):
    pass