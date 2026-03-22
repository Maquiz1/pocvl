# herbal/models/screening/screening_model.py

from django.db import models
from ..subjects.subject_model import Subject
from core.models import BaseModel
from choices.models import YesNo,YesNoNa,YesNoUnk
from herbal.models.cancers.cancer_type_model import CancerType
from django.core.exceptions import ValidationError

class YesNoChoices(models.IntegerChoices):
    YES = 1, "Yes"
    NO = 2, "No"
    
class YesNoNAChoices(models.IntegerChoices):
    YES = 1, "Yes"
    NO = 2, "No"
    NA = 3, "NA"


class YesNoUnknownChoices(models.IntegerChoices):
    YES = 1, "Yes"
    NO = 2, "No"
    UNK = 3, "UNK"

class Screening(BaseModel):

    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name="screening"
    )

    # Core
    screening_date = models.DateField()

    # Consent
    consent = models.IntegerField(choices=YesNoChoices.choices)
    consent_date = models.DateField(null=True, blank=True)

    consent_nimregenin = models.ForeignKey(YesNoUnk,on_delete=models.SET_NULL, null=True, blank=True)
    nimregenin_date = models.DateField(null=True, blank=True)

    consent_reasons = models.TextField(blank=True, null=True)
    nimregenin_reasons = models.TextField(blank=True, null=True)

    # Inclusion Criteria
    age_18 = models.IntegerField(choices=YesNoChoices.choices)

    biopsy = models.IntegerField(choices=YesNoChoices.choices)
    breast_cancer = models.IntegerField(choices=YesNoChoices.choices)
    brain_cancer = models.IntegerField(choices=YesNoChoices.choices)

    # Sex-specific cancers
    cervical_cancer = models.IntegerField(
        choices=YesNoChoices.choices, null=True, blank=True
    )
    prostate_cancer = models.IntegerField(
        choices=YesNoChoices.choices, null=True, blank=True
    )

    cancer_types = models.ManyToManyField(
        CancerType,
        blank=True,
        related_name="screening_cancer"
    )
    
    # Exclusion Criteria
    pregnant = models.IntegerField(
        choices=YesNoChoices.choices, null=True, blank=True
    )
    breast_feeding = models.IntegerField(
        choices=YesNoChoices.choices, null=True, blank=True
    )
    ckd = models.IntegerField(choices=YesNoChoices.choices)
    liver_disease = models.IntegerField(choices=YesNoChoices.choices)

    # Notes
    remarks = models.TextField(blank=True, null=True)

    inclusion_criteria_met = models.BooleanField(default=False)
    exclusion_criteria_present = models.BooleanField(default=False)
    eligible = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        # =========================
        # ✅ SAFE SUBJECT ACCESS
        # =========================
        subject = getattr(self, "subject", None)

        if not subject:
            # Save without crashing if subject not yet assigned
            super().save(*args, **kwargs)
            return

        sex = subject.sex_id

        # =========================
        # 🔥 FORCE NULL FOR NON-APPLICABLE
        # =========================
        if sex == 1:  # 👨 Male
            self.cervical_cancer = None
            self.pregnant = None
            self.breast_feeding = None

        elif sex == 2:  # 👩 Female
            self.prostate_cancer = None

        # =========================
        # ✅ BASIC INCLUSION
        # =========================
        basic_inclusion = (
            self.consent == YesNoChoices.YES and
            self.age_18 == YesNoChoices.YES and
            self.biopsy == YesNoChoices.YES
        )

        # =========================
        # ✅ CANCER LOGIC
        # =========================
        common_cancers = [
            self.breast_cancer,
            self.brain_cancer,
        ]

        if sex == 1:
            specific_cancers = [self.prostate_cancer]
        elif sex == 2:
            specific_cancers = [self.cervical_cancer]
        else:
            specific_cancers = []

        cancer_fields = [f for f in (common_cancers + specific_cancers) if f is not None]

        has_cancer = any(field == YesNoChoices.YES for field in cancer_fields)

        self.inclusion_criteria_met = basic_inclusion and has_cancer

        # =========================
        # ✅ EXCLUSIONS
        # =========================
        exclusion_fields = [
            self.ckd,
            self.liver_disease,
        ]

        if sex == 2:
            exclusion_fields.extend([
                self.pregnant,
                self.breast_feeding,
            ])

        exclusion_fields = [f for f in exclusion_fields if f is not None]

        self.exclusion_criteria_present = any(
            field == YesNoChoices.YES for field in exclusion_fields
        )

        # =========================
        # ✅ FINAL ELIGIBILITY
        # =========================
        self.eligible = (
            self.inclusion_criteria_met and not self.exclusion_criteria_present
        )

        super().save(*args, **kwargs)

    def clean(self):
        super().clean()

        subject = getattr(self, "subject", None)

        if not subject or not subject.sex:
            return

        sex_id = subject.sex.id

        cancers = self.cancer_types.all()

        if sex_id == 1 and cancers.filter(code="CC").exists():
            raise ValidationError("Male cannot have Cervical Cancer")

        if sex_id == 2 and cancers.filter(code="PC").exists():
            raise ValidationError("Female cannot have Prostate Cancer")
            
    def __str__(self):
        return f"Screening - {self.subject}"