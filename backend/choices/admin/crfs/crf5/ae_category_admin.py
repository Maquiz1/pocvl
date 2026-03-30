from django.contrib import admin
from choices.models import AeCategory
from ...base_admin import BaseChoiceAdmin

@admin.register(AeCategory)
class AeCategoryAdmin(BaseChoiceAdmin):
    pass