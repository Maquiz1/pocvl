# herbal/admin/cancers/cancer_type_admin.py

from django.contrib import admin
from herbal.models import CancerType


@admin.register(CancerType)
class CancerTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    # list_filter = ("is_active",)