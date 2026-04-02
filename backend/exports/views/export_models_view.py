from django.shortcuts import render
from django.http import StreamingHttpResponse
from io import BytesIO
import pandas as pd
from datetime import datetime

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

from utils.management.commands.export_data import get_subject_id, get_visit_code, EXCLUDED_FIELDS

# Define models to export
MODELS_TO_EXPORT = {
    "Subject": Subject,
    "Screening": Screening,
    "Enrollment": Enrollment,
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

def export_models_view(request):
    """
    Export all specified models to an Excel file efficiently using streaming
    and queryset iterators to avoid memory crashes.
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, model in MODELS_TO_EXPORT.items():
            fields = [f.name for f in model._meta.fields if f.name not in EXCLUDED_FIELDS]
            data = []

            # Use iterator to avoid loading all rows at once
            for obj in model.objects.iterator():
                row = {"subject_id": get_subject_id(obj)}
                if hasattr(obj, "visit") or hasattr(obj, "crf") or hasattr(obj, "crf2") or hasattr(obj, "visit_day"):
                    row["visit_code"] = get_visit_code(obj)
                for field in fields:
                    value = getattr(obj, field, None)
                    if hasattr(value, "pk"):
                        value = getattr(value, "label", None) or getattr(value, "name", None) or getattr(value, "code", None) or str(value)
                    row[field] = value
                data.append(row)

            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=name[:31], index=False)

    output.seek(0)
    filename = f"Nimregenin_Data_{datetime.today().date()}.xlsx"
    response = StreamingHttpResponse(
        output,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response