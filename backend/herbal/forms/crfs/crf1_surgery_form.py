# herbal/forms/crfs/crf1_surgery_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1Surgery


class CRF1SurgeryForm(forms.ModelForm):
    class Meta:
        model = CRF1Surgery
        fields = [
            "surgery",
            "surgery_start",
            "surgery_number",
            "surgery_remarks",
        ]
        widgets = {
            "surgery": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Procedure"
            }),
            "surgery_start": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
            "surgery_number": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Number"
            }),
            "surgery_remarks": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Remarks"
            }),
        }

    # 🔥 Example validation
    def clean(self):
        cleaned_data = super().clean()
        procedure = cleaned_data.get("surgery")
        date = cleaned_data.get("surgery_start")

        # Rule: if a procedure is given, must have a date
        if procedure and not date:
            self.add_error("surgery_start", "Provide a date for the surgery procedure")

        return cleaned_data


CRF1SurgeryFormSet = inlineformset_factory(
    CRF1,
    CRF1Surgery,
    form=CRF1SurgeryForm,   # 🔥 use the custom form
    extra=0,
    can_delete=True
)
