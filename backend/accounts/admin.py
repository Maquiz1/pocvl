from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, StaffProfile, Prefix, Position


# =========================
# 🔐 CUSTOM USER ADMIN
# =========================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),

        ("Personal Info", {
            "fields": ("first_name", "last_name"),
        }),

        ("Permissions", {
            "fields": (
                "is_staff",
                "is_superuser",
                "is_active",
                "groups",
                "user_permissions",
            )
        }),

        ("Important dates", {
            "fields": ("last_login",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",
                "last_name",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )


# =========================
# 👨‍⚕️ STAFF PROFILE ADMIN
# =========================
@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):

    list_display = (
        "display_name",
        "user_email",
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

    # 🚀 OPTIMIZATION (avoids N+1 queries)
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "prefix", "position", "site")

    # 👤 FULL DISPLAY NAME
    def display_name(self, obj):
        return obj.display_name

    display_name.short_description = "Full Name"
    display_name.admin_order_field = "user__first_name"

    # 📧 EMAIL COLUMN
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"


# =========================
# 🏷 PREFIX ADMIN
# =========================
@admin.register(Prefix)
class PrefixAdmin(admin.ModelAdmin):
    search_fields = ["name"]


# =========================
# 🧑‍⚕️ POSITION ADMIN
# =========================
@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]