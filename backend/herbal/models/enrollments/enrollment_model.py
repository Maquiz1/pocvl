# herbal/models/enrollments/enrollment_model.py

from django.db import models
from django.core.exceptions import ValidationError
from ..screening.screening_model import Screening
from core.models import BaseModel
from choices.models import PatientType,PatientCategory,TreatmentType
from django.core.exceptions import ValidationError

class Enrollment(BaseModel):

    screening = models.OneToOneField(
        Screening,
        on_delete=models.CASCADE,
        related_name="enrollment"
    )

    enrollment_date = models.DateField()

    pt_category = models.ForeignKey(
        PatientCategory,
        on_delete=models.PROTECT,
        related_name="subject_categories"
    )

    pt_type = models.ForeignKey(
        PatientType,
        on_delete=models.PROTECT,
        related_name="subject_types"
    )

    # =========================
    # ✅ New TREATMENT TYPE
    # =========================
    treatment_type = models.ForeignKey(
        TreatmentType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="subject_treatments"
    )

    treatment_date = models.DateField(
        null=True,
        blank=True
    )
    
    treatment_other = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
        
    # =========================
    # ✅ PREVIOUS TREATMENT TYPE
    # =========================
    previous_treatment = models.ForeignKey(
        TreatmentType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="subject_previous_treatment"
    )
        
    previous_date = models.DateField(
        null=True,
        blank=True
    )
    
    previous_other = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================
    # ✅ CYCLES
    # =========================
    total_cycle = models.PositiveIntegerField(
        help_text="Total planned treatment cycles"
    )

    cycle_number = models.PositiveIntegerField(
        help_text="Current cycle number"
    )

    # =========================
    # ✅ STATUS
    # =========================
    STATUS_CHOICES = [
        ("active", "Active"),
        ("completed", "Completed"),
        ("terminated", "Terminated"),
        ("lost", "Lost To Follow Up"),
        ("transfer", "Transferred Out"),
    ]

    remarks = models.TextField(
        blank=True
    )

    # =========================
    # ✅ VALIDATION
    # =========================
    def clean(self):

        VALID_TYPES = [1, 2, 3, 4, 5, 6]
        OTHER = 6

        # =========================
        # ✅ Ensure pt_type exists
        # =========================
        if not self.pt_type:
            return

        # =========================
        # ✅ NEW PATIENT (pt_type = 1)
        # =========================
        if self.pt_type.id == 1:

            # Require treatment_type
            if not self.treatment_type:
                raise ValidationError({
                    "treatment_type": "Treatment type is required."
                })

            # Require date if type in 1–6
            if self.treatment_type and self.treatment_type.id in VALID_TYPES:
                if not self.treatment_date:
                    raise ValidationError({
                        "treatment_date": "Treatment date is required."
                    })

            # Require OTHER text
            if self.treatment_type and self.treatment_type.id == OTHER:
                if not self.treatment_other:
                    raise ValidationError({
                        "treatment_other": "Please specify other treatment."
                    })

            # Disallow previous fields
            if self.previous_treatment:
                raise ValidationError({
                    "previous_treatment": "Not allowed for new patients."
                })

            if self.previous_date:
                raise ValidationError({
                    "previous_date": "Not allowed for new patients."
                })

            if self.previous_other:
                raise ValidationError({
                    "previous_other": "Not allowed for new patients."
                })

        # =========================
        # ✅ PREVIOUS PATIENT (pt_type = 2)
        # =========================
        elif self.pt_type.id == 2:

            # Require previous treatment
            if not self.previous_treatment:
                raise ValidationError({
                    "previous_treatment": "Previous treatment is required."
                })

            # Require date if type in 1–6
            if self.previous_treatment and self.previous_treatment.id in VALID_TYPES:
                if not self.previous_date:
                    raise ValidationError({
                        "previous_date": "Previous date is required."
                    })

            # Require OTHER text
            if self.previous_treatment and self.previous_treatment.id == OTHER:
                if not self.previous_other:
                    raise ValidationError({
                        "previous_other": "Please specify other treatment."
                    })

            # Disallow new treatment fields
            if self.treatment_type:
                raise ValidationError({
                    "treatment_type": "Not allowed for previously treated patients."
                })

            if self.treatment_date:
                raise ValidationError({
                    "treatment_date": "Not allowed for previously treated patients."
                })

            if self.treatment_other:
                raise ValidationError({
                    "treatment_other": "Not allowed for previously treated patients."
                })

        # =========================
        # ✅ Cycle logic
        # =========================
        if self.total_cycle and self.cycle_number:
            if self.cycle_number > self.total_cycle:
                raise ValidationError({
                    "cycle_number": "Cycle number cannot exceed total cycles."
                })

    def __str__(self):
        return f"Enrollment - {self.screening}"