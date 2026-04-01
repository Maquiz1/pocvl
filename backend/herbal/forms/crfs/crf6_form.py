from django import forms
from herbal.models.crfs.crf6.crf6_model import CRF6


class CRF6Form(forms.ModelForm):

    class Meta:

        model = CRF6

        fields = [
            "today_date",
            "termination_date",
            "reason",
            "summary",
            "remarks",
            "clinician_name",
        ]
        
        labels={
            "today_date":"1.a Today's date",
            "termination_date":"1.b Date patient terminated the study",
            "reason":"4. Outcome",
            "summary":"6. Provide/summarise the adverse event",
            "remarks":"6.a Remarks",
            "clinician_name":"7. Responsible Clinician Name",
        }

        widgets = {
            "today_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "termination_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "reason": forms.Select(attrs={"class": "form-control"}),
            "summary": forms.Textarea(attrs={"class": "form-control","rows":3}),
            "remarks": forms.Textarea(attrs={"class": "form-control","rows":3}),
            "clinician_name": forms.Select(attrs={"class": "form-control"}),
        }
