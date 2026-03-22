from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2

class CRF2Form(forms.ModelForm):

    class Meta:

        model = CRF2

        fields = [
            "lab_result",
            "test_date",
            "comments",
        ]

        widgets = {

            "lab_result": forms.NumberInput(
                attrs={"class": "form-control"}
            ),

            "test_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),

            "comments": forms.Textarea(
                attrs={"class": "form-control"}
            ),
        }