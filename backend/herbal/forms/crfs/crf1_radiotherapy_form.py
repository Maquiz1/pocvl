# herbal/forms/crfs/crf1_radiotherapy_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1
from herbal.models import CRF1Radiotherapy

CRF1RadiotherapyFormSet = inlineformset_factory(
    CRF1, CRF1Radiotherapy,
    fields=[
        "radiotherapy",
        "radiotherapy_start",
        "radiotherapy_ongoing",
        "radiotherapy_end",
        "radiotherapy_dose",
        "radiotherapy_frequency",
        "radiotherapy_remarks"
    ],
    extra=0,
    can_delete=True
)
