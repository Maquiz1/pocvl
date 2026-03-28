# herbal/forms/crfs/crf2_other_form.py

from django import forms
from django.forms import inlineformset_factory
from herbal.models.crfs.crf2.crf2_model import CRF2
from herbal.models.crfs.crf2.crf2_other_physical_system_model import CRF2OtherPhysclExam


class CRF2OtherPhysclExamForm(forms.ModelForm):
    class Meta:
        model = CRF2OtherPhysclExam
        fields = ["system", "finding", "comments", "signifcnt"]
        widgets = {
            "system": forms.TextInput(attrs={"class": "form-control"}),
            "finding": forms.Select(attrs={"class": "form-select"}),
            "comments": forms.Textarea(attrs={"class": "form-control", "rows": 2}),
            "signifcnt": forms.Select(attrs={"class": "form-select"}),
        }


CRF2OtherPhysclExamFormSet = inlineformset_factory(
    CRF2,
    CRF2OtherPhysclExam,
    form=CRF2OtherPhysclExamForm,
    extra=0,
    can_delete=True
)