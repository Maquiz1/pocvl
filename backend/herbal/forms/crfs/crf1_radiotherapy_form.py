# herbal/forms/crfs/crf1_radiotherapy_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1Radiotherapy


class CRF1RadiotherapyForm(forms.ModelForm):
    class Meta:
        model = CRF1Radiotherapy
        fields = [
            "radiotherapy",
            "radiotherapy_start",
            "radiotherapy_ongoing",
            "radiotherapy_end",
            "radiotherapy_dose",
            "radiotherapy_frequency",
            "radiotherapy_remarks",
        ]
        widgets = {
            "radiotherapy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Type"
            }),
            "radiotherapy_start": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "radiotherapy_ongoing": forms.Select(attrs={
                "class": "form-select"
            }),
            "radiotherapy_end": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "radiotherapy_dose": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Dose"
            }),
            "radiotherapy_frequency": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Frequency"
            }),
            "radiotherapy_remarks": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Remarks"
            }),
        }

    # 🔥 Example validation
    def clean(self):
        cleaned_data = super().clean()
        ongoing = cleaned_data.get("radiotherapy_ongoing")
        end = cleaned_data.get("radiotherapy_end")

        # Rule: if not ongoing, must have an end date
        if ongoing in ["0", False, "False"] and not end:
            self.add_error("radiotherapy_end", "Provide end date if not ongoing")

        return cleaned_data


CRF1RadiotherapyFormSet = inlineformset_factory(
    CRF1,
    CRF1Radiotherapy,
    form=CRF1RadiotherapyForm,   # 🔥 use the custom form
    extra=0,
    can_delete=True
)
