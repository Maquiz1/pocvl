from django import forms
from herbal.models.crfs.crf5.crf5_model import CRF5
from herbal.models.visits.visit_schedule_model import VisitSchedule

class CRF5Form(forms.ModelForm):

    class Meta:

        model = CRF5

        fields = [
            "event_date",
            "after_visit",
            "event_description",
            "severity",
            "action_taken",
            "outcome",
        ]

        widgets = {
            "event_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "after_visit": forms.Select(attrs={"class": "form-control"}),
            "event_description": forms.Textarea(attrs={"class": "form-control"}),
            "severity": forms.Select(attrs={"class": "form-control"}),
            "action_taken": forms.Textarea(attrs={"class": "form-control"}),
            "outcome": forms.Textarea(attrs={"class": "form-control"}),
        }
        
    def __init__(self, *args, **kwargs):
        enrollment = kwargs.pop("enrollment", None)
        super().__init__(*args, **kwargs)

        if enrollment:
            self.fields["after_visit"].queryset = VisitSchedule.objects.filter(
                enrollment=enrollment
            ).order_by("scheduled_date")
