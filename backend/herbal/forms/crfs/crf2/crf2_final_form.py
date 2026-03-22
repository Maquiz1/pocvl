from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2

class CRF2FinalForm(forms.ModelForm):
    class Meta:
        model = CRF2
        fields = [
            "additional_notes",
            "physical_performed",
            "remarks",
        ]

        widgets = {
            "physical_performed": forms.Select(attrs={"class": "form-control"}),

            "additional_notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }