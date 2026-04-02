from celery import shared_task
from django.conf import settings
import pandas as pd
import os
from datetime import datetime

from herbal.models import Subject, Screening, Enrollment, VisitSchedule
from herbal.models.crfs.crf1 import *
from herbal.models.crfs.crf2 import *
from herbal.models.crfs.crf3 import CRF3
from herbal.models.crfs.crf4 import CRF4
from herbal.models.crfs.crf5 import CRF5
from herbal.models.crfs.crf6 import CRF6
from herbal.models.crfs.crf7 import CRF7

from utils.management.commands.export_data import get_subject_id, get_visit_code, EXCLUDED_FIELDS


@shared_task(bind=True)
def export_data_task(self):
    models = {
        "Subject": Subject,
        "Screening": Screening,
        "Enrollment": Enrollment,
        "Visits": VisitSchedule,
        "CRF1": CRF1,
        "CRF2": CRF2,
        "CRF3": CRF3,
        "CRF4": CRF4,
        "CRF5": CRF5,
        "CRF6": CRF6,
        "CRF7": CRF7,
    }

    base_path = os.path.join(settings.MEDIA_ROOT, "exports")
    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(
        base_path,
        f"Nimregenin_Data_{datetime.today().date()}_{self.request.id}.xlsx"
    )

    total_models = len(models)
    
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for i, (name, model) in enumerate(models.items()):
            data = []
            fields = [f.name for f in model._meta.fields if f.name not in EXCLUDED_FIELDS]

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

            # ✅ update progress
            progress = int(((i + 1) / total_models) * 100)
            self.update_state(state="PROGRESS", meta={"progress": progress})

        # after file is created
        relative_path = file_path.replace(settings.MEDIA_ROOT, "")
        file_url = settings.MEDIA_URL + relative_path.replace("\\", "/")

        return {
            "progress": 100,
            "file": file_url
        }
        
    return {"progress": 100, "file": file_path}