from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2

class CRF2OtherExamForm(forms.ModelForm):
    class Meta:
        model = CRF2
        fields = [
            "physical_exams_other",
            "physical_other_specify",
            "physical_other_system",
            "physical_other_comments",
            "physical_other_signifcnt",
        ]

        widgets = {
            "physical_exams_other": forms.Select(attrs={"class": "form-control"}),
            "physical_other_system": forms.Select(attrs={"class": "form-control"}),
            "physical_other_signifcnt": forms.Select(attrs={"class": "form-control"}),

            "physical_other_specify": forms.TextInput(attrs={"class": "form-control"}),
            "physical_other_comments": forms.Textarea(attrs={"class": "form-control"}),
        }