# herbal/forms/enrollment_form.py

from django import forms
from herbal.models import Enrollment


class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = Enrollment

        fields = [
            "enrollment_date",
            "pt_category",
            "pt_type",
            "treatment_type",
            "treatment_date",
            "treatment_other",
            "previous_treatment",
            "previous_date",
            "previous_other",
            "total_cycle",
            "cycle_number",
            "remarks",
        ]

        labels = {
            "treatment_type": "New Treatment type",
            "treatment_date": "Date Started New Treatment type",
            "treatment_other": "Specify Other Treatment",
            "previous_treatment": "Previous(Past) Treatment type",
            "previous_date": "Date Started Previous(Past) Treatment",
            "previous_other": "Specify Other Previous(Past) Treatment",
        }

        widgets = {
            "enrollment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "pt_category": forms.Select(attrs={"class": "form-select"}),
            "pt_type": forms.Select(attrs={"class": "form-select"}),
            "treatment_type": forms.Select(attrs={"class": "form-select"}),
            "treatment_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "treatment_other": forms.TextInput(attrs={"class": "form-control"}),
            "previous_treatment": forms.Select(attrs={"class": "form-select"}),
            "previous_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "previous_other": forms.TextInput(attrs={"class": "form-control"}),
            "total_cycle": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "cycle_number": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    # =========================
    # ✅ CLEAN VALIDATION
    # =========================
    def clean(self):
        cleaned_data = super().clean()

        pt_type = cleaned_data.get("pt_type")

        # NEW treatment
        treatment_type = cleaned_data.get("treatment_type")
        treatment_date = cleaned_data.get("treatment_date")
        treatment_other = cleaned_data.get("treatment_other")

        # PREVIOUS treatment
        previous_treatment = cleaned_data.get("previous_treatment")
        previous_date = cleaned_data.get("previous_date")
        previous_other = cleaned_data.get("previous_other")

        # Cycles
        total_cycle = cleaned_data.get("total_cycle")
        cycle_number = cleaned_data.get("cycle_number")

        if not pt_type:
            return cleaned_data

        VALID_TYPES = [1, 2, 3, 4, 5, 6]
        OTHER = 6

        # =========================
        # ✅ NEW PATIENT (pt_type = 1)
        # =========================
        if pt_type.id == 1:

            # Require treatment type
            if not treatment_type:
                self.add_error("treatment_type", "Treatment type is required.")

            # If type in 1–6 → require date
            if treatment_type and treatment_type.id in VALID_TYPES:
                if not treatment_date:
                    self.add_error("treatment_date", "Treatment date is required.")

            # If OTHER → require text
            if treatment_type and treatment_type.id == OTHER:
                if not treatment_other:
                    self.add_error("treatment_other", "Please specify other treatment.")

            # Disallow previous fields
            if previous_treatment:
                self.add_error("previous_treatment", "Not allowed for new patients.")

            if previous_date:
                self.add_error("previous_date", "Not allowed for new patients.")

            if previous_other:
                self.add_error("previous_other", "Not allowed for new patients.")

        # =========================
        # ✅ PREVIOUS PATIENT (pt_type = 2)
        # =========================
        elif pt_type.id == 2:

            # Require previous treatment
            if not previous_treatment:
                self.add_error("previous_treatment", "Previous treatment is required.")

            # If type in 1–6 → require date
            if previous_treatment and previous_treatment.id in VALID_TYPES:
                if not previous_date:
                    self.add_error("previous_date", "Previous date is required.")

            # If OTHER → require text
            if previous_treatment and previous_treatment.id == OTHER:
                if not previous_other:
                    self.add_error("previous_other", "Please specify other treatment.")

            # Disallow new treatment fields
            if treatment_type:
                self.add_error(
                    "treatment_type", "Not allowed for previously treated patients."
                )

            if treatment_date:
                self.add_error(
                    "treatment_date", "Not allowed for previously treated patients."
                )

            if treatment_other:
                self.add_error(
                    "treatment_other", "Not allowed for previously treated patients."
                )

        # =========================
        # ✅ Cycle validation
        # =========================
        if total_cycle and cycle_number:
            if cycle_number > total_cycle:
                self.add_error(
                    "cycle_number", "Cycle number cannot exceed total cycles."
                )

        return cleaned_data
