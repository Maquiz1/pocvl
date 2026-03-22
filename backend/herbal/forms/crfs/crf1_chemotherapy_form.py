# herbal/forms/crfs/crf1_chemotherapy_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1
from herbal.models import CRF1Chemotherapy

CRF1ChemotherapyFormSet = inlineformset_factory(
    CRF1, CRF1Chemotherapy,
    fields=[
        "chemotherapy",
        "chemotherapy_start",
        "chemotherapy_ongoing",
        "chemotherapy_end",
        "chemotherapy_dose",
        "chemotherapy_frequency",
        "chemotherapy_remarks"
    ],
    extra=0,
    can_delete=True
)
