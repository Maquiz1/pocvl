from django.contrib import admin
from choices.models import Method
from ...base_admin import BaseChoiceAdmin

@admin.register(Method)
class MethodAdmin(BaseChoiceAdmin):
    pass