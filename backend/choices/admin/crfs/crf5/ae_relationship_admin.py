from django.contrib import admin
from choices.models import AeRelationship
from ...base_admin import BaseChoiceAdmin

@admin.register(AeRelationship)
class AeRelationshipAdmin(BaseChoiceAdmin):
    pass