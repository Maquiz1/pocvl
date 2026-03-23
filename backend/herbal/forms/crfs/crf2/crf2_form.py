from django import forms
from herbal.models import CRF2


class CRF2Form(forms.ModelForm):

    class Meta:
        model = CRF2
        exclude = ["visit"]   # 🔥 important (set in view)

        widgets = {
            # Dates & Times
            "test_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "date_completed": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "vital_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "phys_exm_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),

            # Numbers
            "height": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "bmi": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),

            "temperature": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "respiratory_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "heart_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "systolic": forms.NumberInput(attrs={"class": "form-control"}),
            "diastolic": forms.NumberInput(attrs={"class": "form-control"}),

            # Textareas
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "additional_notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

            "appearance_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "heent_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "respiratory_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "cardiovascular_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "abdominal_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "urogenital_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "musculoskeletal_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "neurological_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "psychological_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "endocrine_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "lymphatic_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "skin_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "local_examination_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "physical_other_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
        }

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔥 Apply Bootstrap to ALL fields automatically
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "form-control")

        # 🔥 Optional: filter staff by site
        if site and "physcl_pfmd_by" in self.fields:
            self.fields["physcl_pfmd_by"].queryset = \
                self.fields["physcl_pfmd_by"].queryset.filter(site=site)