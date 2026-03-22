from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6


class CRF6Form(forms.ModelForm):

    class Meta:

        model = CRF6

        fields = [
            "termination_date",
            "reason",
            "comments",
        ]

        widgets = {
            "termination_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "reason": forms.Select(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
