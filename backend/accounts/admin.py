from django.contrib import admin
from .models import User, StaffProfile, Prefix, Position
from django.contrib.auth.admin import UserAdmin


# class StaffProfileInline(admin.StackedInline):
#     model = StaffProfile
#     can_delete = False
#     extra = 0


# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     model = User

#     inlines = [StaffProfileInline]   # 🔥 add this

#     list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),

        ("Personal Info", {   # 🔥 NEW
            "fields": ("first_name", "last_name")
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

        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "first_name",   # 🔥 NEW
                "last_name",    # 🔥 NEW
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )
    
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