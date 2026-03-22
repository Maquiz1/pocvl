# herbal/forms/crfs/crf1_other_herbal_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1OtherHerbal


CRF1OtherHerbalFormSet = inlineformset_factory(
    CRF1,
    CRF1OtherHerbal,
    fields=[
        "herbal_preparation",
        "herbal_start",
        "herbal_ongoing",
        "herbal_end",
        "herbal_dose",
        "herbal_frequency",
        "herbal_remarks",
    ],
    extra=0,
    can_delete=True
)