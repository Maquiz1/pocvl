# choices/admin/id_type_admin.py

from django.contrib import admin
from choices.models import IDType

@admin.register(IDType)
class IDTypeAdmin(admin.ModelAdmin):
    list_display = ['id','value', 'code', 'name']
    ordering = ['id']
    search_fields = ['code', 'name']