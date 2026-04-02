from django.core.management.base import BaseCommand
import pandas as pd
import os
from datetime import datetime

# import your models
from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf1 import (
    CRF1, CRF1OtherMedical, CRF1OtherHerbal, CRF1Nimregenin,
    CRF1Radiotherapy, CRF1Chemotherapy, CRF1Surgery
)
from herbal.models.crfs.crf2 import CRF2, CRF2OtherPhysclExam
from herbal.models.crfs.crf3 import CRF3
from herbal.models.crfs.crf4 import CRF4
from herbal.models.crfs.crf5 import CRF5
from herbal.models.crfs.crf6 import CRF6
from herbal.models.crfs.crf7 import CRF7


EXCLUDED_FIELDS = {
    "created_at", "updated_at", "created_by", "updated_by",
    "deleted_at", "deleted_by", "is_active", "is_deleted",
    "id","delete_reason","inclusion_criteria_met","exclusion_criteria_met",
    "cancer_types","after_visit","crf","crf2","ae_staff","clinician_name",
    "cpersid","region","district","ward", "subject","screening","enrollment","visit",
}

def get_subject_id(obj):
    """Resolve subject_id from different relationship paths"""
    # direct subject FK
    if hasattr(obj, "subject") and obj.subject:
        return getattr(obj.subject, "subject_id", None)
    # via screening
    if hasattr(obj, "screening") and obj.screening and hasattr(obj.screening, "subject"):
        return getattr(obj.screening.subject, "subject_id", None)
    # via enrollment
    if hasattr(obj, "enrollment") and obj.enrollment and hasattr(obj.enrollment, "subject"):
        return getattr(obj.enrollment.subject, "subject_id", None)
    # via visit
    if hasattr(obj, "visit") and obj.visit and hasattr(obj.visit, "subject"):
        return getattr(obj.visit.subject, "subject_id", None)
    # # via CRF
    # if hasattr(obj, "visit") and obj.visit and hasattr(obj.visit, "subject"):
    #     return getattr(obj.visit.subject, "subject_id", None)
    # fallback for Subject itself
    if obj.__class__.__name__ == "Subject":
        return obj.id
    return None

def get_visit_code(obj):
    """Resolve visit code for CRF1–CRF7 models"""
    visit = getattr(obj, "visit", None)
    if visit:
        return getattr(visit, "code", None)
    # fallback via enrollment -> visit
    enrollment = getattr(obj, "enrollment", None)
    if enrollment and hasattr(enrollment, "visitday_set"):
        visits = getattr(enrollment, "visitday_set").all()
        if visits.exists():
            return visits.first().code
    return None

def get_model_data(model):
    data = []
    fields = [f.name for f in model._meta.fields if f.name not in EXCLUDED_FIELDS]
    queryset = model.objects.all()
    
    for obj in queryset:
        row = {
            "subject_id": get_subject_id(obj)
        }
        # add visit_code only for CRF models
        if obj.__class__.__name__ in ["CRF1","CRF1OtherMedical","CRF1OtherHerbal","CRF1Nimregenin",
                                      "CRF1Radiotherapy","CRF1Chemotherapy","CRF1Surgery",
                                      "CRF2","CRF2OtherPhysclExam","CRF3","CRF4","CRF5","CRF6","CRF7"]:
            row["visit_day"] = get_visit_code(obj)
        
        for field in fields:
            value = getattr(obj, field)
            # Handle FK nicely
            if hasattr(value, "pk"):
                value = getattr(value, "label", None) or getattr(value, "name", None) or getattr(value, "code", None) or str(value)
            row[field] = value
        data.append(row)
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

        # ✅ path
        base_path = os.path.expanduser("~/Documents/WORKS/NIMR/NIMREGENIN/DataExport")
        os.makedirs(base_path, exist_ok=True)

        file_path = os.path.join(base_path, "Nimregenin_Data_Export.xlsx")
        file_path = os.path.join(
            base_path,
            f"Nimregenin_Data_{datetime.today().date()}.xlsx"
        )

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

            for name, model in models.items():
                data = get_model_data(model)
                df = pd.DataFrame(data)

                if not df.empty:
                    df.to_excel(writer, sheet_name=name[:31], index=False)

        self.stdout.write(self.style.SUCCESS(f"✅ Data exported to {file_path}"))