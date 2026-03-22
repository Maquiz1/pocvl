from django.contrib import admin
from choices.models import PatientCategory

class BaseChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "code", "name", "label")
    search_fields = ("code", "name", "label", "description")
    list_filter = ("value",)
    ordering = ("id",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("value", "code", "name", "label"),
        }),
        ("Additional Details", {
            "fields": ("description",),
            "classes": ("collapse",),
        }),
    )