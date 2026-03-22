# herbal/forms/visit_start_form.py

from django import forms
from herbal.models import VisitSchedule


class VisitStartForm(forms.ModelForm):

    class Meta:
        model = VisitSchedule
        fields = ["actual_visit_date"]
        widgets = {
            "actual_visit_date": forms.DateInput(attrs={"type": "date"})
        }