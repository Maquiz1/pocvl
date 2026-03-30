from django.contrib import admin
from choices.models import AeActionTaken
from ...base_admin import BaseChoiceAdmin

@admin.register(AeActionTaken)
class AeActionTakenAdmin(BaseChoiceAdmin):
    pass