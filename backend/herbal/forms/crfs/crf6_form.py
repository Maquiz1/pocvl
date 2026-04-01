from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6   # adjust path if needed


class CRF6Form(forms.ModelForm):

    class Meta:
        model = CRF6

        fields = [
            "today_date",
            "termination_date",
            "reason",
            "reason_date",          # ← was missing
            "reason_other",
            "primary_cause",        # ← was missing
            "secondary_cause",      # ← was missing
            "withdrew_reason",
            "withdrew_other",
            "outcome",
            "outcome_date",
            "outcome_other",
            "summary",
            "clinician_name",
            "remarks",
        ]

        labels = {
            "today_date": "1.a Today's date",
            "termination_date": "1.b Date patient terminated the study",
            "reason": "2. Reason for study termination",
            "reason_date": "2.a Date of termination reason",
            "reason_other": "2.c Other reason (specify)",
            "primary_cause": "3. Primary cause of death (if applicable)",
            "secondary_cause": "3.a Secondary cause of death (if applicable)",
            "withdrew_reason": "2.b Reason for withdrawal",
            "withdrew_other": "2.b.i Other withdrawal reason",
            "outcome": "4. Outcome",
            "outcome_date": "5. Outcome date",
            "outcome_other": "5.a Other outcome (specify)",
            "summary": "6. Provide/summarise the adverse event or termination summary",
            "remarks": "6.a Remarks",
            "clinician_name": "7. Responsible Clinician Name",
        }

        widgets = {
            "today_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "termination_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "reason_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "outcome_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            
            "reason": forms.Select(attrs={"class": "form-control"}),
            "withdrew_reason": forms.Select(attrs={"class": "form-control"}),
            "outcome": forms.Select(attrs={"class": "form-control"}),
            "clinician_name": forms.Select(attrs={"class": "form-control"}),
            
            "summary": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            
            # Optional: better UX for text fields
            "reason_other": forms.TextInput(attrs={"class": "form-control"}),
            "withdrew_other": forms.TextInput(attrs={"class": "form-control"}),
            "outcome_other": forms.TextInput(attrs={"class": "form-control"}),
            "primary_cause": forms.TextInput(attrs={"class": "form-control"}),
            "secondary_cause": forms.TextInput(attrs={"class": "form-control"}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        
        termination_date = cleaned_data.get("termination_date")
        today_date = cleaned_data.get("today_date")
        reason = cleaned_data.get("reason")
        withdrew_reason = cleaned_data.get("withdrew_reason")
        outcome = cleaned_data.get("outcome")
        reason_other = cleaned_data.get("reason_other")
        withdrew_other = cleaned_data.get("withdrew_other")
        outcome_other = cleaned_data.get("outcome_other")

        # Example 1: Date logic
        if termination_date and today_date and termination_date > today_date:
            self.add_error("termination_date", "Termination date cannot be in the future.")

        # Example 2: Conditional required fields
        if reason and reason.name == "Withdrew" and not withdrew_reason:   # adjust according to your TerminationReason choices
            self.add_error("withdrew_reason", "This field is required when reason is Withdrawal.")

        if reason and "Other" in str(reason) and not reason_other:
            self.add_error("reason_other", "Please specify the other reason.")

        # Add similar checks for death/primary_cause, outcome_other, etc.

        return cleaned_data