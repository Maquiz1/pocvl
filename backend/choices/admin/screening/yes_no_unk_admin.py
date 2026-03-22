# choices/admin/screening/yes_no_admin.py

from django.contrib import admin
from choices.models import YesNoUnk


@admin.register(YesNoUnk)
class YesNoUnkAdmin(admin.ModelAdmin):
    list_display = ['id','value','code', 'name']
    ordering = ['id']
    search_fields = ['name']