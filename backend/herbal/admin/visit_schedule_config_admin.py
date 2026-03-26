# choices/admin/visit_schedule_config_admin.py

from django.contrib import admin
from herbal.models import VisitScheduleConfig


@admin.register(VisitScheduleConfig)
class VisitScheduleConfigAdmin(admin.ModelAdmin):
    list_display = (
        "visit_day",
        "offset_days",
        "window_before",
        "window_after",
        "is_active",
    )
    ordering = ("visit_day__order",)
    list_filter = ("is_active",)
    search_fields = ("visit_day__code", "visit_day__name")