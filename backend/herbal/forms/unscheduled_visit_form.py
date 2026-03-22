from django import forms
from herbal.models.visits.unschedule_visit_model import UnscheduledVisit
from herbal.models.visits.visit_schedule_model import VisitSchedule


class UnscheduledVisitForm(forms.ModelForm):

    class Meta:
        model = UnscheduledVisit
        fields = [
            "visit_date",
            "after_visit",
            "reason",
            "notes",
        ]

        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "after_visit": forms.Select(attrs={"class": "form-control"}),
            "reason": forms.Select(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        enrollment = kwargs.pop("enrollment", None)
        super().__init__(*args, **kwargs)

        # 🔥 filter only visits of this enrollment
        if enrollment:
            self.fields["after_visit"].queryset = VisitSchedule.objects.filter(
                enrollment=enrollment
            ).order_by("scheduled_date")