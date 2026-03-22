# choices/admin/id_type_admin.py

from django.contrib import admin
from choices.models import IDType
from ..base_admin import BaseChoiceAdmin

@admin.register(IDType)
class IDTypeAdmin(BaseChoiceAdmin):
    pass