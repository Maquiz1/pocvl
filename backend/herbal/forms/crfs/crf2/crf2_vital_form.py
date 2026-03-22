from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2


class CRF2VitalsForm(forms.ModelForm):
    class Meta:
        model = CRF2
        fields = [
            "test_date",
            "height",
            "weight",
            "bmi",
            "temperature",
            "respiratory_rate",
            "heart_rate",
            "systolic",
            "diastolic",
        ]

        widgets = {
            "test_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            "height": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "bmi": forms.NumberInput(attrs={"class": "form-control", "readonly": "readonly"}),

            "temperature": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),

            "respiratory_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "heart_rate": forms.NumberInput(attrs={"class": "form-control"}),

            "systolic": forms.NumberInput(attrs={"class": "form-control"}),
            "diastolic": forms.NumberInput(attrs={"class": "form-control"}),
        }