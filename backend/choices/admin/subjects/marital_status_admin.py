# choices/admin/marital_status_admin.py

from django.contrib import admin
from choices.models import MaritalStatus


@admin.register(MaritalStatus)
class MaritalStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']
    ordering = ['id']
    search_fields = ['code', 'name']