# herbal/forms/crfs/crf1_chemotherapy_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1Chemotherapy


class CRF1ChemotherapyForm(forms.ModelForm):
    class Meta:
        model = CRF1Chemotherapy
        fields = [
            "chemotherapy",
            "chemotherapy_start",
            "chemotherapy_ongoing",
            "chemotherapy_end",
            "chemotherapy_dose",
            "chemotherapy_frequency",
            "chemotherapy_remarks",
        ]
        widgets = {
            "chemotherapy": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Type"
            }),
            "chemotherapy_start": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "chemotherapy_ongoing": forms.Select(attrs={
                "class": "form-select"
            }),
            "chemotherapy_end": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "chemotherapy_dose": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Dose"
            }),
            "chemotherapy_frequency": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Frequency"
            }),
            "chemotherapy_remarks": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Remarks"
            }),
        }

    # 🔥 Example validation
    def clean(self):
        cleaned_data = super().clean()
        ongoing = cleaned_data.get("chemotherapy_ongoing")
        end = cleaned_data.get("chemotherapy_end")

        # Rule: if not ongoing, must have an end date
        if ongoing in ["0", False, "False"] and not end:
            self.add_error("chemotherapy_end", "Provide end date if not ongoing")

        return cleaned_data


CRF1ChemotherapyFormSet = inlineformset_factory(
    CRF1,
    CRF1Chemotherapy,
    form=CRF1ChemotherapyForm,   # 🔥 use the custom form
    extra=0,
    can_delete=True
)
