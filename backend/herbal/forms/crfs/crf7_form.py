from django import forms
from herbal.models.crfs.crf7.crf7_model import CRF7


class CRF7Form(forms.ModelForm):

    class Meta:

        model = CRF7

        fields = [
            "investigator_notes",
            "follow_up_needed",
        ]

        widgets = {
            "investigator_notes": forms.Textarea(attrs={"class": "form-control"}),
            "follow_up_needed": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
