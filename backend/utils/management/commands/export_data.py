from django.core.management.base import BaseCommand
import pandas as pd
import os
from datetime import datetime

# import your models
from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf1 import (
    CRF1,
    CRF1OtherMedical,
    CRF1OtherHerbal,
    CRF1Nimregenin,
    CRF1Radiotherapy,
    CRF1Chemotherapy,
    CRF1Surgery,
)
from herbal.models.crfs.crf2 import CRF2, CRF2OtherPhysclExam
from herbal.models.crfs.crf3 import CRF3
from herbal.models.crfs.crf4 import CRF4
from herbal.models.crfs.crf5 import CRF5
from herbal.models.crfs.crf6 import CRF6
from herbal.models.crfs.crf7 import CRF7

EXCLUDED_FIELDS = {
    "created_at", "updated_at", "created_by", "updated_by", "deleted_at", "deleted_by",
    "is_active", "is_deleted", "id", "delete_reason", "inclusion_criteria_met",
    "exclusion_criteria_met", "cancer_types", "after_visit", "crf", "crf2",
    "ae_staff", "clinician_name", "cpersid", "region", "district", "ward",
    "subject", "screening", "enrollment", "visit",
}

def get_subject_id(obj):
    """Resolve subject_id from different relationship paths"""
    if hasattr(obj, "subject") and obj.subject:
        return getattr(obj.subject, "subject_id", None)
    if hasattr(obj, "screening") and obj.screening and hasattr(obj.screening, "subject"):
        return getattr(obj.screening.subject, "subject_id", None)
    if hasattr(obj, "enrollment") and obj.enrollment:
        screening = getattr(obj.enrollment, "screening", None)
        if screening and hasattr(screening, "subject"):
            return getattr(screening.subject, "subject_id", None)
    visit = getattr(obj, "visit", None)
    if visit:
        enrollment = getattr(visit, "enrollment", None)
        if enrollment and hasattr(enrollment, "screening") and hasattr(enrollment.screening, "subject"):
            return getattr(enrollment.screening.subject, "subject_id", None)
    crf = getattr(obj, "crf", None)
    if crf and getattr(crf, "visit", None):
        enrollment = getattr(crf.visit, "enrollment", None)
        if enrollment and hasattr(enrollment, "screening") and hasattr(enrollment.screening, "subject"):
            return getattr(enrollment.screening.subject, "subject_id", None)
    crf2 = getattr(obj, "crf2", None)
    if crf2 and getattr(crf2, "visit", None):
        enrollment = getattr(crf2.visit, "enrollment", None)
        if enrollment and hasattr(enrollment, "screening") and hasattr(enrollment.screening, "subject"):
            return getattr(enrollment.screening.subject, "subject_id", None)
    if obj.__class__.__name__ == "Subject":
        return getattr(obj, "subject_id", getattr(obj, "id", None))
    return None

def get_visit_code(obj):
    """Resolve visit code for VisitSchedule and CRFs"""
    if hasattr(obj, "visit_day") and obj.visit_day:
        return getattr(obj.visit_day, "code", None)
    visit = getattr(obj, "visit", None)
    if visit and hasattr(visit, "visit_day") and visit.visit_day:
        return getattr(visit.visit_day, "code", None)
    crf = getattr(obj, "crf", None)
    if crf and getattr(crf, "visit", None) and hasattr(crf.visit, "visit_day") and crf.visit.visit_day:
        return getattr(crf.visit.visit_day, "code", None)
    crf2 = getattr(obj, "crf2", None)
    if crf2 and getattr(crf2, "visit", None) and hasattr(crf2.visit, "visit_day") and crf2.visit.visit_day:
        return getattr(crf2.visit.visit_day, "code", None)
    enrollment = getattr(obj, "enrollment", None)
    if enrollment and hasattr(enrollment, "visits") and enrollment.visits.exists():
        first_visit = enrollment.visits.first()
        if first_visit and hasattr(first_visit, "visit_day") and first_visit.visit_day:
            return getattr(first_visit.visit_day, "code", None)
    return None

def get_model_data(model):
    data = []
    fields = [f.name for f in model._meta.fields if f.name not in EXCLUDED_FIELDS]
    queryset = model.objects.all()

    for obj in queryset:
        row = {"subject_id": get_subject_id(obj)}
        # add visit_code only for CRFs & VisitSchedule
        if hasattr(obj, "visit") or hasattr(obj, "crf") or hasattr(obj, "crf2") or hasattr(obj, "visit_day"):
            row["visit_code"] = get_visit_code(obj)
        for field in fields:
            value = getattr(obj, field, None)
            if hasattr(value, "pk"):
                value = getattr(value, "label", None) or getattr(value, "name", None) or getattr(value, "code", None) or str(value)
            row[field] = value
        data.append(row)

    # Apply ordering
    # Apply ordering
    cls_name = model.__name__
    if cls_name in ["Subject", "Screening", "Enrollment", "CRF5", "CRF6"]:
        data.sort(key=lambda x: x.get("subject_id"))
    else:  # CRF1, CRF2, CRF3, CRF4, CRF7, submodels, VisitSchedule
        def visit_sort_key(x):
            # Extract numeric part of visit_code for proper sorting
            visit_code = x.get("visit_code")
            try:
                number = int(''.join(filter(str.isdigit, visit_code))) if visit_code else -1
            except ValueError:
                number = -1
            return (x.get("subject_id"), number)
        
        data.sort(key=visit_sort_key)

    return data

class Command(BaseCommand):
    help = "Export all model data to Excel"

    def handle(self, *args, **kwargs):
        models = {
            "Subject": Subject,
            "Screening": Screening,
            "Enrolment": Enrollment,
            "Visits": VisitSchedule,
            "CRF1": CRF1,
            "CRF1OtherMedical": CRF1OtherMedical,
            "CRF1OtherHerbal": CRF1OtherHerbal,
            "CRF1Nimregenin": CRF1Nimregenin,
            "CRF1Radiotherapy": CRF1Radiotherapy,
            "CRF1Chemotherapy": CRF1Chemotherapy,
            "CRF1Surgery": CRF1Surgery,
            "CRF2": CRF2,
            "CRF2OtherPhysclExam": CRF2OtherPhysclExam,
            "CRF3": CRF3,
            "CRF4": CRF4,
            "CRF5": CRF5,
            "CRF6": CRF6,
            "CRF7": CRF7,
        }

        base_path = os.path.expanduser("~/Documents/WORKS/NIMR/NIMREGENIN/DataExport")
        os.makedirs(base_path, exist_ok=True)
        file_path = os.path.join(base_path, f"Nimregenin_Data_{datetime.today().date()}.xlsx")

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
            for name, model in models.items():
                data = get_model_data(model)
                df = pd.DataFrame(data)
                if not df.empty:
                    df.to_excel(writer, sheet_name=name[:31], index=False)

        self.stdout.write(self.style.SUCCESS(f"✅ Data exported to {file_path}"))