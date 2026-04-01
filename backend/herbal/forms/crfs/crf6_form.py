from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6


class CRF6Form(forms.ModelForm):

    class Meta:

        model = CRF6

        fields = [
            "termination_date",
            "reason",
            "summary",
            "remarks",
            "clinician_name",
        ]

        widgets = {
            "termination_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "reason": forms.Select(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control","rows":3}),
            "remarks": forms.Textarea(attrs={"class": "form-control","rows":3}),
            "clinician_name": forms.Textarea(attrs={"class": "form-control","rows":3}),
        }
