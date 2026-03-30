from django import forms
from herbal.models.crfs.crf4.crf4_model import CRF4


class CRF4Form(forms.ModelForm):

    class Meta:
        model = CRF4

        fields = [
            # --- General ---
            "sample_date",

            # --- Renal ---
            "renal_creatinine",
            "renal_creatinine_units",
            "renal_creatinine_grade",
            
            "renal_urea",
            "renal_urea_units",
            "renal_urea_grade",
            
            "renal_egfr",
            "renal_egfr_units",
            "renal_egfr_grade",

            # --- Liver ---
            "liver_ast", "liver_ast_grade",
            "liver_alt", "liver_alt_grade",
            "liver_alp", "liver_alp_grade",
            "liver_pt", "liver_pt_grade",
            "liver_ptt", "liver_ptt_grade",
            "liver_inr", "liver_inr_grade",
            "liver_ggt", "liver_ggt_grade",
            "liver_albumin", "liver_albumin_grade",
            "liver_bilirubin_total", "liver_bilirubin_total_units", "bilirubin_total_grade",
            "liver_bilirubin_direct", "liver_bilirubin_direct_units", "bilirubin_direct_grade",

            # --- Glucose / Inflammation ---
            "rbg","rbg_units","rbg_grade",
            "ldh","ldh_grade",
            "crp","crp_grade",
            "d_dimer", "d_dimer_grade",
            "ferritin","ferritin_grade",

            # --- Hematology ---
            "hb", "hb_grade",
            "rbc","rbc_grade",
            "hct","hct_grade",
            "wbc", "wbc_grade",
            "plt", "plt_grade",
            "abs_neutrophil", "abs_neutrophil_grade",
            "abs_lymphocytes", "abs_lymphocytes_grade",
            "abs_eosinophils","abs_eosinophils_grade",
            "abs_monocytes","abs_monocytes_grade",
            "abs_basophils","abs_basophils_grade",
            "mcv", "mcv_grade",
            "mch", "mch_grade",

            # --- Imaging ---
            "cancer",
            "prostate",
            
            "chest_xray", "chest_specify",
            "ct_chest", "ct_chest_specify",
            "ultrasound", "ultrasound_specify",
            
            # --- Medication ---
            "remarks",
        ]
        
        labels={
            "sample_date":"Date of Sample Collection",
            
            # --- Renal ---
            "renal_creatinine":"Serum Creatinine Levels",
            "renal_creatinine_units":"Serum Creatinine Levels Units",
            "renal_creatinine_grade":"Serum Creatinine Levels Grade",
            
            "renal_urea":"Serum Urea Levels",
            "renal_urea_units":"Serum Urea Levels Units",
            "renal_urea_grade":"Serum Urea Levels Grade",

            "renal_egfr":"eGFR",
            "renal_egfr_units":"eGFR (mL/min per 1.73 m²) Units",
            "renal_egfr_grade":"eGFR Grade",
            
            "cancer":"Cancer",
            "prostate":"Prostate",
        }

        widgets = {
            # --- Booleans ---
            "medication_given": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "adherence": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "cancer": forms.NumberInput(attrs={"class": "form-control"}),
            "prostate": forms.NumberInput(attrs={"class": "form-control"}),
            # "chest_xray": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            # "ct_chest": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            # "ultrasound": forms.CheckboxInput(attrs={"class": "form-check-input"}),

            # --- Text ---
            "dosage": forms.TextInput(attrs={"class": "form-control"}),

            # --- Textareas ---
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "chest_specify": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "ct_chest_specify": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "ultrasound_specify": forms.Textarea(attrs={"class": "form-control", "rows": 2}),

            # --- Dates ---
            "sample_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),

            # --- Default numeric/text styling ---
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply form-control to all non-checkbox fields
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                if "class" not in field.widget.attrs:
                    field.widget.attrs["class"] = "form-control"
                    
                    
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get("chest_xray") and not cleaned_data.get("chest_specify"):
            self.add_error("chest_specify", "Please specify chest X-ray findings")

        if cleaned_data.get("ct_chest") and not cleaned_data.get("ct_chest_specify"):
            self.add_error("ct_chest_specify", "Please specify CT chest findings")

        if cleaned_data.get("ultrasound") and not cleaned_data.get("ultrasound_specify"):
            self.add_error("ultrasound_specify", "Please specify ultrasound findings")

        return cleaned_data