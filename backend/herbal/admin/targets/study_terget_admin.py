# herbal/admin/cancers/cancer_type_admin.py

from django.contrib import admin
from herbal.models.targets.study_target_model import StudyTarget


@admin.register(StudyTarget)
class StudyTargetAdmin(admin.ModelAdmin):
    list_display = ("site","cancer_type", "target_enrollment")
    search_fields = ("cancer_type", "target_enrollment")
