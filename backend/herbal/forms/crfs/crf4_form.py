from django import forms
from herbal.models.crfs.crf4.crf4_model import CRF4


class CRF4Form(forms.ModelForm):

    class Meta:

        model = CRF4

        fields = [
            "medication_given",
            "dosage",
            "adherence",
            "comments",
        ]

        widgets = {
            "medication_given": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "dosage": forms.TextInput(attrs={"class": "form-control"}),
            "adherence": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
