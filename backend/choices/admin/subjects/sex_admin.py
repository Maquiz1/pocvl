# choices/admin/sex_admin.py

from django.contrib import admin
from choices.models import Sex


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    ordering = ['id']