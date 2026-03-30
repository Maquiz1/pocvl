from django.contrib import admin

class BaseChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "code", "name", "label")
    search_fields = ("code", "name", "label", "description")
    list_filter = ("value",)
    ordering = ("id","value",)
    # ✅ Enable inline editing
    list_editable = ("value",)

    fieldsets = (
        ("Basic Information", {
            "fields": ("value", "code", "name", "label"),
        }),
        ("Additional Details", {
            "fields": ("description",),
            "classes": ("collapse",),
        }),
    )