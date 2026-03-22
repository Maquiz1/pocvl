# choices/admin/screening/yes_no_admin.py

from django.contrib import admin
from choices.models import YesNo


@admin.register(YesNo)
class YesNoAdmin(admin.ModelAdmin):
    list_display = ['id','value','code', 'name']
    ordering = ['id']
    search_fields = ['name']