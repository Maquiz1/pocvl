from django.core.management.base import BaseCommand
import pandas as pd
import os

from utils.codebook import get_model_codebook

# import your models
from herbal.models import Subject, Screening, Enrollment,VisitSchedule
from herbal.models.crfs.crf1 import CRF1
from herbal.models.crfs.crf1 import CRF1OtherMedical
from herbal.models.crfs.crf1 import CRF1OtherHerbal
from herbal.models.crfs.crf1 import CRF1Nimregenin
from herbal.models.crfs.crf1 import CRF1Radiotherapy
from herbal.models.crfs.crf1 import CRF1Chemotherapy
from herbal.models.crfs.crf1 import CRF1Surgery
from herbal.models.crfs.crf2 import CRF2
from herbal.models.crfs.crf2 import CRF2OtherPhysclExam
from herbal.models.crfs.crf3 import CRF3
from herbal.models.crfs.crf4 import CRF4
from herbal.models.crfs.crf5 import CRF5
from herbal.models.crfs.crf6 import CRF6
from herbal.models.crfs.crf7 import CRF7


class Command(BaseCommand):
    help = "Generate codebook per model"

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

        # ✅ Define base path
        base_path = os.path.expanduser("~/Documents/WORKS/NIMR/NIMREGENIN/Codebook")

        # ✅ Create folder if it doesn't exist
        os.makedirs(base_path, exist_ok=True)

        # ✅ Full file path
        file_path = os.path.join(base_path, "Nimregenin_Codebook_Version_2.0.xlsx")

        writer = pd.ExcelWriter(file_path, engine="openpyxl")

        for name, model in models.items():
            data = get_model_codebook(model)
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=name, index=False)

        writer.close()

        self.stdout.write(self.style.SUCCESS(f"✅ Codebook saved to {file_path}"))