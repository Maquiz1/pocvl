# herbal/forms/crfs/crf1_surgery_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1
from herbal.models import CRF1Surgery


CRF1SurgeryFormSet = inlineformset_factory(
    CRF1, CRF1Surgery,
    fields=[
        "surgery",
        "surgery_start",
        "surgery_number",
        "surgery_remarks"
    ],
    extra=0,
    can_delete=True
)