from django import forms
from herbal.models.crfs.crf3.crf3_model import CRF3

class CRF3Form(forms.ModelForm):

    class Meta:

        model = CRF3

        fields = [
            "symptoms",
            "severity",
            "notes",
        ]

        widgets = {

            "symptoms": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "severity": forms.Select(
                attrs={"class": "form-control"}
            ),

            "notes": forms.Textarea(
                attrs={"class": "form-control"}
            ),
        }