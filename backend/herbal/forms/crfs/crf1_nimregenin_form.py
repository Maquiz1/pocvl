# herbal/forms/crfs/crf1_nimregenin_form.py

from django.forms import inlineformset_factory
from herbal.models import CRF1, CRF1Nimregenin


CRF1NimregeninFormSet = inlineformset_factory(
    CRF1,
    CRF1Nimregenin,
    fields=[
        "nimregenin_preparation",
        "nimregenin_start",
        "nimregenin_ongoing",
        "nimregenin_end",
        "nimregenin_dose",
        "nimregenin_frequency",
        "nimregenin_remarks",
    ],
    extra=0,  # 🔥 JS will control rows
    can_delete=True
)