# choices/admin/occupation_admin.py

from django.contrib import admin
from choices.models import Occupation


@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ['id','value', 'name']
    ordering = ['id']
    search_fields = ['name']