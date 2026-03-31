from django.contrib import admin
from choices.models import WithdrewReason
from ...base_admin import BaseChoiceAdmin

@admin.register(WithdrewReason)
class WithdrewReasonAdmin(BaseChoiceAdmin):
    pass