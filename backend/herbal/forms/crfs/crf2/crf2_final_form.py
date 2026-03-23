from django import forms
from herbal.models.crfs.crf2.crf2_model import CRF2
from accounts.models import StaffProfile  # adjust import if needed


class CRF2FinalForm(forms.ModelForm):
    class Meta:
        model = CRF2
        fields = [
            "additional_notes",
            "physcl_pfmd_by",   # ✅ updated field
            "remarks",
        ]

        widgets = {
            "physcl_pfmd_by": forms.Select(attrs={"class": "form-control"}),

            "additional_notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        site = kwargs.pop("site", None)   # ✅ receive site
        super().__init__(*args, **kwargs)

        if site:
            self.fields["physcl_pfmd_by"].queryset = StaffProfile.objects.filter(
                site=site
            )