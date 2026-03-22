from django.contrib import admin
from choices.models import Appearance
from ...base_admin import BaseChoiceAdmin

@admin.register(Appearance)
class AppearanceAdmin(BaseChoiceAdmin):
    pass