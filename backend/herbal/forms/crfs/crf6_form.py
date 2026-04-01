from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6


class CRF6Form(forms.ModelForm):

    class Meta:
        model = CRF6

        fields = [
            "today_date",
            "termination_date",
            "reason",
            "reason_date",
            "reason_other",
            "primary_cause",
            "secondary_cause",
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
            "summary": "6. Termination summary",
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

            "reason_other": forms.TextInput(attrs={"class": "form-control"}),
            "withdrew_other": forms.TextInput(attrs={"class": "form-control"}),
            "outcome_other": forms.TextInput(attrs={"class": "form-control"}),
            "primary_cause": forms.TextInput(attrs={"class": "form-control"}),
            "secondary_cause": forms.TextInput(attrs={"class": "form-control"}),
        }

    # ✅ FORCE REQUIRED FIELDS (DQA CRITICAL)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["today_date"].required = True
        self.fields["termination_date"].required = True
        self.fields["reason"].required = True
        self.fields["clinician_name"].required = True
        self.fields["outcome"].required = True

    # ✅ CENTRALIZED DATA QUALITY VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        today_date = cleaned_data.get("today_date")
        termination_date = cleaned_data.get("termination_date")

        reason = cleaned_data.get("reason")
        reason_date = cleaned_data.get("reason_date")
        reason_other = cleaned_data.get("reason_other")

        withdrew_reason = cleaned_data.get("withdrew_reason")
        withdrew_other = cleaned_data.get("withdrew_other")

        outcome = cleaned_data.get("outcome")
        outcome_date = cleaned_data.get("outcome_date")
        outcome_other = cleaned_data.get("outcome_other")

        primary_cause = cleaned_data.get("primary_cause")

        # =========================
        # 1. DATE VALIDATION
        # =========================
        if termination_date and today_date:
            if termination_date > today_date:
                self.add_error("termination_date", "Termination date cannot be after today's date.")

        if reason_date and termination_date:
            if reason_date < termination_date:
                self.add_error("reason_date", "Reason date cannot be before termination date.")

        if outcome_date and termination_date:
            if outcome_date < termination_date:
                self.add_error("outcome_date", "Outcome date cannot be before termination date.")

        # =========================
        # 2. REASON VALIDATION (USING CODE ✅)
        # =========================
        if reason:
            code = (reason.code or "").upper()

            # WITHDRAW
            if code == "WITHDRAWN":
                if not withdrew_reason:
                    self.add_error("withdrew_reason", "Withdrawal reason is required.")

            # DEATH
            if code == "DEATH":
                if not primary_cause:
                    self.add_error("primary_cause", "Primary cause of death is required.")

            # OTHER
            if code == "OTHER":
                if not reason_other:
                    self.add_error("reason_other", "Please specify the other reason.")

        # =========================
        # 3. WITHDRAW OTHER
        # =========================
        if withdrew_reason:
            if (withdrew_reason.code or "").upper() == "OTHER" and not withdrew_other:
                self.add_error("withdrew_other", "Please specify other withdrawal reason.")

        # =========================
        # 4. OUTCOME VALIDATION
        # =========================
        # if outcome:
        #     if not outcome_date:
        #         self.add_error("outcome_date", "Outcome date is required.")

        #     if (outcome.code or "").upper() == "OTHER" and not outcome_other:
        #         self.add_error("outcome_other", "Please specify other outcome.")

        # =========================
        # 5. CONSISTENCY CHECK
        # =========================
        if not reason and (withdrew_reason or primary_cause):
            self.add_error("reason", "Termination reason must be selected.")

        return cleaned_data