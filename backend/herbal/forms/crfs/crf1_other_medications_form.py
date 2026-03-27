# herbal/forms/crfs/crf1_other_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models import CRF1,CRF1OtherMedical

class CRF1OtherMedicalForm(forms.ModelForm):
    class Meta:
        model = CRF1OtherMedical
        fields = [
            "other_specify",
            "other_medical_medicatn",
            "other_medicatn_name",
            "medication_remarks"
        ]
        widgets = {
            "other_specify": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "other_medical_medicatn": forms.Select(attrs={
                "class": "form-select"
            }),
            "other_medicatn_name": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "medication_remarks": forms.TextInput(attrs={
                "class": "form-control"
            }),
        }
        
    def clean(self):
        cleaned_data = super().clean()

        med = cleaned_data.get("other_medical_medicatn")
        name = cleaned_data.get("other_medicatn_name")

        if med and not name:
            self.add_error("other_medicatn_name", "Provide medication name")

        return cleaned_data


CRF1OtherMedicalFormSet = inlineformset_factory(
    CRF1,
    CRF1OtherMedical,
    form=CRF1OtherMedicalForm,   # ✅ HERE
    extra=0,
    can_delete=True
)