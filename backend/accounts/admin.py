from django.contrib import admin
from .models import User, StaffProfile, Prefix, Position,Us


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = (
        "display_name",   # 🔥 custom full name
        "role",
        "site",
        "position",
        "prefix",
    )

    search_fields = (
        "user__first_name",
        "user__last_name",
        "middle_name",
        "user__email",
    )

    list_filter = (
        "role",
        "site",
        "position",
        "prefix",
    )

    filter_horizontal = ("assigned_sites",)

    def display_name(self, obj):
        return obj.display_name

    display_name.short_description = "Full Name"
    
    
@admin.register(Prefix)
class PrefixAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]