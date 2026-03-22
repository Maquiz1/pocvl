# herbal/forms/crfs/crf1_form.py

from django import forms
from herbal.models import CRF1

class CRF1Form(forms.ModelForm):

    class Meta:
        model = CRF1
        
        fields = [
            "diagnosis_date",

            "diabetic", "diabetic_medicatn", "diabetic_medicatn_name",
            "hypertension", "hypertension_medicatn", "hypertension_medicatn_name",
            "heart", "heart_medicatn", "heart_medicatn_name",
            "asthma", "asthma_medicatn", "asthma_medicatn_name",
            "hiv_aids", "hiv_aids_medicatn", "hiv_aids_medicatn_name",

            "other_medical",
            "nimregenin_herbal",
            "other_herbal",

            "radiotherapy_performed",
            "chemotherapy_performed",
            "surgery_performed",

            "remarks",
        ]
        
        widgets = {
            "diagnosis_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),

            # Selects
            "diabetic": forms.Select(attrs={"class": "form-select"}),
            "diabetic_medicatn": forms.Select(attrs={"class": "form-select"}),
            "hypertension": forms.Select(attrs={"class": "form-select"}),
            "hypertension_medicatn": forms.Select(attrs={"class": "form-select"}),
            "heart": forms.Select(attrs={"class": "form-select"}),
            "heart_medicatn": forms.Select(attrs={"class": "form-select"}),
            "asthma": forms.Select(attrs={"class": "form-select"}),
            "asthma_medicatn": forms.Select(attrs={"class": "form-select"}),
            "hiv_aids": forms.Select(attrs={"class": "form-select"}),
            "hiv_aids_medicatn": forms.Select(attrs={"class": "form-select"}),

            "other_medical": forms.Select(attrs={"class": "form-select"}),
            "nimregenin_herbal": forms.Select(attrs={"class": "form-select"}),
            "other_herbal": forms.Select(attrs={"class": "form-select"}),

            "radiotherapy_performed": forms.Select(attrs={"class": "form-select"}),
            "chemotherapy_performed": forms.Select(attrs={"class": "form-select"}),
            "surgery_performed": forms.Select(attrs={"class": "form-select"}),

            # Text inputs
            "diabetic_medicatn_name": forms.TextInput(attrs={"class": "form-control"}),
            "hypertension_medicatn_name": forms.TextInput(attrs={"class": "form-control"}),
            "heart_medicatn_name": forms.TextInput(attrs={"class": "form-control"}),
            "asthma_medicatn_name": forms.TextInput(attrs={"class": "form-control"}),
            "hiv_aids_medicatn_name": forms.TextInput(attrs={"class": "form-control"}),

            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    # =========================
    # EXTRA CLEAN (UI LEVEL)
    # =========================

    def clean(self):
        cleaned_data = super().clean()

        def get_val(value):
            return getattr(value, "name", "").lower() if value else None

        def is_yes(value):
            return get_val(value) == "yes"

        def is_no(value):
            return get_val(value) == "no"

        def is_unknown(value):
            return get_val(value) == "unknown"

        groups = [
            ("diabetic", "diabetic_medicatn", "diabetic_medicatn_name"),
            ("hypertension", "hypertension_medicatn", "hypertension_medicatn_name"),
            ("heart", "heart_medicatn", "heart_medicatn_name"),
            ("asthma", "asthma_medicatn", "asthma_medicatn_name"),
            ("hiv_aids", "hiv_aids_medicatn", "hiv_aids_medicatn_name"),
        ]

        for disease, med, name in groups:
            d = cleaned_data.get(disease)
            m = cleaned_data.get(med)
            n = cleaned_data.get(name)

            # Auto-clean instead of error (better UX 🔥)
            if is_no(d) or is_unknown(d):
                cleaned_data[med] = None
                cleaned_data[name] = ""

            if is_yes(d):
                if not m:
                    self.add_error(med, "This field is required.")

                if is_yes(m) and not n:
                    self.add_error(name, "Medication name is required.")

                if not is_yes(m):
                    cleaned_data[name] = ""

        return cleaned_data