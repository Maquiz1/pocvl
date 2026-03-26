# choices/admin/visit_day_admin.py


from django.contrib import admin
from choices.models import VisitDay
from ..base_admin import BaseChoiceAdmin


@admin.register(VisitDay)
class VisitDayAdmin(BaseChoiceAdmin):
    list_display = ("id", "order", "value", "code", "name", "label")
    ordering = ("order",)
    list_editable = ("order",)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)

        fields = list(fieldsets[0][1]["fields"])

        if "order" not in fields:
            fieldsets[0][1]["fields"] = ("order",) + tuple(fields)

        return fieldsets
