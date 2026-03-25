from django import forms
from herbal.models import CRF2


class CRF2Form(forms.ModelForm):

    class Meta:
        model = CRF2
        exclude = ["visit"]  # 🔥 important (set in view)

        widgets = {
            # Dates & Times
            "test_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "date_completed": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "vital_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            "phys_exm_time": forms.TimeInput(
                attrs={"type": "time", "class": "form-control"}
            ),
            # Numbers
            "height": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "bmi": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "temperature": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.1"}
            ),
            "respiratory_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "heart_rate": forms.NumberInput(attrs={"class": "form-control"}),
            "systolic": forms.NumberInput(attrs={"class": "form-control"}),
            "diastolic": forms.NumberInput(attrs={"class": "form-control"}),

            "appearance_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "heent_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "respiratory_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "cardiovascular_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "abdominal_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "urogenital_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "musculoskeletal_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "neurological_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "psychological_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "endocrine_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "lymphatic_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "skin_comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "local_examination_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            "physical_other_comments": forms.Textarea(
                attrs={"class": "form-control", "rows": 2}
            ),
            
            # Textareas
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "additional_notes": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
        }

    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = [
            "test_date",
            "vital_time",
            "height",
            "weight",
            "temperature",
            "respiratory_rate",
            "heart_rate",
            "systolic",
            "diastolic",
            "method",
                        
            # SYSTEMS
            "appearance",
            "heent",
            "respiratory",
            "cardiovascular",
            "abdominal",
            "urogenital",
            "musculoskeletal",
            "neurological",
            "psychological",
            "endocrine",
            "lymphatic",
            "skin",
            "local_examination",
            "physical_exams_other",
            
            # FINAL
            "date_completed",
            "phys_exm_time",
            "physcl_pfmd_by",
        ]

        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True
                # self.fields[field].widget.attrs["required"] = True
                self.fields[field].widget.attrs["required"] = "required"
                
        # 🔥 Apply Bootstrap to ALL fields automatically
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "form-control")

        # 🔥 Optional: filter staff by site
        if site and "physcl_pfmd_by" in self.fields:
            self.fields["physcl_pfmd_by"].queryset = self.fields[
                "physcl_pfmd_by"
            ].queryset.filter(site=site)

    def clean(self):
        cleaned_data = super().clean()

        # --------------------
        # APPEARANCE
        # --------------------
        appearance = cleaned_data.get("appearance")
        appearance_comments = cleaned_data.get("appearance_comments")
        appearance_signif = cleaned_data.get("appearance_signifcnt")

        if appearance and appearance.id == 2:
            if not appearance_signif:
                self.add_error("appearance_signifcnt", "This field is required")
        elif appearance:
            if appearance_comments:
                self.add_error("appearance_comments", "Must be empty when not abnormal")
            if appearance_signif:
                self.add_error("appearance_signifcnt", "Must be empty when not abnormal")
            cleaned_data["appearance_comments"] = ""
            cleaned_data["appearance_signifcnt"] = None


        # --------------------
        # HEENT
        # --------------------
        heent = cleaned_data.get("heent")
        heent_comments = cleaned_data.get("heent_comments")
        heent_signif = cleaned_data.get("heent_signifcnt")

        if heent and heent.id == 2:
            if not heent_signif:
                self.add_error("heent_signifcnt", "This field is required")
        elif heent:
            if heent_comments:
                self.add_error("heent_comments", "Must be empty when not abnormal")
            if heent_signif:
                self.add_error("heent_signifcnt", "Must be empty when not abnormal")
            cleaned_data["heent_comments"] = ""
            cleaned_data["heent_signifcnt"] = None


        # --------------------
        # RESPIRATORY
        # --------------------
        respiratory = cleaned_data.get("respiratory")
        respiratory_comments = cleaned_data.get("respiratory_comments")
        respiratory_signif = cleaned_data.get("respiratory_signifcnt")

        if respiratory and respiratory.id == 2:
            if not respiratory_signif:
                self.add_error("respiratory_signifcnt", "This field is required")
        elif respiratory:
            if respiratory_comments:
                self.add_error("respiratory_comments", "Must be empty when not abnormal")
            if respiratory_signif:
                self.add_error("respiratory_signifcnt", "Must be empty when not abnormal")
            cleaned_data["respiratory_comments"] = ""
            cleaned_data["respiratory_signifcnt"] = None


        # --------------------
        # CARDIOVASCULAR
        # --------------------
        cardiovascular = cleaned_data.get("cardiovascular")
        cardiovascular_comments = cleaned_data.get("cardiovascular_comments")
        cardiovascular_signif = cleaned_data.get("cardiovascular_signifcnt")

        if cardiovascular and cardiovascular.id == 2:
            if not cardiovascular_signif:
                self.add_error("cardiovascular_signifcnt", "This field is required")
        elif cardiovascular:
            if cardiovascular_comments:
                self.add_error("cardiovascular_comments", "Must be empty when not abnormal")
            if cardiovascular_signif:
                self.add_error("cardiovascular_signifcnt", "Must be empty when not abnormal")
            cleaned_data["cardiovascular_comments"] = ""
            cleaned_data["cardiovascular_signifcnt"] = None


        # --------------------
        # ABDOMINAL
        # --------------------
        abdominal = cleaned_data.get("abdominal")
        abdominal_comments = cleaned_data.get("abdominal_comments")
        abdominal_signif = cleaned_data.get("abdominal_signifcnt")

        if abdominal and abdominal.id == 2:
            if not abdominal_signif:
                self.add_error("abdominal_signifcnt", "This field is required")
        elif abdominal:
            if abdominal_comments:
                self.add_error("abdominal_comments", "Must be empty when not abnormal")
            if abdominal_signif:
                self.add_error("abdominal_signifcnt", "Must be empty when not abnormal")
            cleaned_data["abdominal_comments"] = ""
            cleaned_data["abdominal_signifcnt"] = None


        # --------------------
        # UROGENITAL
        # --------------------
        urogenital = cleaned_data.get("urogenital")
        urogenital_comments = cleaned_data.get("urogenital_comments")
        urogenital_signif = cleaned_data.get("urogenital_signifcnt")

        if urogenital and urogenital.id == 2:
            if not urogenital_signif:
                self.add_error("urogenital_signifcnt", "This field is required")
        elif urogenital:
            if urogenital_comments:
                self.add_error("urogenital_comments", "Must be empty when not abnormal")
            if urogenital_signif:
                self.add_error("urogenital_signifcnt", "Must be empty when not abnormal")
            cleaned_data["urogenital_comments"] = ""
            cleaned_data["urogenital_signifcnt"] = None


        # --------------------
        # MUSCULOSKELETAL
        # --------------------
        musculoskeletal = cleaned_data.get("musculoskeletal")
        musculoskeletal_comments = cleaned_data.get("musculoskeletal_comments")
        musculoskeletal_signif = cleaned_data.get("musculoskeletal_signifcnt")

        if musculoskeletal and musculoskeletal.id == 2:
            if not musculoskeletal_signif:
                self.add_error("musculoskeletal_signifcnt", "This field is required")
        elif musculoskeletal:
            if musculoskeletal_comments:
                self.add_error("musculoskeletal_comments", "Must be empty when not abnormal")
            if musculoskeletal_signif:
                self.add_error("musculoskeletal_signifcnt", "Must be empty when not abnormal")
            cleaned_data["musculoskeletal_comments"] = ""
            cleaned_data["musculoskeletal_signifcnt"] = None


        # --------------------
        # NEUROLOGICAL
        # --------------------
        neurological = cleaned_data.get("neurological")
        neurological_comments = cleaned_data.get("neurological_comments")
        neurological_signif = cleaned_data.get("neurological_signifcnt")

        if neurological and neurological.id == 2:
            if not neurological_signif:
                self.add_error("neurological_signifcnt", "This field is required")
        elif neurological:
            if neurological_comments:
                self.add_error("neurological_comments", "Must be empty when not abnormal")
            if neurological_signif:
                self.add_error("neurological_signifcnt", "Must be empty when not abnormal")
            cleaned_data["neurological_comments"] = ""
            cleaned_data["neurological_signifcnt"] = None


        # --------------------
        # PSYCHOLOGICAL
        # --------------------
        psychological = cleaned_data.get("psychological")
        psychological_comments = cleaned_data.get("psychological_comments")
        psychological_signif = cleaned_data.get("psychological_signifcnt")

        if psychological and psychological.id == 2:
            if not psychological_signif:
                self.add_error("psychological_signifcnt", "This field is required")
        elif psychological:
            if psychological_comments:
                self.add_error("psychological_comments", "Must be empty when not abnormal")
            if psychological_signif:
                self.add_error("psychological_signifcnt", "Must be empty when not abnormal")
            cleaned_data["psychological_comments"] = ""
            cleaned_data["psychological_signifcnt"] = None


        # --------------------
        # ENDOCRINE
        # --------------------
        endocrine = cleaned_data.get("endocrine")
        endocrine_comments = cleaned_data.get("endocrine_comments")
        endocrine_signif = cleaned_data.get("endocrine_signifcnt")

        if endocrine and endocrine.id == 2:
            if not endocrine_signif:
                self.add_error("endocrine_signifcnt", "This field is required")
        elif endocrine:
            if endocrine_comments:
                self.add_error("endocrine_comments", "Must be empty when not abnormal")
            if endocrine_signif:
                self.add_error("endocrine_signifcnt", "Must be empty when not abnormal")
            cleaned_data["endocrine_comments"] = ""
            cleaned_data["endocrine_signifcnt"] = None


        # --------------------
        # LYMPHATIC
        # --------------------
        lymphatic = cleaned_data.get("lymphatic")
        lymphatic_comments = cleaned_data.get("lymphatic_comments")
        lymphatic_signif = cleaned_data.get("lymphatic_signifcnt")

        if lymphatic and lymphatic.id == 2:
            if not lymphatic_signif:
                self.add_error("lymphatic_signifcnt", "This field is required")
        elif lymphatic:
            if lymphatic_comments:
                self.add_error("lymphatic_comments", "Must be empty when not abnormal")
            if lymphatic_signif:
                self.add_error("lymphatic_signifcnt", "Must be empty when not abnormal")
            cleaned_data["lymphatic_comments"] = ""
            cleaned_data["lymphatic_signifcnt"] = None


        # --------------------
        # SKIN
        # --------------------
        skin = cleaned_data.get("skin")
        skin_comments = cleaned_data.get("skin_comments")
        skin_signif = cleaned_data.get("skin_signifcnt")

        if skin and skin.id == 2:
            if not skin_signif:
                self.add_error("skin_signifcnt", "This field is required")
        elif skin:
            if skin_comments:
                self.add_error("skin_comments", "Must be empty when not abnormal")
            if skin_signif:
                self.add_error("skin_signifcnt", "Must be empty when not abnormal")
            cleaned_data["skin_comments"] = ""
            cleaned_data["skin_signifcnt"] = None
            
            
        # --------------------
        # local_examination
        # --------------------
        local_examination = cleaned_data.get("local_examination")

        if local_examination and local_examination.id == 2:
            if not cleaned_data.get("local_examination_signifcnt"):
                self.add_error("local_examination_signifcnt", "This field is required")
        else:
            cleaned_data["local_examination_signifcnt"] = None
            
            
        # --------------------
        # physical_exams_other
        # --------------------
        physical_exams_other = cleaned_data.get("physical_exams_other")

        if physical_exams_other and physical_exams_other.id == 2:
            if not cleaned_data.get("physical_other_specify"):
                self.add_error("physical_other_specify", "This field is required")
            if not cleaned_data.get("physical_other_system"):
                self.add_error("physical_other_system", "This field is required")
            if not cleaned_data.get("physical_other_signifcnt"):
                self.add_error("physical_other_signifcnt", "This field is required")
        else:
            cleaned_data["physical_other_signifcnt"] = None

        return cleaned_data
