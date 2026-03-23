# herbal/admin/cancers/cancer_type_admin.py

from django.contrib import admin
from herbal.models import CancerType
from choices.admin import BaseChoiceAdmin

@admin.register(CancerType)
class CancerTypeAdmin(BaseChoiceAdmin):
    pass