# herbal/forms/crfs/crf1_other_herbal_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1OtherHerbal


class CRF1OtherHerbalForm(forms.ModelForm):
    class Meta:
        model = CRF1OtherHerbal
        fields = [
            "herbal_preparation",
            "herbal_start",
            "herbal_ongoing",
            "herbal_end",
            "herbal_dose",
            "herbal_frequency",
            "herbal_remarks",
        ]
        widgets = {
            "herbal_preparation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Preparation"
            }),
            "herbal_start": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "herbal_ongoing": forms.Select(attrs={
                "class": "form-select"
            }),
            "herbal_end": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "herbal_dose": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Dose"
            }),
            "herbal_frequency": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Frequency"
            }),
            "herbal_remarks": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Remarks"
            }),
        }

    # 🔥 VALIDATION
    def clean(self):
        cleaned_data = super().clean()

        ongoing = cleaned_data.get("herbal_ongoing")
        end = cleaned_data.get("herbal_end")

        # Example rule:
        if ongoing in ["0", False, "False"] and not end:
            self.add_error("herbal_end", "Provide end date if not ongoing")

        return cleaned_data
    
    
CRF1OtherHerbalFormSet = inlineformset_factory(
    CRF1,
    CRF1OtherHerbal,
    form=CRF1OtherHerbalForm,   # 🔥 IMPORTANT
    extra=0,
    can_delete=True
)