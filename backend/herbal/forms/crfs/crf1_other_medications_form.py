# herbal/forms/crfs/crf1_other_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1
from herbal.models import CRF1OtherMedical

CRF1OtherMedicalFormSet = inlineformset_factory(
    CRF1,
    CRF1OtherMedical,
    fields=[
        "other_specify",
        "other_medical_medicatn",
        "other_medicatn_name",
        "medication_remarks"
    ],
    extra=0,
    can_delete=True
)