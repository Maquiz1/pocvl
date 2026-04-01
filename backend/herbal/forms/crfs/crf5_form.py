from django import forms
from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.models.visits.visit_schedule_model import VisitSchedule


class CRF5Form(forms.ModelForm):

    class Meta:
        model = CRF5

        fields = [
            "date_reported",
            "after_visit",
            "ae_description",
            "ae_category",
            "ae_start_date",
            "ae_ongoing",
            "ae_end_date",
            "ae_outcome",
            "ae_severity",
            "ae_serious",
            "ae_expected",
            "ae_treatment",
            "ae_action_taken",
            "ae_relationship",
            "ae_staff",
            "remarks",
        ]
        
        labels={
            "ae_staff": "Staff",
            "ae_description": "Adverse Event Description",
            "ae_category": "Adverse Event Category",
            "ae_start_date": "Start date",
            "ae_ongoing": "Ongoing ?",
            "ae_end_date": "End date",
            "ae_outcome": "Outcome",
            "ae_severity": "Severity",
            "ae_serious": "Serious",
            "ae_expected": "Expected",
            "ae_treatment": "Treatment",
            "ae_action_taken": "Action Taken",
            "ae_relationship": "Relationship to study teatment",
        }

        widgets = {
            "date_reported": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "after_visit": forms.Select(attrs={"class": "form-control"}),
            "ae_staff": forms.Select(attrs={"class": "form-control"}),

            "ae_description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

            "ae_category": forms.Select(attrs={"class": "form-control"}),
            "ae_severity": forms.Select(attrs={"class": "form-control"}),
            "ae_serious": forms.Select(attrs={"class": "form-control"}),
            "ae_expected": forms.Select(attrs={"class": "form-control"}),
            "ae_relationship": forms.Select(attrs={"class": "form-control"}),
            "ae_treatment": forms.Select(attrs={"class": "form-control"}),
            "ae_action_taken": forms.Select(attrs={"class": "form-control"}),
            "ae_outcome": forms.Select(attrs={"class": "form-control"}),

            "ae_start_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "ae_end_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "ae_ongoing": forms.Select(attrs={"class": "form-control"}),

            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    # =============================
    # INIT
    # =============================
    def __init__(self, *args, **kwargs):
        enrollment = kwargs.pop("enrollment", None)
        super().__init__(*args, **kwargs)

        self.fields["date_reported"].required = True
        self.fields["ae_description"].required = True
        self.fields["after_visit"].required = True
        self.fields["ae_category"].required = True
        self.fields["ae_severity"].required = True
        self.fields["ae_serious"].required = True
        self.fields["ae_expected"].required = True
        self.fields["ae_relationship"].required = True
        self.fields["ae_treatment"].required = True
        self.fields["ae_action_taken"].required = True
        self.fields["ae_outcome"].required = True
        self.fields["ae_start_date"].required = True
        self.fields["ae_ongoing"].required = True

        # Filter visits
        if enrollment:
            self.fields["after_visit"].queryset = VisitSchedule.objects.filter(
                enrollment=enrollment
            ).order_by("scheduled_date")
        else:
            self.fields["after_visit"].queryset = VisitSchedule.objects.none()

    # =============================
    # FIELD VALIDATION
    # =============================

    def clean_date_reported(self):
        value = self.cleaned_data.get("date_reported")
        if not value:
            raise forms.ValidationError("Date reported is required.")
        return value

    def clean_ae_description(self):
        value = self.cleaned_data.get("ae_description")
        if not value or len(value.strip()) < 5:
            raise forms.ValidationError("Provide a meaningful description (min 5 characters).")
        return value

    def clean_ae_start_date(self):
        value = self.cleaned_data.get("ae_start_date")
        if not value:
            raise forms.ValidationError("Start date is required.")
        return value

    def clean_ae_ongoing(self):
        value = self.cleaned_data.get("ae_ongoing")
        if not value:
            raise forms.ValidationError("Please specify if AE is ongoing.")
        return value

    def clean_ae_severity(self):
        if not self.cleaned_data.get("ae_severity"):
            raise forms.ValidationError("Please select AE severity.")
        return self.cleaned_data.get("ae_severity")

    def clean_ae_action_taken(self):
        if not self.cleaned_data.get("ae_action_taken"):
            raise forms.ValidationError("Please select action taken.")
        return self.cleaned_data.get("ae_action_taken")

    def clean_ae_outcome(self):
        if not self.cleaned_data.get("ae_outcome"):
            raise forms.ValidationError("Please select AE outcome.")
        return self.cleaned_data.get("ae_outcome")

    def clean_ae_staff(self):
        if not self.cleaned_data.get("ae_staff"):
            raise forms.ValidationError("Please select reporting staff.")
        return self.cleaned_data.get("ae_staff")

    # =============================
    # CROSS FIELD VALIDATION
    # =============================
    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("ae_start_date")
        end = cleaned_data.get("ae_end_date")
        ongoing = cleaned_data.get("ae_ongoing")
        reported = cleaned_data.get("date_reported")

        # Ongoing logic
        if ongoing and hasattr(ongoing, "value"):
            if ongoing.value == 1:  # YES
                cleaned_data["ae_end_date"] = None
            else:
                if not end:
                    self.add_error("ae_end_date", "End date required if not ongoing.")

        # Date logic
        if start and end and end < start:
            self.add_error("ae_end_date", "End date cannot be before start date.")

        return cleaned_data