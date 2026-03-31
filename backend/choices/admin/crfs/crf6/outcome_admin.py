from django.contrib import admin
from choices.models import OutCome
from ...base_admin import BaseChoiceAdmin

@admin.register(OutCome)
class OutComeAdmin(BaseChoiceAdmin):
    pass