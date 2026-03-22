# herbal/models/crfs/crf1_nimregenin_model.py

from django.db import models
from choices.models import YesNoUnk
from .crf1_model import CRF1


class CRF1Nimregenin(models.Model):

    crf = models.ForeignKey(
        CRF1,
        on_delete=models.CASCADE,
        related_name="nimregenins"
    )

    nimregenin_preparation = models.CharField(max_length=255)

    nimregenin_start = models.DateField(null=True, blank=True)

    nimregenin_ongoing = models.ForeignKey(
        YesNoUnk,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    nimregenin_end = models.DateField(null=True, blank=True)

    nimregenin_dose = models.CharField(max_length=255)

    nimregenin_frequency = models.CharField(max_length=255)

    nimregenin_remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Nimregenin - {self.nimregenin_preparation}"