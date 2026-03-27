# herbal/forms/crfs/crf1_nimregenin_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1Nimregenin


class CRF1NimregeninForm(forms.ModelForm):
    class Meta:
        model = CRF1Nimregenin
        fields = [
            "nimregenin_preparation",
            "nimregenin_start",
            "nimregenin_ongoing",
            "nimregenin_end",
            "nimregenin_dose",
            "nimregenin_frequency",
            "nimregenin_remarks",
        ]
        widgets = {
            "nimregenin_preparation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Preparation"
            }),
            "nimregenin_start": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "nimregenin_ongoing": forms.Select(attrs={
                "class": "form-select"
            }),
            "nimregenin_end": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "nimregenin_dose": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Dose"
            }),
            "nimregenin_frequency": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Frequency"
            }),
            "nimregenin_remarks": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Remarks"
            }),
        }

    # 🔥 Example validation
    def clean(self):
        cleaned_data = super().clean()
        ongoing = cleaned_data.get("nimregenin_ongoing")
        end = cleaned_data.get("nimregenin_end")

        # Rule: if not ongoing, must have an end date
        if ongoing in ["0", False, "False"] and not end:
            self.add_error("nimregenin_end", "Provide end date if not ongoing")

        return cleaned_data


CRF1NimregeninFormSet = inlineformset_factory(
    CRF1,
    CRF1Nimregenin,
    form=CRF1NimregeninForm,   # 🔥 use the custom form
    extra=0,
    can_delete=True
)
