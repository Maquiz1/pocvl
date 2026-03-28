from django import forms
from herbal.models.crfs.crf3.crf3_model import CRF3

class CRF3Form(forms.ModelForm):
    class Meta:
        model = CRF3
        fields = [
            "fever", "vomiting", "diarrhoea", "nausea", "loss_appetite",
            "headaches", "difficult_breathing", "sore_throat", "fatigue",
            "muscle_pain", "loss_consciousness", "backpain", "weight_loss",
            "heartburn_indigestion", "swelling", "pv_bleeding", "pv_discharge",
            "micturition", "convulsions", "blood_urine",
            "symptoms_other", "symptoms_other_specify",
            "adherence", "adherence_specify",
            "herbal_medication", "herbal_ingredients",
            "notes", "other_comments",
        ]

        widgets = {
            field: forms.Select(attrs={"class": "form-control"})
            for field in [
                "fever", "vomiting", "diarrhoea", "nausea", "loss_appetite",
                "headaches", "difficult_breathing", "sore_throat", "fatigue",
                "muscle_pain", "loss_consciousness", "backpain", "weight_loss",
                "heartburn_indigestion", "swelling", "pv_bleeding", "pv_discharge",
                "micturition", "convulsions", "blood_urine",
                "symptoms_other", "adherence", "herbal_medication",
            ]
        }
        widgets.update({
            "symptoms_other_specify": forms.TextInput(attrs={"class": "form-control"}),
            "adherence_specify": forms.TextInput(attrs={"class": "form-control"}),
            "herbal_ingredients": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "other_comments": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        })

    def clean(self):
        cleaned_data = super().clean()

        # Require all symptom fields
        symptom_fields = [
            "fever", "vomiting", "diarrhoea", "nausea", "loss_appetite",
            "headaches", "difficult_breathing", "sore_throat", "fatigue",
            "muscle_pain", "loss_consciousness", "backpain", "weight_loss",
            "heartburn_indigestion", "swelling", "pv_bleeding", "pv_discharge",
            "micturition", "convulsions", "blood_urine",
        ]
        for field in symptom_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This symptom is required.")

        # If symptoms_other = Yes, require specify
        if cleaned_data.get("symptoms_other") and str(cleaned_data["symptoms_other"].code) == "1":
            if not cleaned_data.get("symptoms_other_specify"):
                self.add_error("symptoms_other_specify", "Please specify other symptoms.")

        # If adherence = Yes, require specify
        if cleaned_data.get("adherence") and str(cleaned_data["adherence"].code) == "1":
            if not cleaned_data.get("adherence_specify"):
                self.add_error("adherence_specify", "Please provide adherence details.")

        # If herbal_medication = Yes, require ingredients
        if cleaned_data.get("herbal_medication") and str(cleaned_data["herbal_medication"].code) == "1":
            if not cleaned_data.get("herbal_ingredients"):
                self.add_error("herbal_ingredients", "Please provide herbal ingredients.")

        return cleaned_data
