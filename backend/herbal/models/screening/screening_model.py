from django.db import models
from ..subjects.subject_model import Subject
from core.models import BaseModel
from choices.models import YesNo, YesNoUnk,NotEnrolledReason
from herbal.models.cancers.cancer_type_model import CancerType
from django.core.exceptions import ValidationError


class Screening(BaseModel):

    subject = models.OneToOneField(
        Subject,
        on_delete=models.CASCADE,
        related_name="screening"
    )

    screening_date = models.DateField()

    # =========================
    # CONSENT
    # =========================
    consent = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    consent_date = models.DateField(null=True, blank=True)

    consent_nimregenin = models.ForeignKey(YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    nimregenin_date = models.DateField(null=True, blank=True)

    consent_reasons = models.TextField(blank=True, null=True)
    nimregenin_reasons = models.TextField(blank=True, null=True)

    # =========================
    # INCLUSION
    # =========================
    age_18 = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    biopsy = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")

    breast_cancer = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    brain_cancer = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")

    cervical_cancer = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    prostate_cancer = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")

    cancer_types = models.ManyToManyField(
        CancerType,
        blank=True,
        related_name="screening_cancer"
    )

    # =========================
    # EXCLUSION
    # =========================
    pregnant = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    breast_feeding = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")

    ckd = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")
    liver_disease = models.ForeignKey(YesNo, on_delete=models.SET_NULL, null=True, blank=True,related_name="+")

    enrolled = models.ForeignKey(YesNoUnk, on_delete=models.SET_NULL, null=True, blank=True)

    reason = models.ForeignKey(
        NotEnrolledReason,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    reason_other = models.TextField(blank=True)
    
    # =========================
    remarks = models.TextField(blank=True, null=True)

    inclusion_criteria_met = models.BooleanField(default=False)
    exclusion_criteria_present = models.BooleanField(default=False)
    eligible = models.BooleanField(default=False)

    # =========================
    # HELPERS ✅ (VERY IMPORTANT)
    # =========================
    def is_yes(self, field):
        return field and field.value == 1

    # =========================
    # SAVE LOGIC
    # =========================
    def save(self, *args, **kwargs):

        subject = getattr(self, "subject", None)

        if not subject:
            super().save(*args, **kwargs)
            return

        sex = subject.sex_id

        # FORCE NULLS
        if sex == 1:
            self.cervical_cancer = None
            self.pregnant = None
            self.breast_feeding = None
        elif sex == 2:
            self.prostate_cancer = None

        # BASIC INCLUSION
        basic_inclusion = (
            self.is_yes(self.consent) and
            self.is_yes(self.age_18) and
            self.is_yes(self.biopsy)
        )

        # CANCER LOGIC
        common = [self.breast_cancer, self.brain_cancer]

        specific = []
        if sex == 1:
            specific = [self.prostate_cancer]
        elif sex == 2:
            specific = [self.cervical_cancer]

        cancer_fields = [f for f in (common + specific) if f]
        has_cancer = any(self.is_yes(f) for f in cancer_fields)

        self.inclusion_criteria_met = basic_inclusion and has_cancer

        # EXCLUSIONS
        exclusions = [self.ckd, self.liver_disease]

        if sex == 2:
            exclusions += [self.pregnant, self.breast_feeding]

        exclusions = [f for f in exclusions if f]

        self.exclusion_criteria_present = any(
            self.is_yes(f) for f in exclusions
        )

        # FINAL
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

        # =========================
        # SEX VS CANCER VALIDATION
        # =========================
        if sex_id == 1 and cancers.filter(code="CC").exists():
            raise ValidationError("Male cannot have Cervical Cancer")

        if sex_id == 2 and cancers.filter(code="PC").exists():
            raise ValidationError("Female cannot have Prostate Cancer")

        # =========================
        # ENROLLMENT LOGIC 🔥
        # =========================
        enrolled = self.enrolled
        reason = self.reason
        reason_other = self.reason_other

        # 1. Eligible → enrolled MUST be answered
        if self.eligible and not enrolled:
            raise ValidationError({
                "enrolled": "Enrollment status is required if participant is eligible."
            })

        if enrolled:

            # helper inline (since model has only is_yes)
            is_yes = enrolled.value == 1
            is_no = enrolled.value == 2

            # 2. NOT enrolled → reason required
            if is_no and not reason:
                raise ValidationError({
                    "reason": "Reason is required if participant is not enrolled."
                })

            # 3. Enrolled → reason must be empty
            if is_yes and reason:
                raise ValidationError({
                    "reason": "Reason must be empty if participant is enrolled."
                })

        # =========================
        # REASON / OTHER 🔥
        # =========================
        if reason:

            # FK safe → use code
            reason_code = getattr(reason, "code", None)

            # 4. OTHER (96) → reason_other required
            if str(reason_code) == "96" and not reason_other:
                raise ValidationError({
                    "reason_other": "Please specify the 'Other' reason."
                })

            # 5. NOT OTHER → must be empty
            if str(reason_code) != "96" and reason_other:
                raise ValidationError({
                    "reason_other": "Only fill this field when 'Other (96)' is selected."
                })

        # # =========================
        # # AUTO CLEAN (OPTIONAL 🔥)
        # # =========================
        # if enrolled and enrolled.value == 1:
        #     self.reason = None
        #     self.reason_other = ""

    def __str__(self):
        return f"Screening - {self.subject}"