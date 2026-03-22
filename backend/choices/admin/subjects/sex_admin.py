# choices/admin/sex_admin.py

from django.contrib import admin
from choices.models import Sex
from ..base_admin import BaseChoiceAdmin


@admin.register(Sex)
class SexAdmin(BaseChoiceAdmin):
    pass