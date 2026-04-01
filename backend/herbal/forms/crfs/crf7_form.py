from django import forms
from herbal.models.crfs.crf7.crf7_model import CRF7


class CRF7Form(forms.ModelForm):

    class Meta:
        model = CRF7
        fields = [
            "tdate",
            "mobility",
            "self_care",
            "usual_active",
            "pain",
            "anxiety",
            # "fdate",
            "cpersid",
            # "cdate",
            "remarks",
        ]
        
        labels={
            "tdate":"Tarehe ya Leo",
            # "cdate":"DATE FORM CHECKED",
            # "fdate":"DATE FORM COMPLETED",
            "cpersid":"NAME OF PERSON CHECKING FORM:",
            "mobility":"A. Uwezo wa kutembea",
            "self_care":"B. Uwezo wa kujihudumia",
            "usual_active":"C. Shughuli za kila siku",
            "pain":"D. Maumivu/Kutojisikia vizuri",
            "anxiety":"E. Wasiwasi/sonona",
            "remarks":"Remarks",
        }

        widgets = {
            "tdate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            # "fdate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            # "cdate": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "cpersid": forms.Select(attrs={"class": "form-control"}),
            # ✅ FK → SELECT
            "mobility": forms.Select(attrs={"class": "form-control"}),
            "self_care": forms.Select(attrs={"class": "form-control"}),
            "usual_active": forms.Select(attrs={"class": "form-control"}),
            "pain": forms.Select(attrs={"class": "form-control"}),
            "anxiety": forms.Select(attrs={"class": "form-control"}),
            "remarks": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        
    def __init__(self, *args, site=None, **kwargs):
        super().__init__(*args, **kwargs)

        required_fields = [
            "tdate",
            "fdate",
            "cdate",
            "cpersid",
            "mobility",
            "self_care",
            "usual_active",
            "pain",
            "anxiety",
        ]

        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True
                self.fields[field].widget.attrs["required"] = True
                # self.fields[field].widget.attrs["required"] = "required"
                
        # 🔥 Apply Bootstrap to ALL fields automatically
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "form-control")

        # 🔥 Optional: filter staff by site
        if site and "cpersid" in self.fields:
            self.fields["cpersid"].queryset = self.fields[
                "cpersid"
            ].queryset.filter(site=site)
