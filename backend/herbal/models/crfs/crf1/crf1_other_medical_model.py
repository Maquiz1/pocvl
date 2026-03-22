# herbal/models/crfs/crf1_other_medical_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1OtherMedical(models.Model):

    crf = models.ForeignKey(
        CRF1,
        on_delete=models.CASCADE,
        related_name="other_medicals"
    )

    other_specify = models.CharField(max_length=255)

    other_medical_medicatn = models.ForeignKey(
        YesNoUnk,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    other_medicatn_name = models.CharField(max_length=255, blank=True)

    medication_remarks = models.TextField(blank=True)

    def __str__(self):
        return self.other_specify