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
            "remarks",
        ]

        labels = {
            "symptoms_other":"Other symptoms",
            "symptoms_other_specify":"Specify",
            "adherence":"Do you take NIMREGENIN as advised (i.e., daily)?",
            "adherence_specify":"If No Specify why",
            "herbal_medication":"Have you taken any herbal medication?",
            "herbal_ingredients":"Specify type by name or ingredients",
            "remarks":"Remarks"
        }
        
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
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        })

    def clean(self):
        cleaned_data = super().clean()

        # ----------------------------
        # REQUIRED SYMPTOMS
        # ----------------------------
        symptom_fields = [
            "fever", "vomiting", "diarrhoea", "nausea", "loss_appetite",
            "headaches", "difficult_breathing", "sore_throat", "fatigue",
            "muscle_pain", "loss_consciousness", "backpain", "weight_loss",
            "heartburn_indigestion", "swelling", "pv_bleeding", "pv_discharge",
            "micturition", "convulsions", "blood_urine", "symptoms_other",
        ]

        for field in symptom_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "This symptom is required.")

        # ----------------------------
        # OTHER SYMPTOMS
        # ----------------------------
        symptoms_other = cleaned_data.get("symptoms_other")
        if symptoms_other and symptoms_other.code == "yes":
            if not cleaned_data.get("symptoms_other_specify"):
                self.add_error("symptoms_other_specify", "Please specify other symptoms.")

        # ----------------------------
        # GET VISIT + CONSENT SAFELY
        # ----------------------------
        visit = getattr(self.instance, "visit", None)

        consent_nimregenin = None
        if visit and visit.enrollment and visit.enrollment.screening:
            consent_nimregenin = visit.enrollment.screening.consent_nimregenin

        # ----------------------------
        # ADHERENCE LOGIC
        # ----------------------------
        if visit and visit.visit_day.code != "D0" and consent_nimregenin:

            adherence = cleaned_data.get("adherence")
            specify = cleaned_data.get("adherence_specify")

            # =========================
            # 🔴 CASE 1: ON NIMREGENIN
            # =========================
            if consent_nimregenin.code == "yes":

                # REQUIRED
                if not adherence:
                    self.add_error(
                        "adherence",
                        "This field is required for patients on NIMREGENIN."
                    )

                # NO → require specify
                elif adherence.code == "no":
                    if not specify:
                        self.add_error(
                            "adherence_specify",
                            "Please specify why not adhering."
                        )

                # YES or UNKNOWN → must be empty
                elif adherence.code in ["yes", "unknown"]:
                    if specify:
                        self.add_error(
                            "adherence_specify",
                            "Must be empty unless patient is NOT adhering."
                        )

            # =========================
            # 🔴 CASE 2: NOT ON NIMREGENIN / UNKNOWN
            # =========================
            elif consent_nimregenin.code in ["no", "unknown"]:

                if adherence:
                    self.add_error(
                        "adherence",
                        "This field must be empty for patients not on NIMREGENIN."
                    )

                if specify:
                    self.add_error(
                        "adherence_specify",
                        "This field must be empty for patients not on NIMREGENIN."
                    )

        # else:
        #     self.add_error(
        #         "adherence",
        #         "This field is is not required since patient is NOT on NIMREGENIN and the Day is Day '0'"
        #     )
        # ----------------------------
        # HERBAL MEDICATION LOGIC
        # ----------------------------
        if consent_nimregenin:

            herbal = cleaned_data.get("herbal_medication")
            ingredients = cleaned_data.get("herbal_ingredients")

            # =========================
            # 🔴 CASE 1: NOT ON NIMREGENIN
            # =========================
            if consent_nimregenin.code == "no":

                # REQUIRED
                if not herbal:
                    self.add_error(
                        "herbal_medication",
                        "This field is required since patient is NOT on NIMREGENIN."
                    )

                # YES → ingredients required
                elif herbal.code == "yes":
                    if not ingredients:
                        self.add_error(
                            "herbal_ingredients",
                            "Please provide herbal ingredients."
                        )

                # NO → ingredients must be empty
                elif herbal.code in ["no", "unknown"]:
                    if ingredients:
                        self.add_error(
                            "herbal_ingredients",
                            "Must be empty if no herbal medication was taken."
                        )

            # =========================
            # 🔴 CASE 2: ON NIMREGENIN OR UNKNOWN
            # =========================
            elif consent_nimregenin.code in ["yes", "unknown"]:

                if herbal:
                    self.add_error(
                        "herbal_medication",
                        "This field must be empty for patients on NIMREGENIN."
                    )

                if ingredients:
                    self.add_error(
                        "herbal_ingredients",
                        "This field must be empty for patients on NIMREGENIN."
                    )

        return cleaned_data