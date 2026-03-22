from django import forms
from herbal.models import Screening
from django.core.exceptions import ValidationError


class ScreeningForm(forms.ModelForm):

    class Meta:
        model = Screening

        fields = [
            # Core
            "screening_date",

            # Consent
            "consent",
            "consent_date",
            "consent_reasons",

            "consent_nimregenin",
            "nimregenin_date",
            "nimregenin_reasons",

            # Inclusion
            "age_18",
            "biopsy",
            "breast_cancer",
            "brain_cancer",
            "cervical_cancer",
            "prostate_cancer",

            "cancer_types",
            
            # Exclusion
            "pregnant",
            "breast_feeding",
            "ckd",
            "liver_disease",

            # Notes
            "remarks",
        ]

        labels = {
            "age_18": "Aged eighteen years and above",
            "biopsy": "Confirmed cancer with biopsy?",
            "consent": "Did the participant consent to be part of the study?",
            "consent_nimregenin": "Did the participant consent to use NIMREGENIN preparation?",
        }

        widgets = {
            "screening_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "consent_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "nimregenin_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            "consent": forms.Select(attrs={"class": "form-select"}),
            "consent_nimregenin": forms.Select(attrs={"class": "form-select"}),
            "age_18": forms.Select(attrs={"class": "form-select"}),
            "biopsy": forms.Select(attrs={"class": "form-select"}),
            "breast_cancer": forms.Select(attrs={"class": "form-select"}),
            "brain_cancer": forms.Select(attrs={"class": "form-select"}),
            "cervical_cancer": forms.Select(attrs={"class": "form-select"}),
            "prostate_cancer": forms.Select(attrs={"class": "form-select"}),

            "cancer_types": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),

            "pregnant": forms.Select(attrs={"class": "form-select"}),
            "breast_feeding": forms.Select(attrs={"class": "form-select"}),
            "ckd": forms.Select(attrs={"class": "form-select"}),
            "liver_disease": forms.Select(attrs={"class": "form-select"}),

            "consent_reasons": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "nimregenin_reasons": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    # =========================
    # 🔥 HELPERS (FK SAFE)
    # =========================
    def is_yes(self, obj):
        return obj and obj.value == 1

    def is_no(self, obj):
        return obj and obj.value == 2

    # =========================
    # INIT (SEX LOGIC)
    # =========================
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        subject = getattr(self.instance, "subject", None)
        sex = subject.sex_id if subject else None

        required_fields = [
            "screening_date",
            "consent",
            "consent_nimregenin",
            "age_18",
            "biopsy",
            "breast_cancer",
            "brain_cancer",
            "ckd",
            "liver_disease",
        ]

        for field in required_fields:
            self.fields[field].required = True

        # Male
        if sex == 1:
            self.fields["prostate_cancer"].required = True
            self.fields["cervical_cancer"].required = False
            self.fields["pregnant"].required = False
            self.fields["breast_feeding"].required = False

        # Female
        elif sex == 2:
            self.fields["cervical_cancer"].required = True
            self.fields["pregnant"].required = True
            self.fields["breast_feeding"].required = True
            self.fields["prostate_cancer"].required = False

    # =========================
    # CLEAN (FULLY FIXED)
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        consent = cleaned_data.get("consent")
        consent_date = cleaned_data.get("consent_date")
        consent_reasons = cleaned_data.get("consent_reasons")

        nimr = cleaned_data.get("consent_nimregenin")
        nimr_date = cleaned_data.get("nimregenin_date")
        nimr_reasons = cleaned_data.get("nimregenin_reasons")

        breast = cleaned_data.get("breast_cancer")
        brain = cleaned_data.get("brain_cancer")
        cervical = cleaned_data.get("cervical_cancer")
        prostate = cleaned_data.get("prostate_cancer")

        cancers = cleaned_data.get("cancer_types")

        subject = getattr(self.instance, "subject", None)
        sex_id = subject.sex_id if subject else None

        # =========================
        # CONSENT
        # =========================
        if self.is_yes(consent) and not consent_date:
            self.add_error("consent_date", "Consent date is required if consent is Yes.")

        if self.is_no(consent) and not consent_reasons:
            self.add_error("consent_reasons", "Reason is required if consent is No.")

        # =========================
        # NIMREGENIN
        # =========================
        if nimr:
            if nimr.value == 1 and not nimr_date:
                self.add_error("nimregenin_date", "Date is required if YES.")

            elif nimr.value == 2 and not nimr_reasons:
                self.add_error("nimregenin_reasons", "Reason is required if NO.")

        # =========================
        # CANCER TYPES
        # =========================
        selected_codes = set(cancers.values_list("code", flat=True)) if cancers else set()

        # Sex validation
        if sex_id == 1 and "CC" in selected_codes:
            self.add_error("cancer_types", "Male cannot have Cervical Cancer")

        if sex_id == 2 and "PC" in selected_codes:
            self.add_error("cancer_types", "Female cannot have Prostate Cancer")

        # Match validation
        if self.is_yes(breast) and "BC" not in selected_codes:
            self.add_error("cancer_types", "Select Breast Cancer (BC)")

        if self.is_yes(brain) and "BR" not in selected_codes:
            self.add_error("cancer_types", "Select Brain Cancer (BR)")

        if self.is_yes(cervical) and "CC" not in selected_codes:
            self.add_error("cancer_types", "Select Cervical Cancer (CC)")

        if self.is_yes(prostate) and "PC" not in selected_codes:
            self.add_error("cancer_types", "Select Prostate Cancer (PC)")

        # Must not be selected
        if not self.is_yes(breast) and "BC" in selected_codes:
            self.add_error("cancer_types", "Uncheck Breast Cancer")

        if not self.is_yes(brain) and "BR" in selected_codes:
            self.add_error("cancer_types", "Uncheck Brain Cancer")

        if not self.is_yes(cervical) and "CC" in selected_codes:
            self.add_error("cancer_types", "Uncheck Cervical Cancer")

        if not self.is_yes(prostate) and "PC" in selected_codes:
            self.add_error("cancer_types", "Uncheck Prostate Cancer")

        # All NO → none selected
        if (
            not self.is_yes(breast) and
            not self.is_yes(brain) and
            not self.is_yes(cervical) and
            not self.is_yes(prostate)
        ):
            if selected_codes:
                self.add_error("cancer_types", "No cancers should be selected if all are No")

        # =========================
        # FINAL CLEANING
        # =========================
        if sex_id == 1:
            cleaned_data["cervical_cancer"] = None
            cleaned_data["pregnant"] = None
            cleaned_data["breast_feeding"] = None

        elif sex_id == 2:
            cleaned_data["prostate_cancer"] = None

        return cleaned_data