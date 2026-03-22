# herbal/models/crfs/crf1_model.py

from django.db import models
from ...visits.visit_schedule_model import VisitSchedule
from core.models import BaseModel
from choices.models import YesNo, YesNoNa, YesNoUnk


class CRF1(BaseModel):

    visit = models.OneToOneField(
        VisitSchedule,
        on_delete=models.CASCADE,
        related_name="crf1"
    )

    # =========================
    # MEDICAL HISTORY
    # =========================

    diagnosis_date = models.DateField()

    # --- Diabetes ---
    diabetic = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_diabetic"
    )
    diabetic_medicatn = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_diabetic_med"
    )
    diabetic_medicatn_name = models.CharField(max_length=255, blank=True)

    # --- Hypertension ---
    hypertension = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_hypertension"
    )
    hypertension_medicatn = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_hypertension_med"
    )
    hypertension_medicatn_name = models.CharField(max_length=255, blank=True)

    # --- Heart Disease ---
    heart = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_heart"
    )
    heart_medicatn = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_heart_med"
    )
    heart_medicatn_name = models.CharField(max_length=255, blank=True)

    # --- Asthma ---
    asthma = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_asthma"
    )
    asthma_medicatn = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_asthma_med"
    )
    asthma_medicatn_name = models.CharField(max_length=255, blank=True)

    # --- HIV/AIDS ---
    hiv_aids = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_hiv"
    )
    hiv_aids_medicatn = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_hiv_med"
    )
    hiv_aids_medicatn_name = models.CharField(max_length=255, blank=True)

    # --- Other Medical Condition ---
    other_medical = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_other_medical"
    )
    
    # =========================
    # HERBAL 
    # =========================

    nimregenin_herbal = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_nimregenin"
    )
      
    # =========================
    # OTHER HERBAL
    # =========================
    
    other_herbal = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_other_herbal"
    )

    # =========================
    # PRIOR TREATMENTS
    # =========================

    radiotherapy_performed = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_radiotherapy"
    )
    chemotherapy_performed = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_chemotherapy"
    )
    surgery_performed = models.ForeignKey(
        YesNoUnk, on_delete=models.PROTECT,
        null=True, blank=True, related_name="crf1_surgery"
    )

    # =========================
    # REMARKS
    # =========================

    remarks = models.TextField(blank=True)


    def clean(self):
        from django.core.exceptions import ValidationError

        errors = {}

        def get_val(value):
            return getattr(value, "name", "").lower() if value else None

        def is_yes(value):
            return get_val(value) == "yes"

        def is_no(value):
            return get_val(value) == "no"

        def is_unknown(value):
            return get_val(value) == "unknown"

        # =========================
        # FIELD GROUPS
        # =========================

        groups = [
            ("diabetic", "diabetic_medicatn", "diabetic_medicatn_name", "Diabetes"),
            ("hypertension", "hypertension_medicatn", "hypertension_medicatn_name", "Hypertension"),
            ("heart", "heart_medicatn", "heart_medicatn_name", "Heart disease"),
            ("asthma", "asthma_medicatn", "asthma_medicatn_name", "Asthma"),
            ("hiv_aids", "hiv_aids_medicatn", "hiv_aids_medicatn_name", "HIV/AIDS"),
        ]

        for disease_field, med_field, name_field, label in groups:
            disease = getattr(self, disease_field)
            med = getattr(self, med_field)
            name = getattr(self, name_field)

            disease_val = get_val(disease)
            med_val = get_val(med)

            # -------------------------
            # 1. Disease = NO or UNKNOWN
            # -------------------------
            if is_no(disease) or is_unknown(disease):
                if med:
                    errors[med_field] = f"{label}: medication must be empty if condition is No or Unknown."

                if name:
                    errors[name_field] = f"{label}: medication name must be empty if condition is No or Unknown."

            # -------------------------
            # 2. Disease = YES
            # -------------------------
            if is_yes(disease):

                # Medication required
                if not med:
                    errors[med_field] = f"{label}: medication is required when condition = Yes."

                # Medication = YES → name required
                if is_yes(med) and not name:
                    errors[name_field] = f"{label}: medication name is required when medication = Yes."

                # Medication = NO or UNKNOWN → name must be empty
                if (is_no(med) or is_unknown(med)) and name:
                    errors[name_field] = f"{label}: medication name must be empty unless medication = Yes."

        # =========================
        # FINAL
        # =========================

        if errors:
            raise ValidationError(errors)
        
    def __str__(self):
        return f"CRF1 - Visit {self.visit_id}"